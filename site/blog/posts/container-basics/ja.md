---
title: "Podbag Training · 最初のコンテナを実行する"
date: 2026-11-21
author: team
categories: [how-to]
tags: [cli, containers, desktop, training]
summary: "CLI で小さな Web サーバーを起動し、Podbag Desktop で停止します。同じターミナルで状態を確認します。"
image: running-en.png
image_alt: "Podbag Desktop で実行中の hello-web コンテナ"
outline: "実習の流れ"
draft: false
---

イメージには、プログラムに必要なファイルが入っています。コンテナは、そのイメージからプログラムを実行します。この実習では、`hello-web` という小さな Web サーバーを実行し、Podbag Desktop で停止します。

![ターミナルが実習環境で busybox イメージから hello-web コンテナを実行し、Podbag Desktop がそれを停止します](architecture-ja-light.svg)

## 初心者コース

**最初のコンテナを実行する** → [ブラウザーで Web サーバーを開く](../web-basics/) → [コンテナが変わってもファイルを残す](../volume-persistence/) → [Web サービスを入れ替えて片付ける](../web-service-lifecycle/)

## 実習モジュールをインストールする

[container-basics.podbag をダウンロード](https://github.com/SteelCrab/podbag/releases/download/training/container-basics/v1.0.0/container-basics.podbag)します。Training に対応した Podbag Desktop を開きます。**Training** の上部にある**モジュールをインストール**を選び、ダウンロードしたファイルを指定して確認します。ダウンロード先のフォルダーで次のコマンドを実行してもインストールできます。

```sh
podbag lab install container-basics.podbag
```

![インストール前に、選んだモジュールとファイルが表示されます](install-en.png)

このモジュールをインストール済みの場合も、新しいファイルを上書きでインストールできます。完了の記録は残ります。インストール済みのモジュールは `podbag lab list` で確認できます。

## 実習を開始する

サイドバーの **Training** を展開し、**コンテナを実行する**を選びます。現在の手順と、その後の手順が表示されます。次のコマンドをコピーし、お使いのターミナルで実行します。`container-lab $` が表示されたら続けます。

```sh
podbag lab start container-basics
```

![コンテナモジュールの開始コマンドと実習の手順](training-en.png)

## CLI で Web サーバーを実行する

実習ターミナルで次のコマンドを入力します。初回の実行では、Podbag が実習用のイメージをダウンロードします。

```sh
podbag run -d --name hello-web --network none docker.io/library/busybox:1.37.0 httpd -f -p 8080
```

`-d` はコンテナをバックグラウンドで実行します。`--name hello-web` はコンテナに名前を付けます。サーバーはコンテナ内のポート 8080 で待ち受けます。この実習ではコンテナの起動と停止を学びます。そのため、このコマンドはサーバーをホストのネットワークから切り離します。

![実習ターミナルに新しいコンテナ ID が表示されます](cli-run.png)

## Desktop でコンテナを停止する

実習ターミナルは開いたままにします。Desktop で**実習コンテナ**を選びます。実行中の `hello-web` を探し、その行の**停止**を選びます。コンテナの詳細を開いて**停止**を選ぶこともできます。

![実習コンテナに実行中の hello-web と停止ボタンが表示されます](running-en.png)

コンテナの行に**停止**と表示されます。**Training** でモジュールを選ぶと、**CLI で状態を確認する**の手順とコマンドが表示されます。コマンドをコピーします。

![実習コンテナの行で hello-web が停止しています](stopped-en.png)

## CLI で結果を確認する

同じ実習ターミナルに戻り、すべてのコンテナを一覧表示します。`-a` オプションを付けると、停止したコンテナも表示されます。

```sh
podbag ps -a
```

![Training で CLI の状態確認の手順が強調され、そのコマンドが表示されます](progress-en.png)

`hello-web` が `Exited` になっていることを確認します。実習ターミナルに `Verified` と表示されます。

![CLI に hello-web の Exited と確認済みのメッセージが表示されます](cli-check.png)

## 実習を終了する

`exit` と入力します。Podbag は実習用のコンテナ、ダウンロードしたイメージ、一時ストアを削除します。モジュールと完了の記録は Training に残ります。

![片付けの後、すべての手順が完了と表示されます](complete-en.png)

[次のモジュール · ブラウザーで Web サーバーを開く](../web-basics/)
