---
title: "実習 · CLI で作ったボリュームを TUI で削除する"
date: 2026-11-20
author: team
categories: [how-to]
tags: [cli, tui, tutorials, volumes]
summary: "実際の CLI と TUI を使ってボリュームを作成、確認、削除します。"
image: volumes.png
image_alt: "my-api · Volumes"
draft: false
---

`podbag lab --help` が使える Podbag を用意します。ファイルをダウンロードし、そのフォルダーでターミナルを開きます。実習は専用の一時ストアを使います。

[実習モジュールをダウンロード](cli-tui-volumes.podbag)

## モジュールをインストールする

ダウンロードしたファイルをインストールします。Desktop のチュートリアル画面からも選択できます。

```sh
podbag lab install cli-tui-volumes.podbag
```

![モジュールをインストールする · podbag lab install](install.png)

## 実習シェルを開く

起動したら `volume-lab $` を確認し、このシェルで作業します。

```sh
podbag lab start --lang ja
```

![実習シェルを開く · volume-lab](shell-ja.png)

## ボリュームを作成する

`my-api` を作成し、一覧の `VOLUME NAME` に表示されることを確認します。

```sh
podbag volume create my-api
podbag volume ls
```

![ボリュームを作成する · my-api](create.png)

## TUI で探す

同じシェルで TUI を起動します。`Tab` で **Volumes** を開き、`my-api` を選択します。

```sh
podbag tui
```

![TUI で探す · Volumes](volumes.png)

## 詳細を確認する

`Enter` で **Inspect** を開きます。`Name` と `Mountpoint` を確認し、`Esc` で戻ります。

![詳細を確認する · Mountpoint](inspect.png)

## ボリュームを削除する

`my-api` で `d` を押し、確認画面の名前を見てから `y` を押します。

![ボリュームを削除する · my-api](remove.png)

## 空の一覧を確認する

**No volumes on this engine.** を確認し、`q` でシェルに戻ります。

![空の一覧を確認する · No volumes on this engine.](empty.png)

## 実習を終了する

一覧を再表示します。`Verified` が出たら `exit` を入力します。サービスと一時ファイルが削除されます。

```sh
podbag volume ls
exit
```

![実習を終了する · Verified](finish.png)

## モジュールを削除する

元のシェルで実行すると、モジュールと完了記録を削除できます。

```sh
podbag lab remove
```

![モジュールを削除する · Module removed.](uninstall.png)
