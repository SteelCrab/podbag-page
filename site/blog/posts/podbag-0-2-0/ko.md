---
title: "Podbag 0.2.0 릴리스"
date: 2026-11-21
author: team
categories: [announcements]
tags: [release, kubernetes, migration, registries, desktop]
summary: "레지스트리에서 이미지를 받고 Dockerfile로 이미지를 빌드합니다. Podbag을 Kubernetes 런타임으로 사용하고, 엔진과 클러스터 사이에서 데이터를 복사합니다."
image: card-ko.png
image_alt: "Podbag 0.2.0 릴리스"
draft: false
---

Podbag 0.2.0을 공개했습니다. 이번 버전에서는 컨테이너 이미지를 만들고 배포할 수 있습니다. 기존 이미지와 데이터를 다른 엔진이나 Kubernetes 클러스터로 옮길 수도 있습니다.

## 이미지 빌드와 레지스트리

`podbag build`로 Dockerfile에서 이미지를 빌드합니다. 레지스트리에서 이미지를 받거나, 빌드한 이미지를 레지스트리에 올릴 수 있습니다.

Podbag Desktop에서 **이미지 받기**를 열고 Docker Hub, GitHub Container Registry 또는 사용자 지정 주소를 선택합니다. 이미지 이름과 태그를 입력합니다. 비공개 이미지는 접근 권한이 있는 기존 Docker 로그인으로 받을 수 있습니다.

![Podbag Desktop의 이미지 받기에서 여러 레지스트리를 고르는 화면](/images/pull-registries-en.png)

## 엔진과 클러스터 사이에서 복사

`podbag migrate` 또는 Desktop의 마이그레이션 메뉴에서 단일 플랫폼 이미지, 중지된 컨테이너, 로컬 볼륨을 Docker 호환 엔진 사이에 복사합니다. 원본은 그대로 유지합니다.

Desktop은 두 Kubernetes 컨텍스트 사이에서 독립 실행형 파드, 서비스, 디플로이먼트, 파일시스템 PVC를 복사합니다. PVC는 영구 저장소를 요청하는 객체입니다. 이미 볼륨에 연결된 파일시스템 PVC는 파일도 옮긴 뒤 대상에서 확인합니다. 복사 전에 원본 볼륨에 쓰는 작업을 중지합니다. [마이그레이션 요건](https://github.com/SteelCrab/podbag/blob/v0.2.0/docs/usage.md#migrate-between-engines-or-kubernetes-clusters)

## Kubernetes, Swarm, Desktop

Linux에서 `podbag cri serve`를 Kubernetes 노드의 컨테이너 런타임으로 사용할 수 있습니다. 단일 노드에서는 Docker Swarm 서비스와 스택도 실행할 수 있습니다. 같은 k3s 노드에서 Docker Engine과 Podbag을 비교한 측정 방법과 결과를 공개했습니다. [k3s 부하 시험](/ko/blog/k3s-30-pods-docker-podbag/)

`podbag tui`와 Desktop에서 컨테이너와 이미지를 관리하고 Docker CLI의 연결 대상을 바꿉니다. Apple Silicon Mac에서는 Desktop에서 Linux VM의 CPU, 메모리, 유휴 종료 시간을 설정할 수 있습니다.

## 0.2.0 설치

Linux 또는 Apple Silicon Mac에서 다음 명령으로 0.2.0 CLI를 설치합니다. 설치 스크립트는 다운로드의 SHA-256을 확인합니다.

```sh
curl -fsSL https://podbag.dev/install.sh | PODBAG_VERSION=v0.2.0 sh
podbag --version
```

Linux는 AMD64와 ARM64용 DEB·RPM 패키지를 제공합니다. macOS에서는 CLI를 설치한 뒤 Desktop ZIP을 풉니다. Windows CLI는 WSL 2가 필요하고 실험 단계입니다. Android ARM64 CLI는 이미지 명령을 지원합니다. [0.2.0 다운로드](https://github.com/SteelCrab/podbag/releases/tag/v0.2.0)

0.1.0에서 저장한 이미지에 파일 수정 시간이나 crontab 문제가 있었다면, 해당 이미지를 제거한 뒤 다시 받거나 불러옵니다. [전체 변경 사항](https://github.com/SteelCrab/podbag/blob/v0.2.0/CHANGELOG.md#v020-2026-11-20)
