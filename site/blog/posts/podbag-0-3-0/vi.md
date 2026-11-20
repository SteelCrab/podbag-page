---
title: "Phát hành Podbag 0.3.0"
date: 2026-11-21
author: team
categories: [announcements]
tags: [release, desktop, windows, training, tui]
summary: "Cài Podbag Desktop trên Windows, khởi động máy ảo Linux trên máy Mac dùng chip Apple và học cách dùng container qua bốn bài thực hành."
image: card-vi.png
image_alt: "Phát hành Podbag 0.3.0"
draft: false
---

Podbag 0.3.0 đã có mặt. Bản này có trình cài đặt cho Windows, gói Desktop cho macOS kèm engine và bốn mô-đun dành cho người mới.

## Cài Podbag Desktop

- **Windows x86_64 và ARM64.** Tải tệp MSI phù hợp với CPU. Mở **Podbag Desktop** từ menu Start. Bật WSL 2 để chạy container.
- **Máy Mac dùng chip Apple.** Giải nén tệp ZIP của Desktop và mở `podbag.app`. Desktop khởi động máy ảo Linux bằng engine đi kèm.
- **Linux x86_64 và ARM64.** Cài gói DEB hoặc RPM phù hợp với bản phân phối và CPU. Gói này có sẵn engine.

[Tải Podbag 0.3.0](https://github.com/SteelCrab/podbag/releases/tag/v0.3.0)

## Học qua các bài thực hành Podbag

Mở **Training** trong Desktop. Bốn mô-đun hướng dẫn chạy container, đưa một trang web lên cổng cục bộ, lưu tệp trong volume và thay thế dịch vụ web. Làm theo từng hướng dẫn để cài mô-đun. Desktop hiển thị tiến độ và chạy bài tập trong từng phiên thực hành riêng. [Chạy container đầu tiên (tiếng Anh)](/blog/container-basics/)

![Podbag Desktop hiển thị các mô-đun nhập môn và lệnh cần chạy](https://podbag.dev/blog/web-basics/start-en.png)

## Làm việc trong terminal

Dùng `podbag tui` để tạo volume, đăng nhập registry, nhập image hoặc xem tài nguyên Kubernetes. CLI bổ sung `podbag engine`, `podbag import`, `podbag kube`, `podbag settings` và `podbag tutorial`.

Cài CLI trên Linux hoặc máy Mac dùng chip Apple. Trình cài đặt kiểm tra mã SHA-256 của tệp tải về.

```sh
curl -fsSL https://podbag.dev/install.sh | PODBAG_VERSION=v0.3.0 sh
podbag --version
```

[Nhật ký thay đổi đầy đủ](https://github.com/SteelCrab/podbag/blob/v0.3.0/CHANGELOG.md#v030-2026-11-21)
