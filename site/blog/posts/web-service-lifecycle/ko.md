---
title: "Podbag 트레이닝 · 웹 서비스 교체하고 정리하기"
date: 2026-11-21
author: team
categories: [how-to]
tags: [cli, containers, desktop, training]
summary: "웹 서비스의 내용을 보존하면서 컨테이너를 교체합니다."
image: gui-ports-ko.png
image_alt: "웹 서비스 교체하고 정리하기"
outline: "실습 순서"
draft: false
---

웹 서비스의 내용을 보존하면서 컨테이너를 교체합니다. 교체 전후에 같은 볼륨과 로컬 주소를 사용합니다.

**예상 시간** 15분

![site-v1이 site-data 볼륨에 페이지를 쓰고, 같은 페이지를 127.0.0.1:18081로 보여 주는 site-v2로 교체됩니다](architecture-ko-light.svg)

## 초보자 코스

[첫 컨테이너 실행하기](../container-basics/) → [브라우저에서 웹 서버 열기](../web-basics/) → [컨테이너를 바꿔도 파일 남기기](../volume-persistence/) → **웹 서비스 교체하고 정리하기**

## 모듈 설치하기

[web-service-lifecycle.podbag 다운로드](web-service-lifecycle.podbag). Desktop의 **Training** 상단에서 **모듈 설치**를 누릅니다. 다운로드한 파일을 선택하고 확인합니다.

```sh
podbag lab install web-service-lifecycle.podbag
```

![모듈 이름과 파일이 표시된 설치 확인 창](install-ko.png)

## 실습 시작하기

왼쪽 메뉴에서 **Training**을 펼치고 설치한 모듈을 선택합니다. 시작 명령을 복사해 사용 중인 터미널에서 실행합니다. `training $` 프롬프트가 나타나면 다음 단계로 이동합니다.

```sh
podbag lab start web-service-lifecycle
```

![실습 시작하기](start-ko.png)

기본 포트가 사용 중이면 Training에 표시된 포트를 사용합니다. 실행 명령과 접속 주소에 같은 포트가 표시됩니다.

## 웹 페이지용 볼륨 만들기

웹 페이지를 저장할 `site-data` 볼륨을 만듭니다.

```sh
podbag volume create site-data
```

![웹 페이지용 볼륨 만들기](create-ko.png)

## 첫 서버 실행하기

`site-v1`가 볼륨에 `index.html`을 저장하고 웹 페이지를 제공합니다. 내 컴퓨터에서 사용할 기본 포트는 `18081`입니다.

```sh
podbag run -d --name site-v1 -p 127.0.0.1:18081:8080 -v site-data:/site docker.io/library/busybox:1.37.0 sh -c 'printf "%s\n" "My Podbag site" > /site/index.html && exec httpd -f -p 8080 -h /site'
```

![첫 서버 실행하기](runFirst-ko.png)

## 첫 서버의 포트 확인하기

**실습 컨테이너 → site-v1 → 포트 보기**를 누릅니다. 상세 화면에서 접속 주소를 확인합니다.

![첫 서버의 포트 확인하기](ports-ko.png)

![첫 서버의 포트 확인하기](gui-ports-ko.png)

## 첫 서버의 페이지 열기

**브라우저에서 열기**를 누릅니다. 페이지에 **My Podbag site**가 표시되는지 확인합니다.

![첫 서버의 페이지 열기](browser-ko.png)

![첫 서버의 페이지 열기](web-browser-en.png)

## 첫 서버 중지하기

**실습 컨테이너 → site-v1 → 중지**를 누릅니다.

![첫 서버 중지하기](stop-ko.png)

![첫 서버 중지하기](gui-stop-ko.png)

## 첫 서버 삭제하기

삭제 명령을 실행합니다. 컨테이너는 사라지고 `site-data` 볼륨은 남습니다.

```sh
podbag rm site-v1
```

![첫 서버 삭제하기](remove-ko.png)

## 교체 서버 실행하기

같은 포트에서 `site-v2`를 시작합니다. `site-data`를 읽기 전용으로 연결합니다. 새 서버는 볼륨에 이미 저장된 페이지를 읽습니다.

```sh
podbag run -d --name site-v2 -p 127.0.0.1:18081:8080 -v site-data:/site:ro docker.io/library/busybox:1.37.0 httpd -f -p 8080 -h /site
```

![교체 서버 실행하기](runReplacement-ko.png)

## 교체 서버의 포트 확인하기

**실습 컨테이너 → site-v2 → 포트 보기**를 누릅니다. 첫 서버와 주소가 같은지 확인합니다.

![교체 서버의 포트 확인하기](portsReplacement-ko.png)

![교체 서버의 포트 확인하기](gui-ports-replacement-ko.png)

## 교체 서버의 페이지 열기

**브라우저에서 열기**를 다시 누릅니다. **My Podbag site**가 계속 표시됩니다. Desktop은 새 HTTP 요청으로 응답을 확인합니다.

![교체 서버의 페이지 열기](browserReplacement-ko.png)

![교체 서버의 페이지 열기](web-browserReplacement-en.png)

## 교체 서버 중지하기

**실습 컨테이너 → site-v2 → 중지**를 누릅니다.

![교체 서버 중지하기](stopReplacement-ko.png)

![교체 서버 중지하기](gui-stop-replacement-ko.png)

## 교체 서버 삭제하기

같은 터미널에서 중지된 컨테이너를 삭제합니다.

```sh
podbag rm site-v2
```

![교체 서버 삭제하기](removeReplacement-ko.png)

## 웹 페이지용 볼륨 확인하기

**실습 볼륨 → site-data**를 눌러 남은 볼륨을 확인합니다.

![웹 페이지용 볼륨 확인하기](inspect-ko.png)

![웹 페이지용 볼륨 확인하기](gui-inspect-en.png)

## 웹 페이지용 볼륨 삭제하기

**삭제**를 누릅니다. 확인 창에서 볼륨 이름을 확인한 뒤 삭제합니다.

![웹 페이지용 볼륨 삭제하기](delete-ko.png)

![웹 페이지용 볼륨 삭제하기](gui-delete-en.png)

## 컨테이너 목록 확인하기

실습 환경의 컨테이너를 조회합니다. 목록이 비어 있습니다.

```sh
podbag ps -a
```

![컨테이너 목록 확인하기](checkContainers-ko.png)

## 볼륨 목록 확인하기

실습 볼륨을 조회합니다. 목록이 비어 있습니다.

```sh
podbag volume ls
```

![볼륨 목록 확인하기](checkVolumes-ko.png)

## 실습 종료하기

현재 단계에 종료 명령이 표시되면 입력합니다. 임시 실습 환경을 정리한 뒤 Training에 완료로 표시됩니다.

```sh
exit
```

![실습 종료하기](finish-ko.png)

![모든 단계가 완료된 Training 화면](complete-ko.png)

[다음 트레이닝 · 로그로 웹 서버 장애 해결하기](/ko/blog/web-service-recovery/)
