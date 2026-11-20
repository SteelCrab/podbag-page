---
title: "podbag 0.1.0: containers with no daemon, stored file by file"
date: 2026-11-20
author: team
categories: [announcements]
tags: [release, docker, compose, rootless, macos, windows]
summary: "The first release of podbag is out. One static binary runs Docker and OCI containers with no daemon, and stores images file by file: less disk, less memory, and a start in about 4 ms."
image: card-en.png
image_alt: "podbag 0.1.0: containers with no daemon, stored file by file"
draft: false
---

Today we release podbag 0.1.0, the first version of podbag.

podbag is a container engine. It runs your Docker and OCI images from one static binary. It has no daemon. It stores images file by file, not layer by layer.

Short on time? Watch the [30-second intro](/media/intro.mp4).

## What podbag is

- **No daemon.** When no container runs, nothing runs.
- **One static binary.** About 4 MB on Linux.
- **Files, not layers.** A file that many images share is stored once and cached once.
- **Fast.** A container starts in about 4 ms on Linux.
- **Works with Docker tools.** The `docker` CLI, Compose and buildx.
- **With or without root.** The same program works both ways.
- **Linux, macOS and Windows.** Windows support is experimental.

## No daemon

Docker is a client and two daemons. `dockerd` and `containerd` run all the time, with or without containers. With no containers, they still hold {{n:203}} MiB.

podbag is one program:

- The `podbag` command sets up each container itself, and then returns.
- One small keeper per user (about 2 MiB) watches the running containers. It writes their logs, and answers `stop`, `kill` and `wait`.
- The keeper starts with the first container. It stops 10 seconds after the last one.
- With no container, nothing runs.

## Files, not layers

![Two images share most of their files. As layers, image B's top layer differs by one file, so its shared files are stored again: 8 files. podbag stores each file once: 6 files.](/images/storage-light.svg "Layers against files: one changed file makes a layer store keep the whole layer again.")

Other engines store an image as layers. A layer is kept once only when the whole layer is the same. When one file in it changes, the whole layer is stored again.

podbag splits each layer into files, and keeps each file once. An image is a list of paths to these files. When two containers read the same file, they read the same inode, so the kernel caches it once.

We measured 8 Spring services in 2 releases:

<!-- compare-columns: podbag docker -->
| | podbag | Docker | podbag saves |
|---|--:|--:|--:|
| Disk for both releases | {{n:902}} MiB | {{n:2970}} MiB | 70% |
| Page cache to start their 16 services | {{n:324}} MiB | {{n:982}} MiB | 67% |

Downloads stay the same size. Registries serve layers, and podbag downloads them whole before it splits them into files.

## Start time and memory

![How podbag compares with Docker, Podman and Kiri on one Linux VM: start time, memory for 100 containers, memory with no containers, disk and page cache.](/images/perf.svg "podbag against Docker, Podman and Kiri, as an animation.")

We ran every tool on the same Linux VM: 4 CPUs, {{n:3.8}} GiB, arm64. The versions: podbag 0.1.0, Podman 5.7.0, Docker 29.1.3 and Kiri 0.2.1. The numbers are medians. Lower is better.

<!-- compare-columns: podbag podbag kiri podman docker -->
| | podbag (rootless) | podbag (root) | Kiri | Podman | Docker |
|---|--:|--:|--:|--:|--:|
| Start a container | {{n:4.1}} ms | {{n:4.4}} ms | {{n:9.1}} ms | {{n:46.4}} ms | {{n:73.8}} ms |
| Memory for 100 containers | {{n:117}} MiB | {{n:105}} MiB | {{n:109}} MiB | {{n:203}} MiB | {{n:562}} MiB |
| Processes with no containers | {{n:0}} | {{n:0}} | {{n:1}} ({{n:5.9}} MiB) | {{n:1}} ({{n:0.6}} MiB) | {{n:4}} ({{n:203}} MiB) |

- The first start, when no keeper runs yet, takes {{n:12.8}}–{{n:16.0}} ms.
- Kiri is close on memory. podbag is ahead when no container runs, because then nothing of it runs.
- All numbers, and how we measured them: [benchmarks](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks.md) and the [Spring microservices benchmark](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks-msa.md).
- The same comparison as a video: [perf.mp4](/media/perf.mp4).

## Works with your Docker tools

`podbag system service` serves the Docker Engine API on a socket. The `docker` CLI, Compose and buildx talk to it.

```sh
podbag system service &
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podbag/docker.sock
docker compose up -d
```

- It is not a daemon. Containers do not depend on it.
- It stops after 60 seconds without a client.
- With systemd, it can start on the first connection.

## With or without root

- The same program works both ways.
- As root, podbag mounts images with composefs.
- Without root, it makes trees of hard links, and `pasta` connects the containers to the network.
- `podbag check` lists what your system still needs, and how to add it.

## Linux, macOS and Windows

- **Linux:** x86_64 and arm64. Linux 5.12 or later, with cgroup v2.
- **macOS** (Apple silicon): podbag runs a small Linux VM of its own. The first command starts it in about half a second. The VM powers off 60 seconds after the last container. Six minutes after the last container, podbag held {{n:1.7}} MiB of the Mac's memory.
- **Windows** (x86_64 and arm64): experimental. podbag runs its Linux engine in a WSL 2 distribution of its own. It is built and tested in CI, but not yet tried on a Windows machine.

## Install

On Linux and macOS:

```sh
curl -fsSL https://podbag.dev/install.sh | sh
```

The script downloads the file for your system, checks its SHA-256 sum, and installs it in `/usr/local/bin`.

You can also get a file from the [release page](https://github.com/SteelCrab/podbag/releases/tag/v0.1.0). Check it with `SHA256SUMS`.

| System | File |
|---|---|
| Linux, x86_64 | `podbag-x86_64-linux` |
| Linux, arm64 | `podbag-aarch64-linux` |
| macOS, Apple silicon | `podbag-aarch64-macos` |
| Windows, x86_64 (experimental) | `podbag-x86_64-windows.exe` |
| Windows, arm64 (experimental) | `podbag-aarch64-windows.exe` |

Then run your first container:

```sh
podbag run --rm alpine echo hello
```

## The limits of 0.1.0

This is a first release. Some things are not there yet:

- **Builds:** Dockerfiles build only through buildx (`docker buildx build`). There is no classic builder.
- **Registries:** podbag pulls public images. There are no logins, no private pulls and no push.
- **Docker commands:** no `commit`, `export`, `diff`, `stats`, `top`, `pause`, `rename` or `update`.
- **Swarm:** no swarm mode, and no plugins.
- **Kubernetes:** there is no CRI, so a Kubernetes node cannot use podbag as its runtime.
- **Windows:** experimental. The `docker` CLI on Windows cannot reach podbag yet.
- **Mac wake-up:** the first command after the VM powered off takes about {{n:0.6}} s.

## What comes next

Work on these is in [open pull requests](https://github.com/SteelCrab/podbag/pulls). It is not finished, and we give no dates:

- registry logins, private pulls, push and search;
- Dockerfile builds, and `commit`, `export` and `diff`;
- a Kubernetes runtime, so a node can run its pods with podbag;
- swarm mode on one node;
- `stats`, `top`, `pause`, `unpause`, `rename` and `update`;
- a terminal UI and a desktop app.

## Try it and tell us

- Read the [usage guide](https://github.com/SteelCrab/podbag/blob/main/docs/usage.md) for all commands.
- Report bugs and ideas in [GitHub issues](https://github.com/SteelCrab/podbag/issues). Reports from Windows machines help most.
- podbag is open source, under the Apache License 2.0.
