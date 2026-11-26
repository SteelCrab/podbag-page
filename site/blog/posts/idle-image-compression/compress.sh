#!/usr/bin/env bash
# Image compression (image_compression = "idle"): how much it saves, how long compressing
# takes, how much the first start of a compressed image is delayed, and that an image that
# is not compressed starts as fast with the feature on as with it off.
#
# Run as root (composefs, drop_caches), for example in the podbag-dev VM:
#   limactl shell podbag-dev -- sudo bash "$PWD/dev/bench/compress.sh"
# The store must be on a disk with room for about 2 GiB (not tmpfs, and on a file system
# that overlay and composefs accept).
#
# usage: dev/bench/compress.sh [work-dir]
#   work-dir  where the store goes, default /var/tmp/podbag-compress-bench (deleted first)
#   PODBAG_BIN       the program to measure, default target/linux/release/podbag in the
#                    repository, else the one in PATH
#   BENCH_RUNTIME    runtime directory, default /run/podbag-compress-bench
#   BENCH_ROUNDS     rounds of the first-run test, default 5
#   BENCH_WARM       alpine starts per setting, default 30
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
work="${1:-/var/tmp/podbag-compress-bench}"
runtime="${BENCH_RUNTIME:-/run/podbag-compress-bench}"
rounds="${BENCH_ROUNDS:-5}"
warm_runs="${BENCH_WARM:-30}"
if [ -n "${PODBAG_BIN:-}" ]; then
  pb="$PODBAG_BIN"
elif [ -x "$here/../../target/linux/release/podbag" ]; then
  pb="$here/../../target/linux/release/podbag"
else
  pb="$(command -v podbag)"
fi
pb="$(cd "$(dirname "$pb")" && pwd)/$(basename "$pb")"
[ "$(id -u)" -eq 0 ] || { echo "run as root" >&2; exit 2; }
# These paths are unmounted and deleted: refuse the ones that would do harm.
work="${work%/}"
runtime="${runtime%/}"
case "$work" in "" | / | /run | /var | /var/tmp | /tmp | /home | /root) echo "bad work dir: '$work'" >&2; exit 2 ;; esac
case "$runtime" in "" | / | /run | /var | /tmp) echo "bad BENCH_RUNTIME: '$runtime'" >&2; exit 2 ;; esac

py=python:3.12.8-slim-bookworm
java=eclipse-temurin:21.0.6_7-jre-noble
alpine=alpine:3.22
images="python:3.12.7-slim-bookworm $py eclipse-temurin:21.0.5_11-jre-noble $java $alpine"

export PODBAG_DATA_DIR="$work/data" PODBAG_RUNTIME_DIR="$runtime" PODBAG_CONFIG_DIR="$work/config"
unset PODBAG_IMAGE_COMPRESSION PODBAG_COMPRESS_IDLE_AFTER

median() { sort -n | awk '{a[NR]=$1} END {print (NR%2) ? a[(NR+1)/2] : (a[NR/2]+a[NR/2+1])/2}'; }
# ms COMMAND...: milliseconds the command takes
# A failing command stops the script: a failed run must not give a plausible number.
ms() {
  local t0 t1
  t0=$(date +%s%N)
  "$@" > /dev/null 2>&1 || { echo "command failed: $*" >&2; exit 1; }
  t1=$(date +%s%N)
  echo $(((t1 - t0) / 1000000))
}
# row NAME: the SIZE column of a `system df` row
row() { "$pb" system df | awk -v n="$1" '$1 == n { $1 = ""; $2 = ""; sub(/^ +/, ""); print }'; }
cold() { sync; echo 3 > /proc/sys/vm/drop_caches; }
# Image mounts of the earlier store (or of this one) keep its files in use.
unmount_images() {
  findmnt -rn -o TARGET | grep "^$runtime/" | sort -r | xargs -r -n1 umount -l || true
}
# Stop the processes of this run only: this program, with this run's runtime dir in its
# environment (a keeper or a shim of the run). Other podbag processes stay.
stop_own_processes() {
  local env pid exe real
  real=$(readlink -f "$pb")
  for env in /proc/[0-9]*/environ; do
    pid=${env#/proc/}
    pid=${pid%/environ}
    [ "$pid" != "$$" ] || continue
    exe=$(readlink -f "/proc/$pid/exe" 2> /dev/null) || continue
    [ "$exe" = "$real" ] || continue
    if tr '\0' '\n' < "$env" 2> /dev/null | grep -qxF "PODBAG_RUNTIME_DIR=$runtime"; then
      kill "$pid" 2> /dev/null || true
    fi
  done
}
cleanup() {
  stop_own_processes
  sleep 1
  unmount_images
}
trap cleanup EXIT

unmount_images
rm -rf "$work"
mkdir -p "$work"
echo "kernel $(uname -r), $("$pb" --version), $(nproc) CPUs"
echo "store: $work (image_compression is off while pulling)"

for i in $images; do "$pb" pull "$i" > /dev/null 2>&1; done
"$pb" images
echo
echo "== size (Objects row of system df)"
echo "before: $(row Objects)"

# Idle for 0 seconds: every image counts as idle, so one command compresses them all.
echo
echo "== time podbag system compress"
t0=$(date +%s%N)
PODBAG_COMPRESS_IDLE_AFTER=0 "$pb" system compress > /dev/null
echo "compress_ms=$((($(date +%s%N) - t0) / 1000000))"
echo "after:  $(row Objects)"
echo "Compressed row: $(row Compressed)"

echo
echo "== first run of a compressed image (median of $rounds, caches dropped)"
for name in "$py" "$java"; do
  case "$name" in
    python*) cmd=(python3 -c pass) ;;
    *) cmd=(java -version) ;;
  esac
  first=$(for _ in $(seq "$rounds"); do
    "$pb" system compress "$name" > /dev/null
    cold
    ms "$pb" run --rm --network none "$name" "${cmd[@]}"
  done | median)
  # The image is not compressed now: the same start with cold caches, without decompressing.
  next=$(for _ in $(seq "$rounds"); do cold; ms "$pb" run --rm --network none "$name" "${cmd[@]}"; done | median)
  echo "$name: first_run_ms=$first plain_run_ms=$next"
done

echo
echo "== alpine start, $warm_runs runs each, off and idle alternating (median)"
"$pb" run --rm --network none "$alpine" true > /dev/null
off=() idle=()
for _ in $(seq "$warm_runs"); do
  t=$(PODBAG_IMAGE_COMPRESSION=off ms "$pb" run --rm --network none "$alpine" true)
  off+=("$t")
  t=$(PODBAG_IMAGE_COMPRESSION=idle ms "$pb" run --rm --network none "$alpine" true)
  idle+=("$t")
done
off_ms=$(printf '%s\n' "${off[@]}" | median)
idle_ms=$(printf '%s\n' "${idle[@]}" | median)
echo "alpine_off_ms=$off_ms alpine_idle_ms=$idle_ms"
