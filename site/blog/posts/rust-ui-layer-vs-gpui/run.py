#!/usr/bin/env python3
"""Benchmark the GPUI and Tauri prototypes (and, optionally, real Podbag Desktop).

Stdlib only. Run from anywhere:

    python3 bench/run.py                      # all variants, N=100,1000,10000, K=5
    python3 bench/run.py --rows 1000 --runs 3 --variants gpui,tauri-full
    python3 bench/run.py --build-stats        # also clean release build times, sizes, deps
    python3 bench/run.py --podbag             # also real Podbag Desktop (window time, memory)

Per run: spawn, wait for `READY`, idle 3 s, measure memory (footprint) of the app and its
helper processes (WebKit XPC services are not children of the app; they are found by diffing
the process list), measure CPU over 10 s of idle, send `filter web-0004` on stdin and wait
for `FILTER`, then send `quit`, and make sure no helper process is left.
"""

import argparse
import datetime
import json
import os
import platform
import queue
import re
import signal
import statistics
import subprocess
import sys
import threading
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCH = os.path.join(ROOT, "bench")
GPUI_BIN = os.path.join(ROOT, "gpui-app", "target", "release", "gpui-app")
TAURI_BIN = os.path.join(ROOT, "tauri-app", "target", "release", "tauri-app")
OWN_BIN = os.path.join(ROOT, "own-app", "target", "release", "own-app")
OWN_FULL_BIN = os.path.join(ROOT, "own-full", "target", "release", "own-full")
PODBAG_SRC = os.environ.get("PODBAG_SRC", os.path.join(ROOT, "podbag"))
PODBAG_TARGET = os.path.join(ROOT, "podbag-target")
PODBAG_BIN = os.path.join(PODBAG_TARGET, "release", "podbag-desktop")
WINWAIT = os.path.join(BENCH, "tools", "winwait")

VARIANTS = {
    "gpui": lambda n: [GPUI_BIN, "--rows", str(n)],
    "own": lambda n: [OWN_BIN, "--rows", str(n)],
    "own-full": lambda n: [OWN_FULL_BIN, "--rows", str(n)],
    "gpui-full": lambda n: [os.path.join(ROOT, "gpui-full", "target", "release", "gpui-full"), "--rows", str(n)],
    "tauri-full": lambda n: [TAURI_BIN, "--rows", str(n), "--mode", "full"],
    "tauri-virtual": lambda n: [TAURI_BIN, "--rows", str(n), "--mode", "virtual"],
}

IDLE_BEFORE_MEM_S = 3.0
CPU_WINDOW_S = 10.0
READY_TIMEOUT_S = 60.0
FILTER_QUERY = "web-0004"
NAV_VIEWS = ["images", "volumes", "networks", "kubernetes", "settings", "containers"]
EXPECTED_VISIBLE = {100: 2, 1000: 2, 10000: 2}  # web-00040 and web-00045
RETRIES = 2


# ---- system helpers ----

def screen_locked():
    try:
        out = subprocess.run(["ioreg", "-n", "Root", "-d1"], capture_output=True, text=True).stdout
    except OSError:
        return None
    m = re.search(r'"CGSSessionScreenIsLocked"=(\w+)', out)
    return m is not None and m.group(1) == "Yes"


def processes():
    """pid -> (ppid, command path)."""
    out = subprocess.run(["ps", "-axo", "pid=,ppid=,comm="], capture_output=True, text=True).stdout
    procs = {}
    for line in out.splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) == 3:
            procs[int(parts[0])] = (int(parts[1]), parts[2])
    return procs


def app_processes(pid, before):
    """The app, its descendants, and new XPC services (ppid 1) started since `before`."""
    procs = processes()
    tree = {pid}
    changed = True
    while changed:
        changed = False
        for p, (pp, _) in procs.items():
            if pp in tree and p not in tree:
                tree.add(p)
                changed = True
    helpers = {p for p, (pp, comm) in procs.items()
               if p not in before and pp == 1 and "/XPCServices/" in comm}
    found = tree | helpers
    return {p: os.path.basename(procs[p][1]) for p in found if p in procs}


def footprint(pids):
    """pid -> phys_footprint bytes, via `footprint -j`."""
    result = {}
    if not pids:
        return result
    path = os.path.join(BENCH, ".footprint.json")
    args = ["footprint", "-f", "bytes", "--noCategories", "-j", path]
    for p in pids:
        args += ["-p", str(p)]
    subprocess.run(args, capture_output=True, text=True)
    try:
        with open(path) as f:
            data = json.load(f)
        for proc in data.get("processes", []):
            result[proc["pid"]] = proc["auxiliary"]["phys_footprint"]
    except (OSError, ValueError, KeyError):
        pass
    finally:
        if os.path.exists(path):
            os.remove(path)
    missing = [p for p in pids if p not in result]
    if missing and len(pids) > 1:
        for p in missing:  # one failing pid makes the whole call fail; retry one by one
            result.update(footprint([p]))
    return result


def parse_cputime(s):
    """ps `time` column ('M:SS.cc' or 'H:MM:SS.cc' or 'D-HH:MM:SS') -> seconds."""
    days = 0
    if "-" in s:
        d, s = s.split("-", 1)
        days = int(d)
    parts = [float(x) for x in s.split(":")]
    secs = 0.0
    for x in parts:
        secs = secs * 60 + x
    return days * 86400 + secs


def cputimes(pids):
    if not pids:
        return {}
    out = subprocess.run(["ps", "-o", "pid=,time=", "-p", ",".join(str(p) for p in pids)],
                         capture_output=True, text=True).stdout
    res = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 2:
            res[int(parts[0])] = parse_cputime(parts[1])
    return res


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def wait_gone(pids, timeout):
    end = time.time() + timeout
    left = set(pids)
    while left and time.time() < end:
        left = {p for p in left if alive(p)}
        if left:
            time.sleep(0.1)
    return left


# ---- one run ----

class Reader(threading.Thread):
    def __init__(self, stream):
        super().__init__(daemon=True)
        self.stream = stream
        self.lines = queue.Queue()

    def run(self):
        for line in self.stream:
            self.lines.put((time.perf_counter(), line.strip()))
        self.lines.put((time.perf_counter(), None))

    def drain(self):
        lines = []
        while True:
            try:
                _, line = self.lines.get_nowait()
            except queue.Empty:
                return lines
            if line is not None:
                lines.append(line)

    def wait_for(self, prefix, timeout):
        end = time.perf_counter() + timeout
        while True:
            left = end - time.perf_counter()
            if left <= 0:
                return None, None
            try:
                t, line = self.lines.get(timeout=left)
            except queue.Empty:
                return None, None
            if line is None:
                return None, None
            if line.startswith(prefix):
                return t, line


def stop(proc, helpers, graceful=True):
    """Quit the app and make sure no helper process stays. Returns lingering helpers."""
    if graceful and proc.poll() is None:
        try:
            proc.stdin.write("quit\n")
            proc.stdin.flush()
        except (BrokenPipeError, OSError):
            pass
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
    others = [p for p in helpers if p != proc.pid]
    lingering = wait_gone(others, 10)
    names = {p: helpers[p] for p in lingering}
    # Only WebKit services are ours for sure; other XPC services are reported, not killed.
    lingering = {p for p in lingering if helpers[p].startswith("com.apple.WebKit")}
    for p in lingering:
        try:
            os.kill(p, signal.SIGTERM)
        except ProcessLookupError:
            pass
    still = wait_gone(lingering, 3)
    for p in still:
        try:
            os.kill(p, signal.SIGKILL)
        except ProcessLookupError:
            pass
    return [{"pid": p, "name": n, "killed": p in lingering} for p, n in sorted(names.items())]


def measure_resources(pid, before):
    procs = app_processes(pid, before)
    fp = footprint(sorted(procs))
    mem = {
        "app_bytes": fp.get(pid),
        "total_bytes": sum(fp.values()) if fp else None,
        "processes": [{"pid": p, "name": procs[p], "bytes": fp.get(p)} for p in sorted(procs)],
    }
    t0 = time.perf_counter()
    c0 = cputimes(sorted(procs))
    time.sleep(CPU_WINDOW_S)
    c1 = cputimes(sorted(procs))
    dt = time.perf_counter() - t0
    per = {p: (c1[p] - c0[p]) / dt * 100 for p in c0 if p in c1}
    cpu = {
        "window_s": round(dt, 2),
        "app_pct": per.get(pid),
        "total_pct": sum(per.values()) if per else None,
        "processes": [{"pid": p, "name": procs[p], "pct": per.get(p)} for p in sorted(procs)],
    }
    return procs, mem, cpu


def one_run(variant, n, index, cold):
    cmd = VARIANTS[variant](n)
    rec = {"variant": variant, "rows": n, "run": index, "cold": cold,
           "screen_locked": screen_locked(), "errors": []}
    before = set(processes())
    t_spawn = time.perf_counter()
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, text=True, bufsize=1)
    reader = Reader(proc.stdout)
    reader.start()
    helpers = {}
    try:
        t_ready, line = reader.wait_for("READY", READY_TIMEOUT_S)
        if t_ready is None:
            rec["errors"].append("no READY line")
            helpers = app_processes(proc.pid, before)
            return rec
        rec["startup_ms"] = round((t_ready - t_spawn) * 1000, 1)
        rec["ready_in_app_ms"] = float(line.split()[1])
        _, line = reader.wait_for("RENDER", 5)
        rec["render_ms"] = float(line.split()[1]) if line else None
        if variant.startswith("tauri"):
            _, line = reader.wait_for("DATA", 5)
            rec["data_ms"] = float(line.split()[1]) if line else None

        time.sleep(IDLE_BEFORE_MEM_S)
        helpers, rec["memory"], rec["cpu"] = measure_resources(proc.pid, before)

        stray = reader.drain()
        if any(l.startswith("FILTER") for l in stray):
            rec["errors"].append("search input changed before the scripted filter (user typing?)")
        proc.stdin.write(f"filter {FILTER_QUERY}\n")
        proc.stdin.flush()
        _, line = reader.wait_for("FILTER", 15)
        if line:
            parts = line.split()
            rec["filter_ms"] = float(parts[1])
            rec["filter_visible"] = int(parts[2])
            if rec["filter_visible"] != EXPECTED_VISIBLE.get(n):
                rec["errors"].append(f"filter showed {parts[2]} rows, expected {EXPECTED_VISIBLE.get(n)}")
        else:
            rec["errors"].append("no FILTER line (window occluded?)")
        if variant in ("gpui-full", "own-full"):
            # Full ports: switch through every view, then read memory again.
            rec["views"] = {}
            for view in NAV_VIEWS:
                proc.stdin.write(f"nav {view}\n")
                proc.stdin.flush()
                _, line = reader.wait_for("VIEW", 10)
                if line and line.split()[1] == view:
                    rec["views"][view] = float(line.split()[2])
                else:
                    rec["errors"].append(f"no VIEW line for {view}")
                time.sleep(0.5)
            time.sleep(1.0)
            procs = {**helpers, **app_processes(proc.pid, before)}
            fp = footprint(sorted(procs))
            rec["memory_after_views"] = {"app_bytes": fp.get(proc.pid),
                                         "total_bytes": sum(fp.values()) if fp else None}
        time.sleep(0.3)
        helpers = {**helpers, **app_processes(proc.pid, before)}
        return rec
    finally:
        rec["lingering_helpers"] = stop(proc, helpers)
        time.sleep(1.0)


# ---- real Podbag Desktop ----

def window_run(cmd, label, idle_s=8.0, env=None):
    """Spawn, wait for a visible window (CGWindowList), idle, then memory and CPU."""
    rec = {"label": label, "cmd": cmd, "screen_locked": screen_locked(), "errors": []}
    before = set(processes())
    t_spawn = time.perf_counter()
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL, text=True, env=env)
    w = subprocess.run([WINWAIT, str(proc.pid), "30"], capture_output=True, text=True)
    t_win = time.perf_counter()
    if w.stdout.startswith("WINDOW"):
        rec["window_ms"] = round((t_win - t_spawn) * 1000, 1)
    else:
        rec["errors"].append("window not seen on screen within 30 s")
    time.sleep(idle_s)
    helpers, rec["memory"], rec["cpu"] = measure_resources(proc.pid, before)
    proc.terminate()
    rec["lingering_helpers"] = stop(proc, helpers, graceful=False)
    time.sleep(1.0)
    return rec


# ---- build statistics ----

def build_stats():
    stats = {}
    for name, d in [("gpui-app", "gpui-app"), ("own-app", "own-app"), ("gpui-full", "gpui-full"),
                    ("own-full", "own-full"), ("tauri-app", "tauri-app")]:
        path = os.path.join(ROOT, d)
        subprocess.run(["cargo", "clean"], cwd=path, capture_output=True)
        t0 = time.perf_counter()
        r = subprocess.run(["cargo", "build", "--release", "--locked"], cwd=path,
                           capture_output=True, text=True)
        secs = time.perf_counter() - t0
        tree = subprocess.run(["cargo", "tree", "--prefix", "none", "--locked"], cwd=path,
                              capture_output=True, text=True).stdout
        tree_unique = len({l.replace(" (*)", "").strip() for l in tree.splitlines() if l.strip()})
        with open(os.path.join(path, "Cargo.lock")) as f:
            lock_pkgs = f.read().count("[[package]]")
        binary = os.path.join(path, "target", "release", d)
        stats[name] = {
            "clean_release_build_s": round(secs, 1),
            "build_ok": r.returncode == 0,
            "binary_bytes": os.path.getsize(binary) if os.path.exists(binary) else None,
            "cargo_tree_unique": tree_unique,
            "cargo_lock_packages": lock_pkgs,
            "target_dir_bytes": dir_size(os.path.join(path, "target")),
        }
    if os.path.exists(PODBAG_BIN):
        stats["podbag-desktop"] = {"binary_bytes": os.path.getsize(PODBAG_BIN),
                                   "target_dir_bytes": dir_size(PODBAG_TARGET)}
    return stats


def dir_size(path):
    total = 0
    for dirpath, _, files in os.walk(path):
        for f in files:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total


# ---- summary ----

METRICS = ["startup_ms", "ready_in_app_ms", "render_ms", "data_ms", "filter_ms"]


def summarize(runs):
    out = {}
    keys = sorted({(r["variant"], r["rows"]) for r in runs}, key=lambda k: (k[1], k[0]))
    for v, n in keys:
        group = [r for r in runs if r["variant"] == v and r["rows"] == n]
        warm = [r for r in group if not r["cold"] and not r.get("retried")]
        cold = [r for r in group if r["cold"]]
        s = {"warm_runs": len(warm), "failed_runs": sum(1 for r in warm if r["errors"]),
             "redone_runs": sum(1 for r in group if r.get("retried"))}
        for m in METRICS:
            vals = [r[m] for r in warm if r.get(m) is not None]
            if vals:
                s[m] = round(statistics.median(vals), 1)
                s[m + "_min"] = min(vals)
                s[m + "_max"] = max(vals)
        for key, path in [("mem_app_mb", ("memory", "app_bytes")),
                          ("mem_total_mb", ("memory", "total_bytes"))]:
            vals = [r[path[0]][path[1]] for r in warm if r.get(path[0]) and r[path[0]][path[1]]]
            if vals:
                s[key] = round(statistics.median(vals) / 1048576, 1)
        for key, path in [("cpu_app_pct", ("cpu", "app_pct")), ("cpu_total_pct", ("cpu", "total_pct"))]:
            vals = [r[path[0]][path[1]] for r in warm if r.get(path[0]) and r[path[0]][path[1]] is not None]
            if vals:
                s[key] = round(statistics.median(vals), 2)
        if cold and cold[0].get("startup_ms") is not None:
            s["first_run_startup_ms"] = cold[0]["startup_ms"]
        out[f"{v}@{n}"] = s
    return out


def print_table(summary):
    cols = ["startup_ms", "render_ms", "filter_ms", "mem_app_mb", "mem_total_mb",
            "cpu_total_pct", "first_run_startup_ms"]
    print("| variant@rows | " + " | ".join(cols) + " |")
    print("|---" * (len(cols) + 1) + "|")
    for k, s in summary.items():
        print(f"| {k} | " + " | ".join(str(s.get(c, "-")) for c in cols) + " |")


def tool_version(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True).stdout.strip().splitlines()[0]
    except (OSError, IndexError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", default="100,1000,10000")
    ap.add_argument("--runs", type=int, default=5, help="warm runs per variant and row count")
    ap.add_argument("--variants", default=",".join(VARIANTS))
    ap.add_argument("--build-stats", action="store_true")
    ap.add_argument("--podbag", action="store_true", help="also measure real Podbag Desktop")
    ap.add_argument("--podbag-runs", type=int, default=3)
    ap.add_argument("--no-bench", action="store_true", help="skip the prototype runs")
    ap.add_argument("--allow-locked", action="store_true",
                    help="run even when the screen is locked (frames are not drawn then)")
    ap.add_argument("--out", default=os.path.join(BENCH, "results.json"))
    args = ap.parse_args()

    if screen_locked() and not args.allow_locked:
        sys.exit("The screen is locked. Windows are occluded, so frames are not presented and "
                 "READY never comes for some variants. Unlock the screen, or pass --allow-locked.")

    results = {}
    if os.path.exists(args.out):
        with open(args.out) as f:
            results = json.load(f)
    results["meta"] = {
        "date": datetime.datetime.now().isoformat(timespec="seconds"),
        "machine": platform.machine(),
        "macos": platform.mac_ver()[0],
        "rustc": tool_version(["rustc", "--version"]),
        "memory_tool": "footprint (phys_footprint)",
        "cpu_tool": "ps cumulative cpu time over the window",
        "idle_before_memory_s": IDLE_BEFORE_MEM_S,
        "cpu_window_s": CPU_WINDOW_S,
        "filter_query": FILTER_QUERY,
        "screen_locked_at_start": screen_locked(),
    }

    if args.build_stats:
        print("clean release builds ...", flush=True)
        results["build"] = build_stats()
        print(json.dumps(results["build"], indent=2), flush=True)

    if not args.no_bench:
        rows = [int(x) for x in args.rows.split(",")]
        variants = args.variants.split(",")
        runs = []
        for n in rows:
            for v in variants:  # first launch of each variant at this row count
                print(f"{v} rows={n} first", flush=True)
                runs.append(one_run(v, n, 0, True))
            for k in range(1, args.runs + 1):  # warm runs, round robin
                for v in variants:
                    r = one_run(v, n, k, False)
                    for _ in range(RETRIES):  # failed runs are kept and redone
                        if not r["errors"]:
                            break
                        r["retried"] = True
                        runs.append(r)
                        r = one_run(v, n, k, False)
                    print(f"{v} rows={n} run={k} startup={r.get('startup_ms')} "
                          f"filter={r.get('filter_ms')} errors={r['errors']}", flush=True)
                    runs.append(r)
        results["runs"] = runs
        results["summary"] = summarize(runs)
        print_table(results["summary"])

    if args.podbag:
        ref = []
        for i in range(args.podbag_runs):
            if os.path.exists(PODBAG_BIN):
                ref.append(window_run([PODBAG_BIN], "podbag-desktop"))
            for v in VARIANTS:
                ref.append(window_run(VARIANTS[v](1000), f"{v}@1000", idle_s=3.0))
        results["podbag_reference"] = ref
        for r in ref:
            m = r.get("memory") or {}
            print(r["label"], r.get("window_ms"), m.get("app_bytes"), m.get("total_bytes"),
                  (r.get("cpu") or {}).get("total_pct"), r["errors"], flush=True)

    with open(args.out, "w") as f:
        json.dump(results, f, indent=2)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
