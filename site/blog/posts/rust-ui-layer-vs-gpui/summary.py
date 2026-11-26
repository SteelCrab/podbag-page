#!/usr/bin/env python3
"""Summarize results.json with only the processes that belong to each app.

    python3 bench/summary.py bench/results.json [more.json ...]

run.py finds helper processes by diffing the process list, so anything that starts during a
run is caught too (for example another virtual machine). Here a run counts the app process
and WebKit's XPC services (com.apple.WebKit.*). Other new processes are listed apart.
Memory is phys_footprint in MiB; CPU is the idle average over the 10 s window.
"""

import json
import statistics
import sys

MIB = 1024 * 1024


def owned(name, variant):
    app = {"gpui": "gpui-app", "own": "own-app", "gpui-full": "gpui-full", "own-full": "own-full"}.get(variant, "tauri-app")
    return name == app or name.startswith("com.apple.WebKit.")


def main():
    runs = []
    for path in sys.argv[1:]:
        runs += json.load(open(path))["runs"]
    groups, others = {}, {}
    for r in runs:
        if r.get("cold") or r.get("errors"):
            continue
        key = (r["variant"], r["rows"])
        g = groups.setdefault(key, {k: [] for k in ("startup", "render", "filter", "app", "mem", "cpu")})
        procs = r["memory"]["processes"]
        g["startup"].append(r["startup_ms"])
        g["render"].append(r["render_ms"])
        g["filter"].append(r["filter_ms"])
        g["app"].append(sum(p["bytes"] for p in procs if not p["name"].startswith("com.apple.")) / MIB)
        g["mem"].append(sum(p["bytes"] for p in procs if owned(p["name"], r["variant"])) / MIB)
        g["cpu"].append(sum(p["pct"] for p in r["cpu"]["processes"] if owned(p["name"], r["variant"])))
        for p in procs:
            if not owned(p["name"], r["variant"]):
                others.setdefault(p["name"], set()).add(r["variant"])
    print("| variant@rows | n | startup ms | render ms | filter ms | app MiB | app+WebKit MiB | idle CPU % |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    for (variant, rows), g in sorted(groups.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        med = {k: statistics.median(v) for k, v in g.items()}
        print(f"| {variant}@{rows} | {len(g['startup'])} | {med['startup']:.0f} | {med['render']:.0f} | "
              f"{med['filter']:.0f} | {med['app']:.1f} | {med['mem']:.1f} | {med['cpu']:.2f} |")
    print("\nnot counted:", {k: sorted(v) for k, v in sorted(others.items())})


if __name__ == "__main__":
    main()
