---
title: "Podbag Training · Mở máy chủ web trong trình duyệt"
date: 2026-11-21
author: team
categories: [how-to]
tags: [cli, containers, desktop, training]
summary: "Máy chủ web nhận yêu cầu ở một cổng bên trong container."
image: gui-ports-en.png
image_alt: "Mở máy chủ web trong trình duyệt"
outline: "Các bước thực hành"
draft: false
---

Máy chủ web nhận yêu cầu ở một cổng bên trong container. Khi công bố cổng, trình duyệt có một địa chỉ trên máy tính của bạn. Trong mô-đun này, địa chỉ đó chỉ mở được trên máy tính này.

**Thời gian** 10 phút

![Trình duyệt mở 127.0.0.1:18080, địa chỉ này dẫn tới cổng 8080 của máy chủ web lab-web trong phiên thực hành](architecture-vi-light.svg)

## Lộ trình cho người mới

[Chạy container đầu tiên](../container-basics/) → **Mở máy chủ web trong trình duyệt** → [Giữ tệp khi thay container](../volume-persistence/) → [Thay thế và dọn dẹp dịch vụ web](../web-service-lifecycle/)

## Cài mô-đun

[Tải web-basics.podbag](web-basics.podbag). Trong Desktop, chọn **Cài mô-đun** ở đầu mục **Training**. Chọn tệp đã tải và xác nhận.

```sh
podbag lab install web-basics.podbag
```

![Hộp thoại xác nhận cài đặt có tên mô-đun và tên tệp](install-en.png)

## Bắt đầu phiên thực hành

Mở rộng **Training** ở thanh bên và chọn mô-đun. Sao chép lệnh bắt đầu vào terminal của bạn. Tiếp tục khi thấy dấu nhắc `training $`.

```sh
podbag lab start web-basics
```

![Bắt đầu phiên thực hành](start-en.png)

Nếu cổng mặc định đang được dùng, hãy dùng cổng hiển thị trong Training. Lệnh và địa chỉ trình duyệt hiển thị cùng một cổng.

## Chạy máy chủ web

Sao chép lệnh của bước hiện tại. Lệnh này chạy BusyBox và phục vụ tệp `/www/index.html`. Lần chạy đầu sẽ tải image về.

```sh
podbag run -d --name lab-web -p 127.0.0.1:18080:8080 docker.io/library/busybox:1.37.0 sh -c 'mkdir -p /www && printf "%s\n" "Podbag Training" > /www/index.html && exec httpd -f -p 8080 -h /www'
```

![Chạy máy chủ web](runWeb-en.png)

## Kiểm tra ánh xạ cổng trong Desktop

Mở **Container thực hành → lab-web → Xem cổng**. Ánh xạ mặc định là `127.0.0.1:18080 → 8080/tcp`. Cổng đầu tiên thuộc về máy tính của bạn. Cổng thứ hai thuộc về container.

![Kiểm tra ánh xạ cổng trong Desktop](ports-en.png)

![Kiểm tra ánh xạ cổng trong Desktop](gui-ports-en.png)

## Mở trang trong trình duyệt

Chọn **Mở trong trình duyệt**. Trang hiển thị **Podbag Training**. Desktop kiểm tra rằng địa chỉ cục bộ trả về HTTP 200 và đúng nội dung mong đợi.

![Mở trang trong trình duyệt](browser-en.png)

![Mở trang trong trình duyệt](web-browser-en.png)

## Dừng máy chủ trong Desktop

Quay lại **Container thực hành**. Tìm `lab-web` và chọn **Dừng** ở hàng của nó.

![Dừng máy chủ trong Desktop](stop-en.png)

![Dừng máy chủ trong Desktop](gui-stop-en.png)

## Xóa container đã dừng

Chạy lệnh xóa trong cùng terminal. Bước tiếp theo xuất hiện khi `lab-web` không còn nữa.

```sh
podbag rm lab-web
```

![Xóa container đã dừng](remove-en.png)

## Kết thúc phiên thực hành

Chạy lệnh ở bước cuối cùng. Training ghi nhận hoàn thành sau khi môi trường thực hành đã được xóa.

```sh
exit
```

![Kết thúc phiên thực hành](finish-en.png)

![Training hiển thị tất cả các bước đã hoàn thành](complete-en.png)

[Mô-đun tiếp theo · Giữ tệp khi thay container](../volume-persistence/)
