---
title: "Paglabas ng Podbag 0.2.0"
date: 2026-11-21
author: team
categories: [announcements]
tags: [release, kubernetes, migration, registries, desktop]
summary: "Mag-pull mula sa mga registry, mag-build mula sa Dockerfile, magpatakbo ng Kubernetes pod sa Linux, at magkopya sa pagitan ng mga engine at cluster."
image: card-fil.png
image_alt: "Paglabas ng Podbag 0.2.0"
draft: false
---

Available na ang Podbag 0.2.0. Maaari ka nang mag-build ng image at i-push ito sa isang registry. Maaari mo ring kopyahin ang mga kasalukuyang image at data sa ibang engine o Kubernetes cluster.

## Pag-build at pag-pull ng image

Gamitin ang `podbag build` para mag-build ng image mula sa Dockerfile. Maaari kang mag-pull mula sa isang registry o mag-push ng mga image na na-build mo.

Sa Podbag Desktop, buksan ang **Pull image**. Piliin ang Docker Hub, GitHub Container Registry, o ilagay ang address ng sarili mong registry. Ilagay ang pangalan at tag ng image. Para sa pribadong image, puwede mong gamitin ang Docker login na may access sa registry.

![Mga pagpipiliang registry sa dialog ng Podbag Desktop para sa pag-pull ng image](/images/pull-registries-en.png)

## Pagkopya sa pagitan ng mga engine at cluster

Gamitin ang `podbag migrate` o ang menu na **Migrate** sa Desktop para kopyahin ang mga single-platform image, nakahintong container, at lokal na volume sa pagitan ng mga engine na compatible sa Docker. Mananatili ang pinagmulan.

Makokopya rin ng Desktop ang mga standalone na Pod, Service, Deployment, at filesystem persistent volume claim (PVC) sa pagitan ng mga Kubernetes context. Kung nakatali na ang filesystem PVC sa isang volume, ililipat din ang mga file at susuriin ang mga ito sa destinasyon. Ihinto muna ang mga workload na nagsusulat sa pinagmulan. [Mga kailangan sa migration](https://github.com/SteelCrab/podbag/blob/v0.2.0/docs/usage.md#migrate-between-engines-or-kubernetes-clusters)

## Kubernetes, Swarm, at Desktop

Sa isang Linux node, gamitin ang `podbag cri serve` bilang container runtime ng Kubernetes. Maaari ring magpatakbo ng Docker Swarm service at stack sa iisang node. Inihambing namin ang Docker Engine at Podbag sa parehong k3s node. [Pagsubok sa k3s](/fil/blog/k3s-30-pods-docker-podbag/)

Gamitin ang `podbag tui` o Desktop para pamahalaan ang mga container at image at palitan ang Docker CLI context. Sa Mac na may Apple silicon, maaaring itakda sa Desktop ang CPU, memory, at oras bago magsara ang Linux VM kapag walang ginagawa.

## Pag-install ng 0.2.0

Sa Linux o Mac na may Apple silicon, gamitin ang mga utos na ito para i-install ang 0.2.0 CLI. Sinusuri ng installer ang SHA-256 checksum ng download.

```sh
curl -fsSL https://podbag.dev/install.sh | PODBAG_VERSION=v0.2.0 sh
podbag --version
```

May DEB at RPM para sa Linux AMD64 at ARM64, at ZIP para sa Apple silicon Mac. Sa macOS, i-install muna ang CLI. Eksperimental ang Windows CLI at nangangailangan ng WSL 2. Sinusuportahan ng Android ARM64 CLI ang mga utos para sa image. [Mga download ng 0.2.0](https://github.com/SteelCrab/podbag/releases/tag/v0.2.0)

Para mailapat ang mga pag-aayos sa oras ng pagbabago ng file at crontab sa apektadong image na naimbak ng 0.1.0, alisin ito at i-pull o i-load muli. [Buong talaan ng mga pagbabago](https://github.com/SteelCrab/podbag/blob/v0.2.0/CHANGELOG.md#v020-2026-11-20)
