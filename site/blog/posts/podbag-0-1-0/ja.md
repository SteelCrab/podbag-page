---
title: "podbag 0.1.0：デーモンなし、ファイル単位で保存するコンテナ"
date: 2026-11-20
author: team
categories: [announcements]
tags: [release, docker, compose, rootless, macos, windows]
summary: "podbag の最初のリリースを公開しました。1つの静的バイナリで Docker と OCI のコンテナをデーモンなしで動かし、イメージをファイル単位で保存します。ディスクもメモリも少なく、コンテナは約 4 ms で起動します。"
image: card-ja.png
image_alt: "podbag 0.1.0：デーモンなし、ファイル単位で保存するコンテナ"
draft: false
---

本日、podbag の最初のバージョン podbag 0.1.0 をリリースしました。

podbag はコンテナエンジンです。1つの静的バイナリで、Docker と OCI のイメージを動かします。デーモンはありません。イメージをレイヤー単位ではなく、ファイル単位で保存します。

時間がなければ、[30秒の紹介動画](/media/intro.mp4)（英語）をご覧ください。

## podbag とは

- **デーモンなし。** コンテナが動いていないときは、何も動きません。
- **1つの静的バイナリ。** Linux で約 4 MB です。
- **レイヤーではなくファイル。** 多くのイメージが共有するファイルは、1回だけ保存し、1回だけキャッシュします。
- **速い。** Linux ではコンテナが約 4 ms で起動します。
- **Docker のツールで使える。** `docker` CLI、Compose、buildx に対応します。
- **root でも root なしでも。** 同じプログラムがどちらでも動きます。
- **Linux、macOS、Windows。** Windows 対応は試験的です。

## デーモンなし

Docker は、1つのクライアントと2つのデーモンでできています。`dockerd` と `containerd` は、コンテナがあってもなくても常に動いています。コンテナがなくても {{n:203}} MiB を使います。

podbag は1つのプログラムです。

- `podbag` コマンドが、コンテナを自分で用意して、すぐに終わります。
- ユーザーごとに小さな keeper が1つ（約 2 MiB）あり、動いているコンテナを見守ります。ログを書き、`stop`、`kill`、`wait` に応えます。
- keeper は最初のコンテナと一緒に起動します。最後のコンテナが終わってから10秒後に止まります。
- コンテナがないときは、何も動きません。

## レイヤーではなくファイル

![2つのイメージが、ほとんどのファイルを共有しています。レイヤー方式では、イメージ B の一番上のレイヤーでファイルが1つ違うだけで、共有していたファイルももう一度保存され、8ファイルになります。podbag は各ファイルを1回だけ保存し、6ファイルです。](/images/storage-ja-light.svg "レイヤーとファイル：ファイルが1つ変わると、レイヤー方式はレイヤー全体をもう一度保存します。")

ほかのエンジンは、イメージをレイヤーとして保存します。レイヤーは、全体が同じときだけ1回で済みます。中のファイルが1つ変わると、レイヤー全体をもう一度保存します。

podbag はレイヤーをファイルに分け、各ファイルを1回だけ保存します。イメージは、それらのファイルを指すパスの一覧です。2つのコンテナが同じファイルを読むと、同じ inode を読むので、カーネルはそのファイルを1回だけキャッシュします。

Spring サービス8個・2リリースで測りました。

<!-- compare-columns: podbag docker -->
| | podbag | Docker | podbag の節約 |
|---|--:|--:|--:|
| 2リリース分のディスク | {{n:902}} MiB | {{n:2970}} MiB | 70% |
| サービス16個の起動時のページキャッシュ | {{n:324}} MiB | {{n:982}} MiB | 67% |

ダウンロード量は変わりません。レジストリはレイヤーを送り、podbag はレイヤーをまるごと受け取ってからファイルに分けます。

## 起動時間とメモリ

![1台の Linux VM で podbag を Docker、Podman、Kiri と比べた結果：起動時間、コンテナ100個のメモリ、コンテナがないときのメモリ、ディスク、ページキャッシュ。](/images/perf.svg "podbag と Docker、Podman、Kiri の比較アニメーション（英語）。")

すべてのツールを、同じ Linux VM で動かしました。CPU 4個、{{n:3.8}} GiB、arm64 です。バージョンは podbag 0.1.0、Podman 5.7.0、Docker 29.1.3、Kiri 0.2.1 です。数字は中央値です。低いほど良い結果です。

<!-- compare-columns: podbag podbag kiri podman docker -->
| | podbag (rootless) | podbag (root) | Kiri | Podman | Docker |
|---|--:|--:|--:|--:|--:|
| コンテナの起動 | {{n:4.1}} ms | {{n:4.4}} ms | {{n:9.1}} ms | {{n:46.4}} ms | {{n:73.8}} ms |
| コンテナ100個のメモリ | {{n:117}} MiB | {{n:105}} MiB | {{n:109}} MiB | {{n:203}} MiB | {{n:562}} MiB |
| コンテナがないときのプロセス | {{n:0}} | {{n:0}} | {{n:1}}個（{{n:5.9}} MiB） | {{n:1}}個（{{n:0.6}} MiB） | {{n:4}}個（{{n:203}} MiB） |

- keeper がまだないときの最初の起動は、{{n:12.8}}–{{n:16.0}} ms かかります。
- メモリは Kiri と近い値です。コンテナがないときは podbag が上です。そのとき podbag は何も動いていないからです。
- すべての数字と測り方：[ベンチマーク](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks.md)と [Spring マイクロサービスのベンチマーク](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks-msa.md)（英語）。
- 同じ比較を動画で：[perf.mp4](/media/perf.mp4)（英語）。

## Docker のツールで使える

`podbag system service` は、ソケットで Docker Engine API を提供します。`docker` CLI、Compose、buildx は、このソケットで podbag を使います。

```sh
podbag system service &
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podbag/docker.sock
docker compose up -d
```

- これはデーモンではありません。コンテナはこのサービスに依存しません。
- クライアントがないと、60秒後に止まります。
- systemd があれば、最初の接続で起動できます。

## root でも root なしでも

- 同じプログラムがどちらでも動きます。
- root のとき、podbag は composefs でイメージをマウントします。
- root なしでは、ハードリンクのツリーを作り、`pasta` がコンテナをネットワークにつなぎます。
- `podbag check` は、システムにまだ必要なものと、その追加方法を表示します。

## Linux、macOS、Windows

- **Linux：** x86_64 と arm64。Linux 5.12 以降と cgroup v2 が必要です。
- **macOS**（Apple silicon）：podbag は専用の小さな Linux VM を動かします。最初のコマンドで、約0.5秒で VM が起動します。最後のコンテナから60秒後に VM は電源を切ります。最後のコンテナから6分後、podbag が使っていた Mac のメモリは {{n:1.7}} MiB でした。
- **Windows**（x86_64、arm64）：試験的です。podbag は専用の WSL 2 ディストリビューションで Linux エンジンを動かします。CI でビルドとテストをしていますが、実際の Windows マシンではまだ試していません。

## インストール

Linux と macOS：

```sh
curl -fsSL https://podbag.dev/install.sh | sh
```

スクリプトは、システムに合うファイルをダウンロードし、SHA-256 を確認して、`/usr/local/bin` にインストールします。

[リリースページ](https://github.com/SteelCrab/podbag/releases/tag/v0.1.0)からファイルを直接取得することもできます。`SHA256SUMS` で確認してください。

| システム | ファイル |
|---|---|
| Linux、x86_64 | `podbag-x86_64-linux` |
| Linux、arm64 | `podbag-aarch64-linux` |
| macOS、Apple silicon | `podbag-aarch64-macos` |
| Windows、x86_64（試験的） | `podbag-x86_64-windows.exe` |
| Windows、arm64（試験的） | `podbag-aarch64-windows.exe` |

次に、最初のコンテナを動かしてみましょう。

```sh
podbag run --rm alpine echo hello
```

## 0.1.0 の制限

最初のリリースなので、まだないものがあります。

- **ビルド：** Dockerfile のビルドは buildx（`docker buildx build`）だけです。従来のビルダーはありません。
- **レジストリ：** 公開イメージだけを取得します。ログイン、非公開イメージの取得、push はありません。
- **Docker のコマンド：** `commit`、`export`、`diff`、`stats`、`top`、`pause`、`rename`、`update` はありません。
- **Swarm：** swarm モードとプラグインはありません。
- **Kubernetes：** CRI がないので、Kubernetes のノードは podbag をランタイムとして使えません。
- **Windows：** 試験的です。Windows の `docker` CLI は、まだ podbag につながりません。
- **Mac の復帰：** VM の電源が切れたあとの最初のコマンドは、約{{n:0.6}}秒かかります。

## これから

次の作業は、[オープンなプルリクエスト](https://github.com/SteelCrab/podbag/pulls)で進めています。まだ完成しておらず、日付は決めていません。

- レジストリへのログイン、非公開イメージの取得、push、search
- Dockerfile のビルドと、`commit`、`export`、`diff`
- ノードが podbag でポッドを動かせる Kubernetes ランタイム
- 1ノードでの swarm モード
- `stats`、`top`、`pause`、`unpause`、`rename`、`update`
- ターミナル UI とデスクトップアプリ

## 試して、教えてください

- すべてのコマンドは[使い方ガイド](https://github.com/SteelCrab/podbag/blob/main/docs/usage.md)（英語）にあります。
- バグやアイデアは [GitHub のイシュー](https://github.com/SteelCrab/podbag/issues)へどうぞ。Windows マシンで試した結果が特に役立ちます。
- podbag は Apache License 2.0 のオープンソースです。
