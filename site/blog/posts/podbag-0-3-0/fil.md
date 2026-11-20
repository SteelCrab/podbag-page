---
title: "Podbag 0.3.0"
date: 2026-11-21
author: team
categories: [announcements]
tags: [release, desktop, windows, training, tui]
summary: "I-install ang Podbag Desktop sa Windows, patakbuhin ang Linux VM nito sa Mac na may Apple chip, at matutong gumamit ng container sa apat na pagsasanay."
image: card-fil.png
image_alt: "Podbag 0.3.0"
draft: false
---

Available na ang Podbag 0.3.0. May installer na ito para sa Windows, Desktop bundle para sa macOS na may kasamang engine, at apat na module para sa mga baguhan.

## I-install ang Podbag Desktop

- **Windows x86_64 at ARM64.** I-download ang MSI para sa iyong CPU. Buksan ang **Podbag Desktop** mula sa Start menu. I-enable ang WSL 2 para makapagpatakbo ng container.
- **Mac na may Apple chip.** I-extract ang ZIP ng Desktop at buksan ang `podbag.app`. Sinisimulan ng Desktop ang Linux VM gamit ang kasamang engine.
- **Linux x86_64 at ARM64.** I-install ang DEB o RPM para sa iyong distribusyon at CPU. Kasama ang engine sa package.

[I-download ang Podbag 0.3.0](https://github.com/SteelCrab/podbag/releases/tag/v0.3.0)

## Matuto sa Podbag Training

Buksan ang **Training** sa Desktop. Saklaw ng apat na module ang pagpapatakbo ng container, pag-publish ng lokal na web page, pagtatago ng file sa volume at pagpapalit ng web service. Sundin ang bawat gabay para i-install ang module. Ipinapakita ng Desktop ang progreso at nagpapatakbo ng mga ehersisyo sa magkakahiwalay na sesyon. [Patakbuhin ang unang container (English)](/blog/container-basics/)

![Ipinapakita ng Podbag Desktop ang mga module para sa baguhan at ang kasalukuyang command](https://podbag.dev/blog/web-basics/start-en.png)

## Gamitin ang terminal

Gamitin ang `podbag tui` para gumawa ng volume, mag-log in sa registry, mag-import ng image o tingnan ang mga resource ng Kubernetes. Idinagdag sa CLI ang `podbag engine`, `podbag import`, `podbag kube`, `podbag settings` at `podbag tutorial`.

I-install ang CLI sa Linux o sa Mac na may Apple chip. Bineberipika ng installer ang SHA-256 checksum ng na-download na file.

```sh
curl -fsSL https://podbag.dev/install.sh | PODBAG_VERSION=v0.3.0 sh
podbag --version
```

[Buong tala ng mga pagbabago](https://github.com/SteelCrab/podbag/blob/v0.3.0/CHANGELOG.md#v030-2026-11-21)
