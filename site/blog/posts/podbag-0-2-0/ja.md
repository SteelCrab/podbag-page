---
title: "Podbag 0.2.0 リリース"
date: 2026-11-21
author: team
categories: [announcements]
tags: [release, kubernetes, migration, registries, desktop]
summary: "レジストリからのイメージ取得、Dockerfile からのビルド、Kubernetes ランタイム、エンジン間とクラスタ間の移行に対応しました。"
image: card-ja.png
image_alt: "Podbag 0.2.0 リリース"
draft: false
---

Podbag 0.2.0 を公開しました。イメージをビルドしてレジストリに公開できます。既存のイメージやデータも別のエンジンや Kubernetes クラスタにコピーできます。

## イメージのビルドと取得

`podbag build` は Dockerfile からイメージをビルドします。レジストリからイメージを取得したり、ビルドしたイメージをプッシュしたりできます。

![2 行の Alpine Dockerfile と Hello from Podbag を出力したターミナル](build-example.png "Dockerfile からイメージをビルドして実行します。")

Podbag Desktop でイメージ取得画面を開き、Docker Hub、GitHub Container Registry、または任意のレジストリを選びます。イメージ名とタグを入力します。非公開イメージには、アクセス権のある既存の Docker ログインを使えます。

![Docker Hub、GitHub、Amazon ECR が表示されたレジストリ一覧](registry-en.png "Podbag Desktop で取得元のレジストリを選びます。")

## エンジン間とクラスタ間のコピー

`podbag migrate` または Desktop の移行メニューで、単一プラットフォームのイメージ、停止中のコンテナ、ローカルボリュームを Docker 互換エンジン間でコピーできます。コピー元は残ります。

![pgdata のコピー元に Docker、コピー先に Podbag を指定した画面](engine-copy-en.png "pgdata ボリュームを Docker から Podbag にコピーします。")

Desktop は Kubernetes コンテキスト間で単独の Pod、Service、Deployment、ファイルシステム型の PVC をコピーします。ボリュームに結び付いた PVC ではファイルも転送し、コピー先で確認します。コピーの前に、元のボリュームへ書き込む処理を止めてください。 [移行の要件](https://github.com/SteelCrab/podbag/blob/v0.2.0/docs/usage.md#migrate-between-engines-or-kubernetes-clusters)

![qa-a から qa-b にコピーしたボリュームの検証が完了した画面](cluster-copy.png "Kubernetes クラスタ間のボリュームコピーを確認します。")

## Kubernetes、Swarm、Desktop

Linux ノードでは `podbag cri serve` を Kubernetes のコンテナランタイムとして使えます。 同じ k3s ノード上で Docker Engine と Podbag を比較した結果も公開しています。 [k3s 負荷試験](/ja/blog/k3s-30-pods-docker-podbag/)

![worker-1 で動作する web Pod の準備状態が 1/1 と表示された一覧](kubernetes-pods-en.png "Podbag Desktop で Pod の状態を確認します。")

単一ノードの Docker Swarm サービスとスタックにも対応します。

![Swarm を初期化し、Web サービスを 3 レプリカで作成し、タスクを表示するコマンド](swarm-example.png "Docker CLI を Podbag に接続した場合の例です。")

`podbag tui` と Desktop でコンテナやイメージを管理し、Docker CLI の接続先を切り替えられます。Apple シリコン搭載 Mac では、Desktop から Linux VM の CPU 数、メモリ、アイドル時の終了までの時間を設定できます。

![CPU、メモリ、アイドル時の終了までの時間を指定する設定画面](vm-settings.png "Desktop で macOS 上の Linux VM を設定します。")

## 0.2.0 のインストール

Linux または Apple シリコン搭載 Mac では、次のコマンドで 0.2.0 の CLI をインストールします。インストーラーはダウンロードの SHA-256 を検証します。

```sh
curl -fsSL https://podbag.dev/install.sh | PODBAG_VERSION=v0.2.0 sh
podbag --version
```

Desktop は Linux の AMD64 と ARM64 向けに DEB と RPM、Apple シリコン搭載 Mac 向けに ZIP を用意しています。Mac では CLI を先にインストールしてください。Windows CLI は試験的な機能で、WSL 2 が必要です。Android ARM64 の CLI はイメージ関連コマンドに対応します。 [0.2.0 のダウンロード](https://github.com/SteelCrab/podbag/releases/tag/v0.2.0)

0.1.0 で保存したイメージにファイルの更新日時や crontab の問題がある場合、イメージを削除し、再取得または再読み込みしてください。 [変更履歴](https://github.com/SteelCrab/podbag/blob/v0.2.0/CHANGELOG.md#v020-2026-11-20)
