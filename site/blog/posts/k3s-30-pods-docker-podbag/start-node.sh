#!/usr/bin/env bash
set -euo pipefail
rt=${1:?docker or podbag}
[[ $rt == docker || $rt == podbag ]]
block=${2:?measurement block}
data=/var/lib/bench-controlled-$rt-$block
mkdir -p /run/bench-binaries /var/lib/rancher/k3s "$data"
mountpoint -q /run/bench-binaries || mount -t tmpfs -o size=750M,mode=755 tmpfs /run/bench-binaries
for dir in /var/lib/rancher/k3s "$data"; do
  if [[ ! -e "$dir/data" ]]; then ln -sfn /run/bench-binaries "$dir/data"; fi
done
args=(--write-kubeconfig /etc/rancher/k3s/k3s.yaml --data-dir "$data" --disable traefik,servicelb,metrics-server,local-storage
      --kubelet-arg cgroup-driver=cgroupfs --node-name bench)
mkdir -p /etc/rancher/k3s
case $rt in
  docker)
    systemctl start docker
    docker info --format '{{.CgroupDriver}}' | grep -Fx cgroupfs
    args+=(--docker)
    ;;
  podbag)
    pb=/var/lib/pb30-controlled-$block
    mkdir -p "$pb" /var/lib/pb30/store /run/pb30 "$data/agent/etc/cni/net.d"
    ln -sfn /var/lib/pb30/store "$pb/store"
    systemd-run --unit=bench-cri -p Delegate=yes --setenv=PODBAG_RUNTIME_DIR=/run/pb30 --setenv=PODBAG_DATA_DIR="$pb" \
      /usr/local/bin/podbag cri serve --socket /run/pb30/cri.sock \
      --cni-conf-dir "$data/agent/etc/cni/net.d" --cni-bin-dir "$data/data/cni:$data/data/current/bin" --cgroup-driver cgroupfs
    args+=(--container-runtime-endpoint unix:///run/pb30/cri.sock)
    ;;
esac
systemd-run --unit=bench-k3s -p Delegate=yes -p KillMode=process /usr/local/bin/k3s server "${args[@]}"
k() { k3s kubectl "$@"; }
for i in $(seq 150); do
  systemctl is-active --quiet bench-k3s || { journalctl -u bench-k3s -n 5; exit 1; }
  if k -n kube-system get deploy coredns >/dev/null 2>&1; then break; fi
  sleep 1
done
k wait --for=condition=ready node/bench --timeout=120s
k -n kube-system rollout status deploy/coredns --timeout=240s
k get ns shop-bench >/dev/null 2>&1 || k create ns shop-bench
systemd-run --unit=bench-kproxy /usr/local/bin/k3s kubectl proxy --port=8001
for i in $(seq 20); do curl -fsS http://127.0.0.1:8001/version >/dev/null && break; sleep 1; done
k get node bench -o jsonpath='{.status.nodeInfo.containerRuntimeVersion}{"\n"}'
