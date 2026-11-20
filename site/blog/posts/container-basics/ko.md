---
title: "Podbag Training · 첫 컨테이너 실행하기"
date: 2026-11-21
author: team
categories: [how-to]
tags: [cli, containers, desktop, training]
summary: "CLI에서 작은 웹 서버를 실행하고 Podbag Desktop에서 중지합니다. 다시 CLI에서 중지 상태를 확인합니다."
image: running-ko.png
image_alt: "Podbag Desktop에서 실행 중인 hello-web 컨테이너"
outline: "실습 흐름"
draft: false
---

이미지에는 프로그램 실행에 필요한 파일이 들어 있습니다. 컨테이너는 그 이미지의 프로그램을 실행합니다. 이 실습에서는 `hello-web`이라는 작은 웹 서버를 실행하고 Podbag Desktop에서 중지합니다.

## 실습 모듈 설치하기

[container-basics.podbag 다운로드](https://github.com/SteelCrab/podbag/releases/download/training/container-basics/v1.0.0/container-basics.podbag). Training을 지원하는 Podbag Desktop을 엽니다. **Training**에서 파일을 선택하고 **모듈 설치**를 누릅니다. 파일을 받은 폴더에서 다음 명령으로 설치할 수도 있습니다.

```sh
podbag lab install container-basics.podbag
```

이 실습을 이미 설치했다면 새 파일을 다시 설치해도 완료 기록이 유지됩니다. `podbag lab list`로 설치한 실습을 확인할 수 있습니다.

## 실습 터미널 열기

Training 카드에서 **터미널**을 누릅니다. `container-lab $` 프롬프트가 나올 때까지 기다립니다.

![실습 터미널 열기가 완료되고 CLI 실행 단계가 진행 중인 Training 화면](training-ko.png)

## CLI에서 웹 서버 실행하기

같은 실습 터미널에서 다음 명령을 입력합니다. 처음 실행할 때 Podbag이 실습 이미지를 내려받습니다.

```sh
podbag run -d --name hello-web --network none docker.io/library/busybox:1.37.0 httpd -f -p 8080
```

`-d`는 컨테이너를 백그라운드에서 실행합니다. `--name hello-web`은 컨테이너 이름을 지정합니다. 웹 서버는 컨테이너 내부의 8080번 포트에서 실행됩니다. 이번 실습에서는 컨테이너의 시작과 중지를 배우므로 호스트 네트워크와 분리해 실행합니다.

![실습 터미널에 새 컨테이너 ID가 표시된 화면](cli-run.png)

## Desktop에서 컨테이너 중지하기

실습 터미널을 열어 둔 채 Desktop에서 **실습 컨테이너**를 선택합니다. 실행 중인 `hello-web`의 행에서 **중지**를 누릅니다. 컨테이너 상세 화면에서도 중지할 수 있습니다.

![실습 컨테이너의 hello-web이 실행 중이고 중지 버튼을 누를 수 있는 화면](running-ko.png)

Desktop에 중지 상태가 나타납니다. **CLI에서 상태 확인하기**가 진행 중으로 바뀝니다.

![hello-web이 중지되고 CLI 상태 확인이 진행 중인 화면](stopped-ko.png)

## CLI에서 결과 확인하기

같은 실습 터미널로 돌아가 모든 컨테이너를 조회합니다. `-a` 옵션은 중지된 컨테이너도 목록에 표시합니다.

```sh
podbag ps -a
```

`hello-web`의 상태가 `Exited`인지 확인합니다. 실습 터미널에는 `Verified`가 표시됩니다.

![CLI에 hello-web의 Exited 상태와 검증 완료 메시지가 표시된 화면](cli-check.png)

## 실습 종료하기

`exit`를 입력합니다. Podbag이 실습 컨테이너와 내려받은 이미지, 임시 저장소를 정리합니다. 실습 모듈과 완료 기록은 Training에서 확인할 수 있습니다.

![임시 저장소가 정리되고 실습이 완료된 Podbag Desktop 화면](complete-ko.png)
