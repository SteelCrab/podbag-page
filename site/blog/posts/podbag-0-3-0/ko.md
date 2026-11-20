---
title: "Podbag 0.3.0 릴리스"
date: 2026-11-21
author: team
categories: [announcements]
tags: [release, desktop, windows, training, tui]
summary: "Windows에서 Podbag Desktop을 설치합니다. Apple silicon Mac에서는 내장 엔진으로 Linux VM을 시작합니다. 실습 네 개로 컨테이너 사용법을 익힙니다."
image: card-ko.png
image_alt: "Podbag 0.3.0 릴리스"
draft: false
---

Podbag 0.3.0을 공개했습니다. Windows용 설치 프로그램, 엔진이 포함된 macOS용 Desktop 번들, 초급 실습 네 개를 추가했습니다.

## Podbag Desktop 설치

- **Windows x86_64 및 ARM64.** CPU에 맞는 MSI를 받습니다. 시작 메뉴에서 **Podbag Desktop**을 엽니다. 컨테이너를 실행하려면 WSL 2를 활성화합니다.
- **Apple silicon Mac.** Desktop ZIP을 풀고 `podbag.app`을 엽니다. Desktop이 내장 엔진으로 Linux VM을 시작합니다.
- **Linux x86_64 및 ARM64.** 배포판과 CPU에 맞는 DEB 또는 RPM을 설치합니다. 패키지에 엔진이 포함됩니다.

[Podbag 0.3.0 다운로드](https://github.com/SteelCrab/podbag/releases/tag/v0.3.0)

## Podbag 실습

Desktop의 **Training**을 엽니다. 컨테이너 실행, 로컬 웹 페이지 공개, 볼륨에 파일 보관, 웹 서비스 교체를 차례로 배웁니다. 각 가이드에 따라 모듈을 설치합니다. Desktop은 실습을 별도 환경에서 실행하고 진행 상태를 표시합니다. [첫 컨테이너 실행하기](/ko/blog/container-basics/)

![Podbag Desktop의 초급 실습 목록과 실행할 명령](https://podbag.dev/blog/web-basics/start-ko.png)

## 터미널에서 관리

`podbag tui`에서 볼륨을 만들고, 레지스트리에 로그인하고, 이미지를 가져오고, Kubernetes 리소스를 확인합니다. CLI에는 `podbag engine`, `podbag import`, `podbag kube`, `podbag settings`, `podbag tutorial` 명령이 추가되었습니다.

Linux 또는 Apple silicon Mac에서 CLI를 설치합니다. 설치 스크립트는 다운로드한 파일의 SHA-256 체크섬을 확인합니다.

```sh
curl -fsSL https://podbag.dev/install.sh | PODBAG_VERSION=v0.3.0 sh
podbag --version
```

[전체 변경 기록](https://github.com/SteelCrab/podbag/blob/v0.3.0/CHANGELOG.md#v030-2026-11-21)
