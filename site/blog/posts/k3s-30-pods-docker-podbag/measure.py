"""Measure one warm-up and two rounds in a dedicated, rootful, single-node k3s VM.

Start 'k3s kubectl proxy --port=8001' on loopback in the VM first.
Run beside workload.json. Uses the shop-bench namespace exclusively.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from http.client import HTTPConnection, HTTPException
import json
from math import ceil
from pathlib import Path
import statistics
import subprocess
import time
from urllib.request import Request, urlopen

NAMESPACE = "shop-bench"
CLIENTS = 12
PER_CLIENT = 100
BASE = "http://127.0.0.1:8001"
CORE = f"/api/v1/namespaces/{NAMESPACE}"
APPS = f"/apis/apps/v1/namespaces/{NAMESPACE}/deployments"
HERE = Path(__file__).resolve().parent


def api(path, patch=None):
    request = Request(BASE + path)
    if patch is not None:
        request = Request(BASE + path, method="PATCH", data=json.dumps(patch).encode(),
                          headers={"Content-Type": "application/merge-patch+json"})
    with urlopen(request, timeout=10) as response:
        return json.load(response)


def wait_until(check, timeout=180):
    deadline = time.monotonic() + timeout
    while not check():
        if time.monotonic() >= deadline:
            raise TimeoutError(check.__name__)
        time.sleep(0.1)


def scale(api_count, web_count):
    for name, count in [("api", api_count), ("web", web_count)]:
        api(f"{APPS}/{name}/scale", {"spec": {"replicas": count}})


def ready():
    counts = {}
    for deployment in api(APPS)["items"]:
        status = deployment["status"]
        counts[deployment["metadata"]["name"]] = status.get("readyReplicas", 0)
    return counts == {"web": 6, "api": 24}


def endpoint_counts():
    counts = {}
    for role in ("api", "web"):
        slices = api(f"/apis/discovery.k8s.io/v1/namespaces/{NAMESPACE}/endpointslices"
                     f"?labelSelector=kubernetes.io%2Fservice-name%3D{role}")
        counts[role] = sum(ep["conditions"].get("ready") is True for s in slices["items"]
                           for ep in s["endpoints"])
    return counts == {"api": 24, "web": 6}


def client(host, count, interval):
    samples = []
    first = time.perf_counter()
    for i in range(count):
        if interval:
            time.sleep(max(0, first + i * interval - time.perf_counter()))
        connection = HTTPConnection(host, 8080, timeout=3)
        start = time.perf_counter()
        try:
            connection.request("GET", "/api", headers={"Connection": "close"})
            response = connection.getresponse()
            backend = response.read().decode().strip()
            ok = response.status == 200 and backend.startswith("api-")
        except (HTTPException, OSError, ValueError) as error:
            backend, ok = type(error).__name__, False
        finally:
            connection.close()
        samples.append(((time.perf_counter() - start) * 1000, backend, ok))
    return samples


def round_once(host):
    scale(0, 0)
    wait_until(lambda: not api(CORE + "/pods")["items"])
    start = time.perf_counter()
    scale(24, 6)
    wait_until(ready)
    ready_s = time.perf_counter() - start
    wait_until(endpoint_counts)
    # Allow node service rules to settle before sending traffic. Outside both timers.
    time.sleep(2)
    burst = load(host, PER_CLIENT, 0)
    time.sleep(2)
    steady = load(host, 600, 0.05)
    return {"ready_s": round(ready_s, 4), "burst": burst, "steady": steady}


def load(host, count, interval):
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=CLIENTS) as pool:
        futures = [pool.submit(client, host, count, interval) for _ in range(CLIENTS)]
        samples = [sample for future in futures for sample in future.result()]
    elapsed = time.perf_counter() - start
    good = sorted(ms for ms, _, ok in samples if ok)
    return {
        "success": len(good), "requests": len(samples),
        "backends": len({name for _, name, ok in samples if ok}),
        "load_s": round(elapsed, 4), "successful_rps": round(len(good) / elapsed, 2),
        "p50_ms": round(statistics.median(good), 3) if good else None,
        "p95_ms": round(good[ceil(len(good) * 0.95) - 1], 3) if good else None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runtime", choices=("docker", "podbag"))
    parser.add_argument("block", type=int)
    args = parser.parse_args()
    documents = json.loads((HERE / "workload.json").read_text())
    for item in documents["items"]:
        if item["kind"] == "Deployment":
            item["spec"]["replicas"] = 0
    subprocess.run(["k3s", "kubectl", "apply", "-f", "-"], input=json.dumps(documents),
                   text=True, check=True, stdout=subprocess.DEVNULL)
    host = api(CORE + "/services/web")["spec"]["clusterIP"]
    for index in range(3):
        result = round_once(host)
        result.update(runtime=args.runtime, block=args.block, run=index, warmup=index == 0)
        print(json.dumps(result), flush=True)
        if any(result[phase]["success"] != result[phase]["requests"] for phase in ("burst", "steady")):
            raise RuntimeError("HTTP response validation failed")
    scale(0, 0)
    wait_until(lambda: not api(CORE + "/pods")["items"])


if __name__ == "__main__":
    main()
