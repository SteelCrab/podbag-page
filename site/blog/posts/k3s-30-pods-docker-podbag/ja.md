---
title: "k3sでウェブPodを30個動かすとDockerとPodbagはどう違うか"
date: 2026-11-20
author: steelcrab
categories: [benchmarks, engineering]
tags: [k3s, kubernetes, docker, nginx, aws]
summary: "同じノードにウェブプロキシ6個とAPIレプリカ24個を配置し、起動から準備完了までの時間とHTTP応答時間を測りました。"
image: card-ja.png
image_alt: "k3sでウェブPodを30個動かすとDockerとPodbagはどう違うか"
draft: false
---

デプロイ後、いつリクエストを受け付けられるでしょうか。稼働中の応答時間にも差が出るでしょうか。同じk3sノードでコンテナランタイムを切り替えて測定しました。

## 測定した構成

6個のウェブPodがKubernetes Serviceを通して24個のAPI Podへ転送します。APIは自分のPod名を返します。ノード上のクライアントはウェブServiceのClusterIPに接続します。ステータスが200で本文がAPIのPod名の場合に成功と数えます。

![ローカルノードで測定した経路。ランタイムを一つずつ実行しました。](measured-layout.svg "ローカルノードで測定した経路。ランタイムを一つずつ実行しました。")

両方の層で同じNGINXイメージとHTTPの準備完了プローブを使います。コンテナの要求はCPU 20m、メモリ16 MiBで、上限は200mと48 MiBです。Docker Engineはk3s内蔵のcri-dockerd、Podbagは専用のCRIソケットで接続します。

Ubuntu 26.04.1 LTS · Linux 7.0.0-43-generic · ARM64 · 4 vCPU · 4 GiB · k3s v1.37.2+k3s1 · Docker Engine 29.1.3 · [Podbag c0ff5eb](https://github.com/SteelCrab/podbag/commit/c0ff5ebdbd8762760652fbe0a869655a105557a9)

## 測定結果

| 指標 | Docker Engine | Podbag |
|---|---:|---:|
| 30個すべてが準備完了 | {{n:3.39}} s | {{n:2.48}} s |
| 固定負荷でのHTTP p95 | {{n:1.41}} ms | {{n:1.26}} ms |
| 短い集中負荷でのHTTP p95 | {{n:3.46}} ms | {{n:3.69}} ms |
| 集中負荷での成功応答数/秒 | {{n:7019}} | {{n:6330}} |
| 検証済みの応答 | {{n:33600}} / {{n:33600}} | {{n:33600}} / {{n:33600}} |

このノードでは、準備完了までの中央値はPodbagで {{n:0.91}} 秒速くなりました。毎秒240件での各回のp95はDockerが {{n:1.20}}–{{n:1.60}} ms、Podbagが {{n:0.93}}–{{n:1.88}} msでした。全回で24個のAPI Podが応答しました。 短い集中負荷ではDockerの処理件数の中央値が高くなりました。各回の処理件数の範囲は重なっています。

![白丸は各回、菱形は中央値です。上段は準備時間、下段は毎秒240件でのHTTP p95です。](trials.png "白丸は各回、菱形は中央値です。上段は準備時間、下段は毎秒240件でのHTTP p95です。")

最初のスケール要求の直前に計測を開始し、二つのDeploymentで計30個が準備完了になるまで100ミリ秒ごとに確認します。次に有効なエンドポイント30個を確認し、2秒待ちます。12クライアントがそれぞれ新しいTCP接続で100回要求します。p95は成功した要求の95%が完了した時間です。

集中負荷の後は2秒待ち、12クライアントがそれぞれ毎秒20回、約30秒間要求を送りました。目標は合計で毎秒240回です。p95は区間ごとに算出しました。

順序はDocker → Podbag → Podbag → Dockerです。各区間で1回予熱し、2回測定しました。表はランタイムごとに4回の中央値を示し、成功応答は合計を示します。イメージはキャッシュ済みです。クライアントとサーバーは同じVMのCPUを使います。短いAPI応答だけを返し、データベース処理や外部通信は測定していません。

この結果は単一ノードでの展開とHTTP応答の測定です。集中負荷の処理件数にはクライアントとネットワークも影響します。継続的な最大処理能力を推定するには短い区間です。

## イメージの指定方法が与えた影響

予備試験では複数アーキテクチャのNGINXインデックスと `IfNotPresent` を使用しました。PodbagはARM64イメージを保持していましたが、CRIがインデックスのダイジェストで照会すると見つからず、kubeletが再取得して速度制限に達しました。本測定は両ランタイムでARM64マニフェストのダイジェストを確認し、`imagePullPolicy: Never` を使用しました。各区間の前にVMを再起動し、新しいクラスタを作成しました。

## AWSへの配置例

![AWSの配置例です。EC2ワーカーとロードバランサーは測定の対象外です。](aws-layout.svg "AWSの配置例です。EC2ワーカーとロードバランサーは測定の対象外です。")

インターネット向けApplication Load Balancerを二つのアベイラビリティーゾーンのパブリックサブネットに接続します。HTTPSのトラフィックはプライベートサブネットのEC2ワーカー上のウェブServiceのNodePortに転送します。Deploymentにゾーン単位の分散制約を設定し、各ゾーンにウェブ3個、API 12個を配置します。APIは内部のClusterIPで公開します。図はアプリの通信経路です。

[AWS Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html) · [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/)

## 再現用の資料

[ワークロード](workload.json) · [測定スクリプト](measure.py) · [各回のデータ](results.jsonl) · [ノード設定と実行順序](reproduce.txt) · [start-node.sh](start-node.sh)

[k3s · Docker](https://docs.k3s.io/advanced#using-docker-as-the-container-runtime) · [Podbag CRI](https://github.com/SteelCrab/podbag/blob/c0ff5ebdbd8762760652fbe0a869655a105557a9/docs/usage.md)
