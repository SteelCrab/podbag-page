---
title: "Podbag 0.3.0 发布"
date: 2026-11-21
author: team
categories: [announcements]
tags: [release, desktop, windows, training, tui]
summary: "在 Windows 上安装 Podbag Desktop，在配备 Apple 芯片的 Mac 上用内置引擎启动 Linux 虚拟机，并通过四项练习学习容器操作。"
image: card-zh-CN.png
image_alt: "Podbag 0.3.0 发布"
draft: false
---

Podbag 0.3.0 已发布。此版本新增 Windows 安装程序、内置引擎的 macOS 桌面应用包和四项入门练习。

## 安装 Podbag Desktop

- **Windows x86_64 和 ARM64。** 下载与 CPU 匹配的 MSI。从开始菜单打开 **Podbag Desktop**。运行容器需要启用 WSL 2。
- **配备 Apple 芯片的 Mac。** 解压 Desktop ZIP 并打开 `podbag.app`。Desktop 使用内置引擎启动 Linux 虚拟机。
- **Linux x86_64 和 ARM64。** 安装与发行版和 CPU 匹配的 DEB 或 RPM。安装包包含引擎。

[下载 Podbag 0.3.0](https://github.com/SteelCrab/podbag/releases/tag/v0.3.0)

## 通过 Podbag 练习学习

在 Desktop 中打开 **Training**。四个模块涵盖运行容器、发布本地网页、在卷中保留文件和替换 Web 服务。按照各指南安装模块。Desktop 在隔离的练习环境中运行任务，并显示进度。 [运行第一个容器（英文）](/blog/container-basics/)

![Podbag Desktop 显示入门练习列表和当前命令](https://podbag.dev/blog/web-basics/start-en.png)

## 在终端中管理

使用 `podbag tui` 创建卷、登录镜像仓库、导入镜像或查看 Kubernetes 资源。CLI 新增 `podbag engine`、`podbag import`、`podbag kube`、`podbag settings` 和 `podbag tutorial` 命令。

在 Linux 或配备 Apple 芯片的 Mac 上安装 CLI。安装程序会验证下载文件的 SHA-256 校验和。

```sh
curl -fsSL https://podbag.dev/install.sh | PODBAG_VERSION=v0.3.0 sh
podbag --version
```

[完整变更记录](https://github.com/SteelCrab/podbag/blob/v0.3.0/CHANGELOG.md#v030-2026-11-21)
