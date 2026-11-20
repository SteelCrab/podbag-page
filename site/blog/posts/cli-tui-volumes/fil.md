---
title: "Lab · Pamahalaan ang volume gamit ang CLI at GUI"
date: 2026-11-20
author: team
categories: [how-to]
tags: [cli, desktop, tutorials, volumes]
summary: "Gumawa ng volume sa CLI, siyasatin at burahin ito sa Desktop, at tingnan ang progreso."
image: gui-volumes-fil.png
image_alt: "Mga practice volume · my-api"
draft: false
---

Gumawa ng volume sa CLI, siyasatin at burahin ito sa Desktop, at tingnan ang progreso.

[I-download ang module](cli-gui-volumes.podbag)

## Ano ang volume?

Ang volume ay imbakan ng mga file na hiwalay sa container. Dito, sine-save ng `app-a` ang `note.txt` sa volume na `my-api`. Pagkatapos alisin ang `app-a`, magagamit ng bagong container na `app-b` ang file kapag ini-mount nito ang parehong volume. Kapag binura ang volume mismo, mabubura rin ang mga file nito.

[![Ano ang volume?](volume-life.webp)](volume-life.mp4)

## I-install ang module

Gumamit ng magkatugmang bersiyon ng Desktop at CLI. I-download ang file at i-install mula sa Tutorials o patakbuhin ang command sa folder ng download.

```sh
podbag lab install cli-gui-volumes.podbag
```

![I-install ang module](gui-install.png)

## Buksan ang lab sa Desktop

Sa Tutorials, buksan ang module. Makikita ang kasalukuyang gawain sa progreso. Pindutin ang Terminal para buksan ang practice shell.

![Progreso ng lab · Naghihintay](gui-ready-fil.png)

## Buksan ang shell

Panatilihing bukas ang shell. Piliin ang Mga practice volume sa sidebar ng Desktop para makita ang command.

![Gumawa sa CLI · Ginagawa](gui-shell-fil.png)

## Gumawa sa CLI

I-type ito sa prompt na volume-lab.

```sh
podbag volume create my-api
podbag volume ls
```

![podbag volume ls · my-api](gui-create.png)

## Siyasatin sa GUI

Kapag lumabas ang my-api, tapos na ang paggawa at magsisimula ang pagsisiyasat sa GUI.

![Mga practice volume · my-api](gui-volumes-fil.png)

Sa Mga practice volume, piliin ang my-api at tingnan ang pangalan at lokasyon.

![my-api · Mountpoint](gui-inspect-fil.png)

## Burahin sa GUI

Piliin ang Remove sa my-api. Tiyakin ang pangalan at kumpirmahin.

![Burahin sa GUI · my-api](gui-dialog-fil.png)

Kapag wala nang volume sa listahan, bumalik sa parehong shell para tiyakin ang resulta.

![Tiyakin sa CLI · Ginagawa](gui-empty-fil.png)

## Tiyakin sa CLI

Ilista muli ang mga volume sa practice shell.

```sh
podbag volume ls
```

![Tapusin ang session · Ginagawa](gui-verified-fil.png)

## Tapusin ang session

Kapag lumabas ang Verified, i-type ang exit. Hihinto ang serbisyo, lilinisin ang pansamantalang storage, at mamarkahang tapos ang lahat ng gawain.

```sh
exit
```

![Verified · exit](gui-finish.png)

![Progreso ng lab · Tapos na](gui-complete-fil.png)

## Alisin ang module

Patakbuhin ito sa orihinal na terminal para alisin ang module at ang tala ng pagkumpleto.

```sh
podbag lab remove volume-basics
```

![Alisin ang module · Module removed.](uninstall.png)
