---
title: "podbag 0.1.0: 데몬 없이, 파일 단위로 저장하는 컨테이너"
date: 2026-11-20
author: team
categories: [announcements]
tags: [release, docker, compose, rootless, macos, windows]
summary: "podbag의 첫 릴리스가 나왔습니다. 정적 바이너리 하나로 Docker와 OCI 컨테이너를 데몬 없이 실행하고, 이미지를 파일 단위로 저장합니다. 디스크와 메모리를 덜 쓰고, 컨테이너는 약 4 ms에 시작합니다."
image: card-ko.png
image_alt: "podbag 0.1.0: 데몬 없이, 파일 단위로 저장하는 컨테이너"
draft: false
---

오늘 podbag의 첫 버전인 podbag 0.1.0을 릴리스합니다.

podbag은 컨테이너 엔진입니다. 정적 바이너리 하나로 Docker와 OCI 이미지를 실행합니다. 데몬이 없습니다. 이미지를 레이어 단위가 아니라 파일 단위로 저장합니다.

시간이 없다면 [30초 소개 영상](/media/intro.mp4)(영어)을 보세요.

## podbag은 무엇인가

- **데몬 없음.** 실행 중인 컨테이너가 없으면 아무것도 실행되지 않습니다.
- **정적 바이너리 하나.** Linux에서 약 4 MB입니다.
- **레이어 대신 파일.** 여러 이미지가 함께 쓰는 파일은 한 번만 저장하고 한 번만 캐시합니다.
- **빠름.** Linux에서 컨테이너가 약 4 ms에 시작합니다.
- **Docker 도구와 함께 동작.** `docker` CLI, Compose, buildx를 지원합니다.
- **root 유무와 상관없이.** 같은 프로그램이 두 방식 모두로 동작합니다.
- **Linux, macOS, Windows.** Windows 지원은 실험 기능입니다.

## 데몬 없음

Docker는 클라이언트 하나와 데몬 두 개로 이루어집니다. `dockerd`와 `containerd`는 컨테이너가 있든 없든 항상 실행됩니다. 컨테이너가 없어도 {{n:203}} MiB를 차지합니다.

podbag은 프로그램 하나입니다.

- `podbag` 명령이 컨테이너를 직접 설정하고 바로 끝납니다.
- 사용자마다 작은 keeper 하나(약 2 MiB)가 실행 중인 컨테이너를 지켜봅니다. 로그를 쓰고, `stop`, `kill`, `wait`에 응답합니다.
- keeper는 첫 컨테이너와 함께 시작합니다. 마지막 컨테이너가 끝나고 10초 뒤에 멈춥니다.
- 컨테이너가 없으면 아무것도 실행되지 않습니다.

## 레이어 대신 파일

![두 이미지가 대부분의 파일을 함께 씁니다. 레이어 방식에서는 이미지 B의 맨 위 레이어가 파일 하나만 달라도, 함께 쓰던 파일까지 다시 저장되어 파일이 8개가 됩니다. podbag은 파일마다 한 번만 저장해서 6개입니다.](/images/storage-ko-light.svg "레이어와 파일: 파일 하나가 바뀌면 레이어 방식은 레이어 전체를 다시 저장합니다.")

다른 엔진은 이미지를 레이어로 저장합니다. 레이어는 전체가 같을 때만 한 번 저장됩니다. 안의 파일 하나가 바뀌면 레이어 전체를 다시 저장합니다.

podbag은 레이어를 파일로 나누고, 파일마다 한 번만 저장합니다. 이미지는 이 파일들을 가리키는 경로 목록입니다. 두 컨테이너가 같은 파일을 읽으면 같은 inode를 읽으므로, 커널은 그 파일을 한 번만 캐시합니다.

Spring 서비스 8개, 릴리스 2개로 측정했습니다.

<!-- compare-columns: podbag docker -->
| | podbag | Docker | podbag 절감 |
|---|--:|--:|--:|
| 두 릴리스의 디스크 | {{n:902}} MiB | {{n:2970}} MiB | 70% |
| 서비스 16개를 시작할 때의 페이지 캐시 | {{n:324}} MiB | {{n:982}} MiB | 67% |

내려받는 양은 같습니다. 레지스트리는 레이어를 보내고, podbag은 레이어를 통째로 받은 다음 파일로 나눕니다.

## 시작 시간과 메모리

![Linux VM 한 대에서 podbag을 Docker, Podman, Kiri와 비교한 결과: 시작 시간, 컨테이너 100개의 메모리, 컨테이너가 없을 때의 메모리, 디스크, 페이지 캐시.](/images/perf.svg "podbag과 Docker, Podman, Kiri의 비교 애니메이션(영어).")

모든 도구를 같은 Linux VM에서 실행했습니다. CPU 4개, {{n:3.8}} GiB, arm64입니다. 버전은 podbag 0.1.0, Podman 5.7.0, Docker 29.1.3, Kiri 0.2.1입니다. 숫자는 중앙값입니다. 낮을수록 좋습니다.

<!-- compare-columns: podbag podbag kiri podman docker -->
| | podbag (rootless) | podbag (root) | Kiri | Podman | Docker |
|---|--:|--:|--:|--:|--:|
| 컨테이너 시작 | {{n:4.1}} ms | {{n:4.4}} ms | {{n:9.1}} ms | {{n:46.4}} ms | {{n:73.8}} ms |
| 컨테이너 100개의 메모리 | {{n:117}} MiB | {{n:105}} MiB | {{n:109}} MiB | {{n:203}} MiB | {{n:562}} MiB |
| 컨테이너가 없을 때의 프로세스 | {{n:0}} | {{n:0}} | {{n:1}}개 ({{n:5.9}} MiB) | {{n:1}}개 ({{n:0.6}} MiB) | {{n:4}}개 ({{n:203}} MiB) |

- keeper가 아직 없을 때의 첫 시작은 {{n:12.8}}–{{n:16.0}} ms 걸립니다.
- 메모리는 Kiri와 비슷합니다. 컨테이너가 없을 때는 podbag이 앞섭니다. 그때는 podbag의 어떤 것도 실행되지 않기 때문입니다.
- 모든 숫자와 측정 방법: [벤치마크](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks.md), [Spring 마이크로서비스 벤치마크](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks-msa.md)(영어).
- 같은 비교를 영상으로: [perf.mp4](/media/perf.mp4)(영어).

## Docker 도구와 함께 동작

`podbag system service`는 소켓으로 Docker Engine API를 제공합니다. `docker` CLI, Compose, buildx가 이 소켓으로 podbag을 씁니다.

```sh
podbag system service &
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podbag/docker.sock
docker compose up -d
```

- 데몬이 아닙니다. 컨테이너는 이 서비스에 의존하지 않습니다.
- 클라이언트가 없으면 60초 뒤에 멈춥니다.
- systemd가 있으면 첫 연결 때 시작할 수 있습니다.

## root 유무와 상관없이

- 같은 프로그램이 두 방식 모두로 동작합니다.
- root일 때 podbag은 composefs로 이미지를 마운트합니다.
- root가 아닐 때는 하드 링크 트리를 만들고, `pasta`가 컨테이너를 네트워크에 연결합니다.
- `podbag check`는 시스템에 더 필요한 것과 그것을 추가하는 방법을 보여 줍니다.

## Linux, macOS, Windows

- **Linux:** x86_64와 arm64. Linux 5.12 이상, cgroup v2가 필요합니다.
- **macOS**(Apple silicon): podbag은 자체 Linux VM을 작게 실행합니다. 첫 명령이 약 0.5초 만에 VM을 시작합니다. 마지막 컨테이너가 끝나고 60초 뒤에 VM이 꺼집니다. 마지막 컨테이너가 끝나고 6분 뒤, podbag이 차지한 Mac 메모리는 {{n:1.7}} MiB였습니다.
- **Windows**(x86_64, arm64): 실험 기능입니다. podbag은 자체 WSL 2 배포판에서 Linux 엔진을 실행합니다. CI에서 빌드하고 테스트하지만, 실제 Windows 컴퓨터에서는 아직 시험하지 않았습니다.

## 설치

Linux와 macOS:

```sh
curl -fsSL https://podbag.dev/install.sh | sh
```

스크립트는 시스템에 맞는 파일을 내려받고, SHA-256 체크섬을 확인하고, `/usr/local/bin`에 설치합니다.

[릴리스 페이지](https://github.com/SteelCrab/podbag/releases/tag/v0.1.0)에서 파일을 직접 받을 수도 있습니다. `SHA256SUMS`로 확인하세요.

| 시스템 | 파일 |
|---|---|
| Linux, x86_64 | `podbag-x86_64-linux` |
| Linux, arm64 | `podbag-aarch64-linux` |
| macOS, Apple silicon | `podbag-aarch64-macos` |
| Windows, x86_64 (실험 기능) | `podbag-x86_64-windows.exe` |
| Windows, arm64 (실험 기능) | `podbag-aarch64-windows.exe` |

그다음 첫 컨테이너를 실행해 보세요.

```sh
podbag run --rm alpine echo hello
```

## 0.1.0의 한계

첫 릴리스라서 아직 없는 기능이 있습니다.

- **빌드:** Dockerfile은 buildx(`docker buildx build`)로만 빌드합니다. 기존 빌더는 없습니다.
- **레지스트리:** 공개 이미지만 받습니다. 로그인, 비공개 이미지 받기, push가 없습니다.
- **Docker 명령:** `commit`, `export`, `diff`, `stats`, `top`, `pause`, `rename`, `update`가 없습니다.
- **Swarm:** swarm 모드와 플러그인이 없습니다.
- **Kubernetes:** CRI가 없어서 Kubernetes 노드가 podbag을 런타임으로 쓸 수 없습니다.
- **Windows:** 실험 기능입니다. Windows의 `docker` CLI는 아직 podbag에 연결할 수 없습니다.
- **Mac 깨우기:** VM이 꺼진 뒤 첫 명령은 약 {{n:0.6}}초 걸립니다.

## 다음 계획

다음 작업은 [열린 풀 리퀘스트](https://github.com/SteelCrab/podbag/pulls)에서 진행 중입니다. 아직 끝나지 않았고, 날짜는 정하지 않았습니다.

- 레지스트리 로그인, 비공개 이미지 받기, push, search
- Dockerfile 빌드와 `commit`, `export`, `diff`
- 노드가 podbag으로 파드를 실행하는 Kubernetes 런타임
- 노드 하나에서 쓰는 swarm 모드
- `stats`, `top`, `pause`, `unpause`, `rename`, `update`
- 터미널 UI와 데스크톱 앱

## 써 보고 알려 주세요

- 모든 명령은 [사용 안내](https://github.com/SteelCrab/podbag/blob/main/docs/usage.md)(영어)에 있습니다.
- 버그와 의견은 [GitHub 이슈](https://github.com/SteelCrab/podbag/issues)에 남겨 주세요. Windows 컴퓨터에서 써 본 결과가 가장 도움이 됩니다.
- podbag은 Apache License 2.0을 따르는 오픈 소스입니다.
