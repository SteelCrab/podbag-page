---
title: "Podbag Desktop · Quản lý container"
date: 2026-11-27
author: team
categories: [how-to]
tags: [desktop, gui, containers]
summary: "Chạy một container mới, dừng, tạm dừng và xóa container, đọc nhật ký và chi tiết, mở shell, rồi dọn dẹp các container đã dừng."
image: gui-logs-vi.png
image_alt: "Tab Nhật ký của container web trong Podbag Desktop"
outline: "Trong hướng dẫn này"
draft: false
---

Mở **Container** trên thanh bên. Danh sách hiện tên và ID, image, trạng thái, cổng và ngày tạo của mỗi container.

**Thời gian** 5 phút.

## Chạy một container mới

Nhấp vào **Chạy container** ở đầu danh sách. Một biểu mẫu mở ra.

1. Gõ **Image**, ví dụ `nginx:alpine`. Ô này gợi ý những image bạn đã có.
2. Gõ **Tên**. Bạn có thể để trống.
3. Trong **Cổng**, gõ một cổng máy chủ và một cổng container, ví dụ `8081` và `80`. Chọn TCP hoặc UDP. Để trống cổng máy chủ để engine tự chọn. **Thêm cổng** thêm một dòng.
4. Nhấp vào **Chạy**.

![Biểu mẫu Chạy một container của Podbag Desktop](gui-run-vi.png)

**Tùy chọn khác** hiện thêm các ô.

- **Biến môi trường:** mỗi dòng một `KEY=VALUE`.
- **Ổ đĩa:** tên ổ đĩa hoặc đường dẫn đầy đủ trên máy, rồi đến đường dẫn trong container. Đánh dấu **Chỉ đọc** nếu container không được ghi vào đó.
- **Lệnh:** để trống để dùng lệnh của image.
- **Chính sách khởi động lại:** **Không khởi động lại**, **Khi bị lỗi**, **Luôn luôn** hoặc **Trừ khi bạn dừng**.
- **Xóa khi dừng:** xóa container khi nó dừng. Tùy chọn này tắt chính sách khởi động lại.

Biểu mẫu kiểm tra những gì bạn nhập trước khi gửi. Khi engine chưa có image, ứng dụng tải image trước. Ứng dụng dùng thông tin đăng nhập registry của bạn, như **Tải image**. Sau đó container mới mở ra cùng nhật ký của nó.

## Chạy và dừng container

Các nút ở cuối một dòng thay đổi theo trạng thái của container.

- **Đang chạy:** **Dừng**, **Khởi động lại**, **Tạm dừng**, **Nhật ký**, **Mở shell** và **Xóa**.
- **Tạm dừng:** **Tiếp tục**, **Dừng**, **Nhật ký** và **Xóa**.
- **Đã dừng:** **Chạy**, **Nhật ký** và **Xóa**.

**Tạm dừng**, **Tiếp tục** và **Đổi tên** chỉ hiện khi engine hỗ trợ các thao tác này. podbag có hỗ trợ. Trạng thái trong danh sách thay đổi khi thao tác xong.

## Mở một container

Nhấp vào một dòng. Phần chi tiết có ba tab.

- **Thông tin:** ID, image, lệnh, trạng thái, cổng và ngày tạo container.
- **Nhật ký:** đầu ra của container. Khi bật **Theo dõi**, các dòng mới hiện ở dưới cùng.
- **Dữ liệu đầy đủ:** mọi thông tin engine có về container, ở dạng JSON.

![Tab Thông tin của container web trong Podbag Desktop](gui-detail-vi.png)

Các nút ở góc trên bên phải thao tác với container này. Nút **Đổi tên** cũng ở đây. Nhấn `Esc` hoặc nhấp vào mũi tên lùi để quay lại danh sách.

![Tab Nhật ký của container web trong Podbag Desktop](gui-logs-vi.png)

## Mở shell

**Mở shell** mở một terminal với shell bên trong container đang chạy. Khi ứng dụng không tìm thấy ứng dụng terminal, nó hiện lệnh. Nhấp vào **Sao chép** và chạy lệnh đó trong terminal.

## Xóa container

Nhấp vào **Xóa**. Ứng dụng hỏi trước. Container đang chạy sẽ bị dừng, rồi bị xóa.

![Podbag Desktop hỏi trước khi xóa container web đang chạy](gui-remove-vi.png)

## Dọn dẹp

**Dọn dẹp** ở phía trên danh sách xóa tất cả container đã dừng. Ứng dụng hỏi trước. Sau đó, ứng dụng cho biết đã xóa bao nhiêu container và giải phóng bao nhiêu dung lượng.

## Tiếp theo

[Tải và quản lý image](../gui-images/).
