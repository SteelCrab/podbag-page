---
title: "Bài thực hành · Tạo volume bằng CLI và xóa bằng TUI"
date: 2026-11-20
author: team
categories: [how-to]
tags: [cli, tui, tutorials, volumes]
summary: "Tạo volume Podbag, xem thông tin rồi xóa bằng giao diện terminal."
image: volumes.png
image_alt: "my-api · Volumes"
draft: false
---

Dùng bản Podbag hỗ trợ `podbag lab --help`. Tải tệp rồi mở terminal tại thư mục chứa tệp. Bài thực hành dùng vùng lưu trữ tạm riêng.

[Tải mô-đun](cli-tui-volumes.podbag)

## Cài mô-đun

Cài tệp đã tải. Bạn cũng có thể chọn tệp trong mục hướng dẫn của Desktop.

```sh
podbag lab install cli-tui-volumes.podbag
```

![Cài mô-đun · podbag lab install](install.png)

## Mở terminal thực hành

Bắt đầu phiên. Khi thấy `volume-lab $`, hãy nhập các lệnh tiếp theo tại đó.

```sh
podbag lab start --lang vi
```

![Mở terminal thực hành · volume-lab](shell-vi.png)

## Tạo volume

Tạo `my-api`, liệt kê volume và tìm tên trong cột `VOLUME NAME`.

```sh
podbag volume create my-api
podbag volume ls
```

![Tạo volume · my-api](create.png)

## Tìm volume trong TUI

Chạy TUI trong cùng terminal. Nhấn `Tab` đến **Volumes** rồi chọn `my-api`.

```sh
podbag tui
```

![Tìm volume trong TUI · Volumes](volumes.png)

## Xem thông tin volume

Nhấn `Enter` để mở **Inspect**. Kiểm tra `Name` và `Mountpoint`, rồi nhấn `Esc` để quay lại.

![Xem thông tin volume · Mountpoint](inspect.png)

## Xóa volume đã chọn

Nhấn `d` tại dòng `my-api`. Kiểm tra tên trong hộp thoại và nhấn `y` để xác nhận.

![Xóa volume đã chọn · my-api](remove.png)

## Kiểm tra danh sách trống

Khi thấy **No volumes on this engine.**, nhấn `q` để quay lại terminal.

![Kiểm tra danh sách trống · No volumes on this engine.](empty.png)

## Kết thúc phiên

Liệt kê volume lần nữa. Khi thấy `Verified`, nhập `exit` để dừng dịch vụ và dọn các tệp tạm.

```sh
podbag volume ls
exit
```

![Kết thúc phiên · Verified](finish.png)

## Gỡ mô-đun

Chạy lệnh này trong terminal ban đầu để xóa mô-đun và bản ghi hoàn thành.

```sh
podbag lab remove
```

![Gỡ mô-đun · Module removed.](uninstall.png)
