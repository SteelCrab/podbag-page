---
title: "実習 · CLI と GUI でボリュームを管理する"
date: 2026-11-20
author: team
categories: [how-to]
tags: [cli, desktop, tutorials, volumes]
summary: "CLI で作成したボリュームを Desktop で確認し、削除します。実習画面には現在の作業が表示されます。"
image: gui-volumes-ja.png
image_alt: "実習ボリューム · my-api"
draft: false
---

CLI で作成したボリュームを Desktop で確認し、削除します。実習画面には現在の作業が表示されます。

[実習モジュールをダウンロード](cli-gui-volumes.podbag)

## ボリュームとは？

ボリュームはコンテナとは別にファイルを保存する領域です。ここでは `app-a` が `my-api` ボリュームに `note.txt` を保存します。`app-a` を削除しても、新しいコンテナ `app-b` に同じボリュームをマウントすると、そのファイルを読み取れます。 ボリューム自体を削除すると、中のファイルも消えます。

[![ボリュームとは？](volume-life.webp)](volume-life.mp4)

## モジュールをインストールする

対応する Desktop と CLI を使います。下のファイルをチュートリアル画面で選んでインストールするか、ダウンロード先で次のコマンドを実行します。

```sh
podbag lab install cli-gui-volumes.podbag
```

![モジュールをインストールする](gui-install.png)

## Desktop で実習を開く

Desktop の **Training** で **ウェブの実習ガイド**を選ぶとこのページに戻れます。Training にはモジュールの状態と現在の作業が表示されます。

![Training のボリューム実習と操作ボタン](gui-ready-ja.png)

## 実習シェルを開く

Desktop のサイドバーで実習ボリュームを開き、ターミナルボタンを選びます。実習中はターミナルとこのページを開いておきます。

![ターミナル起動後の実習ボリューム](gui-shell-ja.png)

## CLI でボリュームを作成

volume-lab のプロンプトで次のコマンドを入力します。

```sh
podbag volume create my-api
podbag volume ls
```

![podbag volume ls · my-api](gui-create.png)

## GUI で詳細を確認

作成したボリュームが表示されます。Training では GUI で詳細を開く作業が進行中になります。

![実習ボリューム · my-api](gui-volumes-ja.png)

実習ボリュームで my-api を選び、名前と保存先を確認します。

![my-api · Mountpoint](gui-inspect-ja.png)

## GUI で削除

my-api の削除を選び、確認画面で名前を確認して削除します。

![GUI で削除 · my-api](gui-dialog-ja.png)

削除すると一覧が空になります。同じ実習ターミナルに戻ります。

![CLI で削除を確認 · 進行中](gui-empty-ja.png)

## CLI で削除を確認

実習シェルで一覧を再表示します。

```sh
podbag volume ls
```

![実習を終了 · 進行中](gui-verified-ja.png)

## 実習を終了

`Verified` が表示されたら `exit` で一時ストアを片付けます。Training に完了と表示されます。

```sh
exit
```

![Verified · exit](gui-finish.png)

![実習の進捗 · 完了](gui-complete-ja.png)

## モジュールを削除する

元のシェルで実行すると、モジュールと完了記録を削除できます。

```sh
podbag lab remove volume-basics
```

![モジュールを削除する · Module removed.](uninstall.png)
