---
title: "Bài thực hành · Đọc JSON từ volume qua HTTP"
date: 2026-11-20
author: team
categories: [how-to]
tags: [desktop, tutorials, volumes, http]
summary: "Tạo volume, viết tệp phản hồi rồi đọc nội dung qua máy chủ HTTP cục bộ."
image: 08-response-vi.png
image_alt: "Phản hồi HTTP 200 chứa JSON được đọc từ volume."
draft: false
---

Dùng phiên bản Podbag Desktop có mục **Hướng dẫn** trên thanh bên. Bài thực hành dùng vùng lưu trữ tạm trên máy, không cần chạy container hoặc tải image.

[Tải mô-đun thực hành](volume-api.podbag)

Lưu `volume-api.podbag` và ghi nhớ vị trí.

## Mở mục Hướng dẫn

Chọn **Hướng dẫn** ở thanh bên trái. Lần đầu mở, bạn sẽ thấy màn hình cài mô-đun.

![Màn hình cài đặt có nút chọn tệp.](01-open-vi.png)

## Chọn mô-đun

Nhấn **Chọn tệp** và mở `volume-api.podbag` đã tải. Kiểm tra tiêu đề bài và tên tệp.

![Tên tệp đã chọn và tiêu đề bài thực hành.](02-file-vi.png)

## Cài và bắt đầu

Nhấn **Cài mô-đun**. Khi đã cài xong, nhấn **Bắt đầu thực hành** để mở không gian trống.

![Mô-đun đã cài hiển thị mục tiêu và nút bắt đầu.](03-installed-vi.png)

## Tạo volume

Nhập `my-api` vào ô tên rồi nhấn **Tạo volume**. Đường dẫn tệp ở màn hình tiếp theo bắt đầu bằng tên này.

![Ô tên volume có giá trị my-api.](04-volume-vi.png)

## Viết nội dung phản hồi

Thay giá trị của `message` bằng lời chào của bạn, chẳng hạn `Hello from my lab!`. Giữ nguyên dấu ngoặc kép và ngoặc nhọn. Nhấn **Lưu tệp**.

![Trình chỉnh sửa response.json hiển thị lời chào đã nhập.](05-write-vi.png)

## Khởi động máy chủ

Kiểm tra JSON đã lưu rồi nhấn **Khởi động máy chủ**. Ứng dụng chọn một cổng trống trên `127.0.0.1`.

![JSON đã lưu và nút khởi động máy chủ.](06-saved-vi.png)

## Gửi yêu cầu

Nhấn **Gửi GET /** để đọc đường dẫn gốc. Bạn cũng có thể sao chép URL vào trình duyệt trên cùng máy. Số cổng có thể khác ở mỗi buổi thực hành.

![Địa chỉ cục bộ và nút gửi GET /.](07-server-vi.png)

## Kiểm tra và thay đổi phản hồi

Tìm lời chào của bạn bên dưới `HTTP 200`. Nhấn **Sửa tệp**, đổi lời chào rồi lưu. Gửi yêu cầu đến cùng URL để xem giá trị mới.

![Phản hồi HTTP 200 chứa JSON được đọc từ volume.](08-response-vi.png)

## Kết thúc thực hành

Nhấn **Kết thúc thực hành** rồi xác nhận. Máy chủ dừng, volume tạm và các tệp được xóa. Mô-đun và bản ghi hoàn thành vẫn được giữ lại.

![Hộp thoại xác nhận dừng máy chủ và xóa volume tạm.](09-end-vi.png)
