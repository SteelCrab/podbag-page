---
title: "Podbag Training · Giữ tệp khi thay container"
date: 2026-11-21
author: team
categories: [how-to]
tags: [cli, containers, desktop, training]
summary: "Volume lưu các tệp vẫn còn sau khi container bị xóa."
image: read-en.png
image_alt: "Giữ tệp khi thay container"
outline: "Các bước thực hành"
draft: false
---

Volume lưu các tệp vẫn còn sau khi container bị xóa. Xem hình động, rồi thử cùng các bước đó với `app-a` và `app-b`.

**Thời gian** 15 phút

![app-a ghi note.txt vào volume training-data và app-b đọc tệp đó; volume vẫn còn sau khi cả hai container bị xóa](architecture-vi-light.svg)

## Lộ trình cho người mới

[Chạy container đầu tiên](../container-basics/) → [Mở máy chủ web trong trình duyệt](../web-basics/) → **Giữ tệp khi thay container** → [Thay thế và dọn dẹp dịch vụ web](../web-service-lifecycle/)

[![Volume vẫn còn khi thay container](volume-life.webp)](volume-life.mp4)

## Cài mô-đun

[Tải volume-persistence.podbag](volume-persistence.podbag). Trong Desktop, chọn **Cài mô-đun** ở đầu mục **Training**. Chọn tệp đã tải và xác nhận.

```sh
podbag lab install volume-persistence.podbag
```

![Hộp thoại xác nhận cài đặt có tên mô-đun và tên tệp](install-en.png)

## Bắt đầu phiên thực hành

Mở rộng **Training** ở thanh bên và chọn mô-đun. Sao chép lệnh bắt đầu vào terminal của bạn. Tiếp tục khi thấy dấu nhắc `training $`.

```sh
podbag lab start volume-persistence
```

![Bắt đầu phiên thực hành](start-en.png)

Để làm các bước trong TUI thay cho Podbag Desktop, hãy thêm `--tui`.

```sh
podbag lab start volume-persistence --tui
```

Trong TUI, nhấn `:` để mở shell Training cho bước chạy lệnh, gõ `exit` để quay lại TUI và nhấn `q` để kết thúc phiên.

## Tạo volume

Tạo volume có tên `training-data` trong phiên thực hành.

```sh
podbag volume create training-data
```

- **Trong Podbag Desktop:** Chọn **Volume thực hành → Tạo volume training-data**.
- **Trong TUI:** Mở **Volume**, nhấn `v`, gõ `training-data` rồi nhấn `Enter`.

![Tạo volume](create-en.png)

## Ghi tệp từ app-a

`-v training-data:/data` gắn volume vào container. Lệnh này ghi `note.txt`, rồi `app-a` thoát.

```sh
podbag run --name app-a --network none -v training-data:/data docker.io/library/busybox:1.37.0 sh -c 'printf "%s\n" "hello from app-a" > /data/note.txt'
```

![Ghi tệp từ app-a](write-en.png)

## Xóa app-a

Xóa container đã dừng. Volume vẫn còn trong phiên thực hành.

```sh
podbag rm app-a
```

- **Trong Podbag Desktop:** Chọn **Container thực hành → app-a → Xóa** và xác nhận.
- **Trong TUI:** Chọn `app-a` trong **Container**, nhấn `d`, rồi nhấn `y`.

![Xóa app-a](removeWriter-en.png)

## Đọc tệp từ app-b

`app-b` gắn cùng volume đó. Hậu tố `:ro` làm cho volume chỉ đọc. Terminal hiển thị `hello from app-a`.

```sh
podbag run --name app-b --network none -v training-data:/data:ro docker.io/library/busybox:1.37.0 cat /data/note.txt
```

![Đọc tệp từ app-b](read-en.png)

![Đọc tệp từ app-b](terminal-read-en.png)

## Xóa app-b

Xóa container thứ hai để giải phóng volume trước khi xóa volume.

```sh
podbag rm app-b
```

- **Trong Podbag Desktop:** Chọn **Container thực hành → app-b → Xóa** và xác nhận.
- **Trong TUI:** Chọn `app-b` trong **Container**, nhấn `d`, rồi nhấn `y`.

![Xóa app-b](removeReader-en.png)

## Mở chi tiết volume

Chọn **Volume thực hành → training-data**. Phần chi tiết hiển thị tên và điểm gắn (mount point) của volume.

- **Trong Podbag Desktop:** Chọn **Volume thực hành → training-data**.
- **Trong TUI:** Chọn `training-data` trong **Volume** rồi nhấn `Enter`.

![Mở chi tiết volume](inspect-en.png)

![Mở chi tiết volume](gui-inspect-en.png)

## Xóa volume trong Desktop

Chọn **Xóa** và kiểm tra rằng hộp thoại ghi tên `training-data`. Volume và tệp bên trong bị xóa.

- **Trong Podbag Desktop:** Chọn **Volume thực hành → training-data → Xóa** và xác nhận.
- **Trong TUI:** Chọn `training-data` trong **Volume**, nhấn `d`, rồi nhấn `y`.

![Xóa volume trong Desktop](delete-en.png)

![Xóa volume trong Desktop](gui-delete-en.png)

## Kiểm tra danh sách volume

Quay lại cùng terminal. Danh sách volume không còn `training-data`.

```sh
podbag volume ls
```

![Kiểm tra danh sách volume](checkVolumes-en.png)

## Kết thúc phiên thực hành

Chạy lệnh ở bước cuối cùng. Training ghi nhận hoàn thành sau khi môi trường thực hành đã được xóa.

```sh
exit
```

![Kết thúc phiên thực hành](finish-en.png)

![Training hiển thị tất cả các bước đã hoàn thành](complete-en.png)

[Mô-đun tiếp theo · Thay thế và dọn dẹp dịch vụ web](../web-service-lifecycle/)
