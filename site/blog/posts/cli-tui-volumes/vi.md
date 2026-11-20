---
title: "Bài thực hành · Quản lý volume bằng CLI và GUI"
date: 2026-11-20
author: team
categories: [how-to]
tags: [cli, desktop, tutorials, volumes]
summary: "Tạo volume trong CLI, xem chi tiết và xóa trong Desktop, rồi theo dõi tiến độ."
image: gui-volumes-vi.png
image_alt: "Volume thực hành · my-api"
draft: false
---

Tạo volume trong CLI, xem chi tiết và xóa trong Desktop, rồi theo dõi tiến độ.

[Tải mô-đun](cli-gui-volumes.podbag)

## Volume là gì?

Volume là nơi lưu tệp độc lập với container. Trong ví dụ này, `app-a` lưu `note.txt` vào volume `my-api`. Sau khi xóa `app-a`, container mới `app-b` gắn cùng volume và đọc lại tệp. Nếu xóa chính volume đó, các tệp bên trong cũng sẽ bị xóa.

[![Volume là gì?](volume-life.webp)](volume-life.mp4)

## Cài mô-đun

Dùng bản Desktop và CLI hỗ trợ bài này. Tải tệp rồi cài từ mục hướng dẫn trên Desktop, hoặc chạy lệnh dưới đây trong thư mục tải xuống.

```sh
podbag lab install cli-gui-volumes.podbag
```

![Cài mô-đun](gui-install.png)

## Mở bài thực hành trong Desktop

Chọn **Mở hướng dẫn trên web** trong **Training** để quay lại trang này. Training hiển thị trạng thái mô-đun và tác vụ hiện tại.

![Mô-đun volume cùng các nút thao tác trong Training](gui-ready-vi.png)

## Mở terminal

Mở **Volume thực hành** ở thanh bên Desktop, rồi chọn Terminal. Giữ trang này và terminal mở trong khi thực hành.

![Volume thực hành khi terminal đang mở](gui-shell-vi.png)

## Tạo volume trong CLI

Nhập lệnh này tại dấu nhắc volume-lab.

```sh
podbag volume create my-api
podbag volume ls
```

![podbag volume ls · my-api](gui-create.png)

## Xem chi tiết trong GUI

Khi volume xuất hiện, Training hiển thị tác vụ xem chi tiết trong GUI.

![Volume thực hành · my-api](gui-volumes-vi.png)

Trong Volume thực hành, chọn my-api để xem tên và đường dẫn lưu trữ.

![my-api · Mountpoint](gui-inspect-vi.png)

## Xóa trong GUI

Chọn Xóa cho my-api. Kiểm tra tên rồi xác nhận.

![Xóa trong GUI · my-api](gui-dialog-vi.png)

Sau khi xóa, danh sách sẽ trống. Hãy quay lại cùng terminal thực hành.

![Danh sách volume thực hành trống sau khi xóa](gui-empty-vi.png)

## Kiểm tra trong CLI

Liệt kê lại các volume trong terminal thực hành.

```sh
podbag volume ls
```

![Kết thúc phiên · Đang thực hiện](gui-verified-vi.png)

## Kết thúc phiên

Khi thấy `Verified`, nhập `exit` để dọn kho tạm. Training hiển thị mô-đun đã hoàn thành.

```sh
exit
```

![Verified · exit](gui-finish.png)

![Training hiển thị mô-đun volume đã hoàn thành](gui-complete-vi.png)

## Gỡ mô-đun

Chạy lệnh này trong terminal ban đầu để xóa mô-đun và bản ghi hoàn thành.

```sh
podbag lab remove volume-basics
```

![Gỡ mô-đun · Module removed.](uninstall.png)
