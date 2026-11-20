---
title: "podbag 0.1.0: container không daemon, lưu theo từng tệp"
date: 2026-11-20
author: team
categories: [announcements]
tags: [release, docker, compose, rootless, macos, windows]
summary: "Bản phát hành đầu tiên của podbag đã ra mắt. Một tệp nhị phân tĩnh chạy container Docker và OCI mà không cần daemon, và lưu image theo từng tệp: ít đĩa hơn, ít bộ nhớ hơn, khởi động trong khoảng 4 ms."
image: card-vi.png
image_alt: "podbag 0.1.0: container không daemon, lưu theo từng tệp"
draft: false
---

Hôm nay chúng tôi phát hành podbag 0.1.0, phiên bản đầu tiên của podbag.

podbag là một công cụ chạy container. Nó chạy image Docker và OCI của bạn từ một tệp nhị phân tĩnh. Nó không có daemon. Nó lưu image theo từng tệp, không theo từng lớp.

Không có nhiều thời gian? Hãy xem [phần giới thiệu 30 giây](/media/intro.mp4) (tiếng Anh).

## podbag là gì

- **Không daemon.** Khi không có container nào chạy, không có gì chạy cả.
- **Một tệp nhị phân tĩnh.** Khoảng 4 MB trên Linux.
- **Tệp, không phải lớp.** Một tệp mà nhiều image dùng chung chỉ được lưu và đệm một lần.
- **Nhanh.** Một container khởi động trong khoảng 4 ms trên Linux.
- **Dùng được với công cụ Docker.** CLI `docker`, Compose và buildx.
- **Có hoặc không có root.** Cùng một chương trình chạy được cả hai cách.
- **Linux, macOS và Windows.** Hỗ trợ Windows đang ở mức thử nghiệm.

## Không daemon

Docker gồm một client và hai daemon. `dockerd` và `containerd` luôn chạy, dù có container hay không. Khi không có container, chúng vẫn giữ {{n:203}} MiB.

podbag là một chương trình duy nhất:

- Lệnh `podbag` tự dựng từng container, rồi kết thúc.
- Mỗi người dùng có một keeper nhỏ (khoảng 2 MiB) trông các container đang chạy. Nó ghi log và trả lời `stop`, `kill` và `wait`.
- Keeper khởi động cùng container đầu tiên. Nó dừng 10 giây sau container cuối cùng.
- Khi không có container, không có gì chạy cả.

## Tệp, không phải lớp

![Hai image dùng chung phần lớn tệp. Với lớp, lớp trên cùng của image B chỉ khác một tệp, nên các tệp dùng chung bị lưu lại: 8 tệp. podbag lưu mỗi tệp một lần: 6 tệp.](/images/storage-vi-light.svg "Lớp và tệp: chỉ cần một tệp thay đổi, kho lưu theo lớp lưu lại cả lớp.")

Các công cụ khác lưu image theo lớp. Một lớp chỉ được lưu một lần khi cả lớp giống hệt. Khi một tệp trong đó thay đổi, cả lớp được lưu lại.

podbag tách mỗi lớp thành các tệp, và lưu mỗi tệp một lần. Một image là danh sách đường dẫn tới các tệp đó. Khi hai container đọc cùng một tệp, chúng đọc cùng một inode, nên kernel chỉ đệm tệp đó một lần.

Chúng tôi đo với 8 dịch vụ Spring ở 2 bản phát hành:

| | podbag | Docker | podbag tiết kiệm |
|---|--:|--:|--:|
| Đĩa cho cả hai bản phát hành | {{n:902}} MiB | {{n:2970}} MiB | 70% |
| Page cache để khởi động 16 dịch vụ | {{n:324}} MiB | {{n:982}} MiB | 67% |

Lượng tải về vẫn như cũ. Registry gửi các lớp, và podbag tải trọn mỗi lớp rồi mới tách thành tệp.

## Thời gian khởi động và bộ nhớ

![So sánh podbag với Docker, Podman và Kiri trên một VM Linux: thời gian khởi động, bộ nhớ cho 100 container, bộ nhớ khi không có container, đĩa và page cache.](/images/perf.svg "podbag so với Docker, Podman và Kiri, dạng hoạt hình (tiếng Anh).")

Chúng tôi chạy mọi công cụ trên cùng một VM Linux: 4 CPU, {{n:3.8}} GiB, arm64. Các phiên bản: podbag 0.1.0, Podman 5.7.0, Docker 29.1.3 và Kiri 0.2.1. Các con số là trung vị. Càng thấp càng tốt.

| | podbag (rootless) | podbag (root) | Kiri | Podman | Docker |
|---|--:|--:|--:|--:|--:|
| Khởi động một container | {{n:4.1}} ms | {{n:4.4}} ms | {{n:9.1}} ms | {{n:46.4}} ms | {{n:73.8}} ms |
| Bộ nhớ cho 100 container | {{n:117}} MiB | {{n:105}} MiB | {{n:109}} MiB | {{n:203}} MiB | {{n:562}} MiB |
| Tiến trình khi không có container | không có | không có | 1 ({{n:5.9}} MiB) | 1 ({{n:0.6}} MiB) | 4 ({{n:203}} MiB) |

- Lần khởi động đầu tiên, khi chưa có keeper, mất {{n:12.8}}–{{n:16.0}} ms.
- Về bộ nhớ, Kiri gần bằng podbag. podbag dẫn trước khi không có container, vì lúc đó không có gì của nó chạy.
- Mọi con số và cách đo: [đo hiệu năng](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks.md) và [đo hiệu năng với microservice Spring](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks-msa.md) (tiếng Anh).
- Cùng phép so sánh dưới dạng video: [perf.mp4](/media/perf.mp4) (tiếng Anh).

## Dùng được với công cụ Docker của bạn

`podbag system service` cung cấp Docker Engine API trên một socket. CLI `docker`, Compose và buildx nói chuyện với nó.

```sh
podbag system service &
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podbag/docker.sock
docker compose up -d
```

- Nó không phải daemon. Container không phụ thuộc vào nó.
- Nó dừng sau 60 giây không có client.
- Với systemd, nó có thể khởi động ở kết nối đầu tiên.

## Có hoặc không có root

- Cùng một chương trình chạy được cả hai cách.
- Khi có root, podbag gắn image bằng composefs.
- Khi không có root, nó tạo cây liên kết cứng, và `pasta` nối container vào mạng.
- `podbag check` liệt kê những gì hệ thống của bạn còn thiếu, và cách thêm vào.

## Linux, macOS và Windows

- **Linux:** x86_64 và arm64. Linux 5.12 trở lên, có cgroup v2.
- **macOS** (Apple silicon): podbag chạy một VM Linux nhỏ của riêng nó. Lệnh đầu tiên khởi động VM trong khoảng nửa giây. VM tắt 60 giây sau container cuối cùng. Sáu phút sau container cuối cùng, podbag chỉ giữ {{n:1.7}} MiB bộ nhớ của máy Mac.
- **Windows** (x86_64 và arm64): thử nghiệm. podbag chạy công cụ Linux của nó trong một bản phân phối WSL 2 riêng. Nó được build và kiểm thử trong CI, nhưng chưa được thử trên máy Windows thật.

## Cài đặt

Trên Linux và macOS:

```sh
curl -fsSL https://podbag.dev/install.sh | sh
```

Script tải tệp phù hợp với hệ thống của bạn, kiểm tra tổng SHA-256, và cài vào `/usr/local/bin`.

Bạn cũng có thể lấy tệp từ [trang phát hành](https://github.com/SteelCrab/podbag/releases/tag/v0.1.0). Kiểm tra bằng `SHA256SUMS`.

| Hệ thống | Tệp |
|---|---|
| Linux, x86_64 | `podbag-x86_64-linux` |
| Linux, arm64 | `podbag-aarch64-linux` |
| macOS, Apple silicon | `podbag-aarch64-macos` |
| Windows, x86_64 (thử nghiệm) | `podbag-x86_64-windows.exe` |
| Windows, arm64 (thử nghiệm) | `podbag-aarch64-windows.exe` |

Sau đó, chạy container đầu tiên của bạn:

```sh
podbag run --rm alpine echo hello
```

## Giới hạn của 0.1.0

Đây là bản phát hành đầu tiên. Một số thứ chưa có:

- **Build:** Dockerfile chỉ build được qua buildx (`docker buildx build`). Không có builder cổ điển.
- **Registry:** podbag chỉ kéo image công khai. Không có đăng nhập, không kéo image riêng tư và không push.
- **Lệnh Docker:** không có `commit`, `export`, `diff`, `stats`, `top`, `pause`, `rename` hay `update`.
- **Swarm:** không có chế độ swarm, và không có plugin.
- **Kubernetes:** không có CRI, nên node Kubernetes không thể dùng podbag làm runtime.
- **Windows:** thử nghiệm. CLI `docker` trên Windows chưa kết nối được với podbag.
- **Đánh thức trên Mac:** lệnh đầu tiên sau khi VM tắt mất khoảng {{n:0.6}} s.

## Sắp tới

Công việc cho những mục này nằm trong các [pull request đang mở](https://github.com/SteelCrab/podbag/pulls). Chúng chưa xong, và chúng tôi không hứa ngày:

- đăng nhập registry, kéo image riêng tư, push và search;
- build Dockerfile, và `commit`, `export`, `diff`;
- runtime cho Kubernetes, để node chạy pod của nó bằng podbag;
- chế độ swarm trên một node;
- `stats`, `top`, `pause`, `unpause`, `rename` và `update`;
- giao diện terminal và ứng dụng desktop.

## Hãy thử và cho chúng tôi biết

- Đọc [hướng dẫn sử dụng](https://github.com/SteelCrab/podbag/blob/main/docs/usage.md) (tiếng Anh) để xem mọi lệnh.
- Báo lỗi và ý tưởng trong [GitHub issues](https://github.com/SteelCrab/podbag/issues). Báo cáo từ máy Windows giúp ích nhiều nhất.
- podbag là phần mềm mã nguồn mở, theo Apache License 2.0.
