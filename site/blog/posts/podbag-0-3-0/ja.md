---
title: "Podbag 0.3.0 リリース"
date: 2026-11-21
author: team
categories: [announcements]
tags: [release, desktop, windows, training, tui]
summary: "Windows に Podbag Desktop をインストールできます。Apple シリコンでは同梱のエンジンで Linux VM を起動します。4 つの実習でコンテナの基本を学べます。"
image: card-ja.png
image_alt: "Podbag 0.3.0 リリース"
draft: false
---

Podbag 0.3.0 を公開しました。Windows 用のインストーラー、エンジンを同梱した macOS 用 Desktop バンドル、初心者向けの実習 4 つを追加しました。

## Podbag Desktop をインストールする

- **Windows x86_64 と ARM64。** CPU に合った MSI をダウンロードします。スタートメニューから **Podbag Desktop** を開きます。コンテナを実行するには WSL 2 を有効にします。
- **Apple シリコン搭載の Mac。** Desktop の ZIP を展開し、`podbag.app` を開きます。Desktop は同梱のエンジンで Linux VM を起動します。
- **Linux x86_64 と ARM64。** ディストリビューションと CPU に合った DEB または RPM をインストールします。パッケージにはエンジンが含まれます。

[Podbag 0.3.0 をダウンロード](https://github.com/SteelCrab/podbag/releases/tag/v0.3.0)

## Podbag の実習で学ぶ

Desktop で **Training** を開きます。4 つのモジュールで、コンテナの実行、ローカル Web ページの公開、ボリュームへのファイル保存、Web サービスの入れ替えを学びます。各ガイドに従ってモジュールをインストールします。Desktop は分離された実習環境で手順を実行し、進捗を表示します。 [最初のコンテナを実行する（英語）](/blog/container-basics/)

![Podbag Desktop に初心者向けの実習と現在のコマンドが表示されている](https://podbag.dev/blog/web-basics/start-en.png)

## ターミナルから操作する

`podbag tui` でボリュームを作成し、レジストリへのログイン、イメージのインポート、Kubernetes リソースの確認を行えます。CLI には `podbag engine`、`podbag import`、`podbag kube`、`podbag settings`、`podbag tutorial` が加わりました。

Linux または Apple シリコン搭載の Mac に CLI をインストールします。インストーラーはダウンロードしたファイルの SHA-256 チェックサムを検証します。

```sh
curl -fsSL https://podbag.dev/install.sh | PODBAG_VERSION=v0.3.0 sh
podbag --version
```

[変更履歴](https://github.com/SteelCrab/podbag/blob/v0.3.0/CHANGELOG.md#v030-2026-11-21)
