---
title: "podbag 0.1.0：没有守护进程、按文件存储的容器"
date: 2026-11-20
author: team
categories: [announcements]
tags: [release, docker, compose, rootless, macos, windows]
summary: "podbag 的第一个版本发布了。一个静态二进制文件，不用守护进程就能运行 Docker 和 OCI 容器，并按文件存储镜像：磁盘更少，内存更少，容器约 4 ms 启动。"
image: card-zh-CN.png
image_alt: "podbag 0.1.0：没有守护进程、按文件存储的容器"
draft: false
---

今天我们发布 podbag 0.1.0，这是 podbag 的第一个版本。

podbag 是一个容器引擎。它用一个静态二进制文件运行 Docker 和 OCI 镜像。它没有守护进程。它按文件存储镜像，而不是按层。

时间不多？看看 [30 秒介绍视频](/media/intro.mp4)（英文）。

## podbag 是什么

- **没有守护进程。** 没有容器运行时，什么也不运行。
- **一个静态二进制文件。** 在 Linux 上约 4 MB。
- **按文件，不按层。** 许多镜像共用的文件只存一份、只缓存一次。
- **快。** 在 Linux 上，容器约 4 ms 启动。
- **兼容 Docker 工具。** 支持 `docker` CLI、Compose 和 buildx。
- **有没有 root 都行。** 同一个程序两种方式都能用。
- **Linux、macOS、Windows。** Windows 支持仍是实验性的。

## 没有守护进程

Docker 由一个客户端和两个守护进程组成。不管有没有容器，`dockerd` 和 `containerd` 一直在运行。没有容器时，它们仍占用 {{n:203}} MiB。

podbag 只是一个程序：

- `podbag` 命令自己创建每个容器，然后就退出。
- 每个用户有一个小小的 keeper（约 2 MiB），看管正在运行的容器。它写日志，并响应 `stop`、`kill` 和 `wait`。
- keeper 随第一个容器启动，在最后一个容器结束 10 秒后退出。
- 没有容器时，什么也不运行。

## 按文件，不按层

![两个镜像共用大部分文件。按层存储时，镜像 B 最上面的层只差一个文件，共用的文件也要再存一次，共 8 个文件。podbag 每个文件只存一份，共 6 个文件。](/images/storage-zh-CN-light.svg "层与文件：只要一个文件变了，按层存储就要把整层再存一次。")

其他引擎按层存储镜像。只有整层完全相同时，层才只存一份。层里只要有一个文件变了，整层就要再存一次。

podbag 把每个层拆成文件，每个文件只存一份。镜像是指向这些文件的路径列表。两个容器读同一个文件时，读的是同一个 inode，所以内核只缓存一次。

我们用 8 个 Spring 服务、2 个版本做了测量：

<!-- compare-columns: podbag docker -->
| | podbag | Docker | podbag 节省 |
|---|--:|--:|--:|
| 两个版本的磁盘 | {{n:902}} MiB | {{n:2970}} MiB | 70% |
| 启动 16 个服务的页缓存 | {{n:324}} MiB | {{n:982}} MiB | 67% |

下载量不变。镜像仓库按层提供，podbag 先完整下载每个层，再拆成文件。

## 启动时间和内存

![在一台 Linux 虚拟机上比较 podbag 与 Docker、Podman 和 Kiri：启动时间、100 个容器的内存、没有容器时的内存、磁盘和页缓存。](/images/perf.svg "podbag 与 Docker、Podman 和 Kiri 的比较动画（英文）。")

所有工具都在同一台 Linux 虚拟机上运行：4 个 CPU、{{n:3.8}} GiB、arm64。版本为 podbag 0.1.0、Podman 5.7.0、Docker 29.1.3 和 Kiri 0.2.1。数字是中位数。越低越好。

<!-- compare-columns: podbag podbag kiri podman docker -->
| | podbag (rootless) | podbag (root) | Kiri | Podman | Docker |
|---|--:|--:|--:|--:|--:|
| 启动一个容器 | {{n:4.1}} ms | {{n:4.4}} ms | {{n:9.1}} ms | {{n:46.4}} ms | {{n:73.8}} ms |
| 100 个容器的内存 | {{n:117}} MiB | {{n:105}} MiB | {{n:109}} MiB | {{n:203}} MiB | {{n:562}} MiB |
| 没有容器时的进程 | {{n:0}} | {{n:0}} | {{n:1}} 个（{{n:5.9}} MiB） | {{n:1}} 个（{{n:0.6}} MiB） | {{n:4}} 个（{{n:203}} MiB） |

- 还没有 keeper 时，第一次启动需要 {{n:12.8}}–{{n:16.0}} ms。
- 内存方面，Kiri 和 podbag 接近。没有容器时 podbag 领先，因为那时 podbag 什么也不运行。
- 全部数字和测量方法：[基准测试](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks.md)和 [Spring 微服务基准测试](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks-msa.md)（英文）。
- 同样的比较，视频版：[perf.mp4](/media/perf.mp4)（英文）。

## 兼容 Docker 工具

`podbag system service` 在一个套接字上提供 Docker Engine API。`docker` CLI、Compose 和 buildx 通过它使用 podbag。

```sh
podbag system service &
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podbag/docker.sock
docker compose up -d
```

- 它不是守护进程。容器不依赖它。
- 60 秒没有客户端连接，它就退出。
- 有 systemd 时，它可以在第一次连接时启动。

## 有没有 root 都行

- 同一个程序两种方式都能用。
- 有 root 时，podbag 用 composefs 挂载镜像。
- 没有 root 时，它建立硬链接树，并由 `pasta` 把容器接入网络。
- `podbag check` 列出系统还缺什么，以及怎么补上。

## Linux、macOS、Windows

- **Linux：** x86_64 和 arm64。需要 Linux 5.12 或更高版本，以及 cgroup v2。
- **macOS**（Apple 芯片）：podbag 运行一个自己的小型 Linux 虚拟机。第一条命令约 0.5 秒就能启动它。最后一个容器结束 60 秒后，虚拟机关机。最后一个容器结束 6 分钟后，podbag 只占用 Mac {{n:1.7}} MiB 内存。
- **Windows**（x86_64、arm64）：实验性。podbag 在自己的 WSL 2 发行版里运行 Linux 引擎。它在 CI 中构建和测试，但还没在真正的 Windows 电脑上试过。

## 安装

Linux 和 macOS：

```sh
curl -fsSL https://podbag.dev/install.sh | sh
```

脚本会下载适合你系统的文件，检查 SHA-256 校验和，并安装到 `/usr/local/bin`。

也可以从[发布页面](https://github.com/SteelCrab/podbag/releases/tag/v0.1.0)下载文件，并用 `SHA256SUMS` 校验。

| 系统 | 文件 |
|---|---|
| Linux，x86_64 | `podbag-x86_64-linux` |
| Linux，arm64 | `podbag-aarch64-linux` |
| macOS，Apple 芯片 | `podbag-aarch64-macos` |
| Windows，x86_64（实验性） | `podbag-x86_64-windows.exe` |
| Windows，arm64（实验性） | `podbag-aarch64-windows.exe` |

然后运行你的第一个容器：

```sh
podbag run --rm alpine echo hello
```

## 0.1.0 的限制

这是第一个版本，有些功能还没有：

- **构建：** Dockerfile 只能通过 buildx（`docker buildx build`）构建。没有经典构建器。
- **镜像仓库：** 只能拉取公开镜像。没有登录、私有拉取和推送。
- **Docker 命令：** 没有 `commit`、`export`、`diff`、`stats`、`top`、`pause`、`rename` 和 `update`。
- **Swarm：** 没有 swarm 模式，也没有插件。
- **Kubernetes：** 没有 CRI，所以 Kubernetes 节点不能把 podbag 当作运行时。
- **Windows：** 实验性。Windows 上的 `docker` CLI 还连不上 podbag。
- **Mac 唤醒：** 虚拟机关机后的第一条命令约需 {{n:0.6}} 秒。

## 接下来

下面这些工作在[开放的拉取请求](https://github.com/SteelCrab/podbag/pulls)中进行。它们还没有完成，我们不给日期：

- 镜像仓库登录、私有拉取、推送和搜索
- Dockerfile 构建，以及 `commit`、`export` 和 `diff`
- Kubernetes 运行时，让节点用 podbag 运行 Pod
- 单节点 swarm 模式
- `stats`、`top`、`pause`、`unpause`、`rename` 和 `update`
- 终端界面和桌面应用

## 试一试，告诉我们

- 全部命令见[使用指南](https://github.com/SteelCrab/podbag/blob/main/docs/usage.md)（英文）。
- 问题和想法请提交到 [GitHub 问题反馈](https://github.com/SteelCrab/podbag/issues)。在 Windows 电脑上的试用结果最有帮助。
- podbag 是开源软件，采用 Apache License 2.0。
