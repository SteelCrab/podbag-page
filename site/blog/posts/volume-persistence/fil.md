---
title: "Podbag Training · Panatilihin ang mga file sa pagitan ng mga container"
date: 2026-11-21
author: team
categories: [how-to]
tags: [cli, containers, desktop, training]
summary: "Nag-iimbak ang volume ng mga file na nananatili kahit maalis ang container."
image: read-en.png
image_alt: "Panatilihin ang mga file sa pagitan ng mga container"
outline: "Daloy ng pagsasanay"
draft: false
---

Nag-iimbak ang volume ng mga file na nananatili kahit maalis ang container. Panoorin ang animation. Pagkatapos, subukan ang parehong pagkakasunod gamit ang `app-a` at `app-b`.

**Oras** 15 minuto

![Isinusulat ng app-a ang note.txt sa volume na training-data at binabasa ito ng app-b; nananatili ang volume pagkatapos maalis ang dalawang container](architecture-fil-light.svg)

## Kurso para sa baguhan

[Patakbuhin ang iyong unang container](../container-basics/) → [Buksan ang web server sa browser](../web-basics/) → **Panatilihin ang mga file sa pagitan ng mga container** → [Palitan at linisin ang web service](../web-service-lifecycle/)

[![Nananatili ang volume kahit palitan ang container](volume-life.webp)](volume-life.mp4)

## I-install ang module

[I-download ang volume-persistence.podbag](volume-persistence.podbag). Sa Desktop, piliin ang **I-install ang module** sa itaas ng **Training**. Piliin ang na-download na file at kumpirmahin.

```sh
podbag lab install volume-persistence.podbag
```

![Kumpirmasyon ng pag-install na may pangalan ng module at file](install-en.png)

## Simulan ang practice session

Palawakin ang **Training** sa sidebar at piliin ang module. Kopyahin ang command sa pagsisimula sa terminal mo. Magpatuloy kapag lumabas ang prompt na `training $`.

```sh
podbag lab start volume-persistence
```

![Simulan ang practice session](start-en.png)

Para gawin ang mga hakbang sa TUI sa halip na sa Podbag Desktop, idagdag ang `--tui`.

```sh
podbag lab start volume-persistence --tui
```

Sa TUI, pindutin ang `:` para buksan ang training shell sa isang hakbang na command. I-type ang `exit` para bumalik sa TUI. Pindutin ang `q` para tapusin ang practice session.

## Gumawa ng volume

Gumawa ng named volume na `training-data` sa practice session.

```sh
podbag volume create training-data
```

- **Sa Podbag Desktop:** Piliin ang **Mga practice volume → Gumawa ng volume na training-data**.
- **Sa TUI:** Buksan ang **Mga volume**, pindutin ang `v`, i-type ang `training-data` at pindutin ang `Enter`.

![Gumawa ng volume](create-en.png)

## Magsulat ng file mula sa app-a

Ikinokonekta ng `-v training-data:/data` ang volume sa container. Isinusulat ng command ang `note.txt` at saka lalabas ang `app-a`.

```sh
podbag run --name app-a --network none -v training-data:/data docker.io/library/busybox:1.37.0 sh -c 'printf "%s\n" "hello from app-a" > /data/note.txt'
```

![Magsulat ng file mula sa app-a](write-en.png)

## Alisin ang app-a

Alisin ang nakahintong container. Mananatili ang volume sa practice session.

```sh
podbag rm app-a
```

- **Sa Podbag Desktop:** Piliin ang **Mga practice container → app-a → Alisin** at kumpirmahin.
- **Sa TUI:** Piliin ang `app-a` sa **Mga container**, pindutin ang `d`, saka ang `y`.

![Alisin ang app-a](removeWriter-en.png)

## Basahin ang file mula sa app-b

Ini-mount ng `app-b` ang parehong volume. Ginagawang read-only ng suffix na `:ro` ang volume. Ipinapakita ng terminal ang `hello from app-a`.

```sh
podbag run --name app-b --network none -v training-data:/data:ro docker.io/library/busybox:1.37.0 cat /data/note.txt
```

![Basahin ang file mula sa app-b](read-en.png)

![Basahin ang file mula sa app-b](terminal-read-en.png)

## Alisin ang app-b

Alisin ang pangalawang container para mapalaya ang volume bago mo ito burahin.

```sh
podbag rm app-b
```

- **Sa Podbag Desktop:** Piliin ang **Mga practice container → app-b → Alisin** at kumpirmahin.
- **Sa TUI:** Piliin ang `app-b` sa **Mga container**, pindutin ang `d`, saka ang `y`.

![Alisin ang app-b](removeReader-en.png)

## Buksan ang detalye ng volume

Piliin ang **Mga practice volume → training-data**. Ipinapakita ng detalye ang pangalan at mount point nito.

- **Sa Podbag Desktop:** Piliin ang **Mga practice volume → training-data**.
- **Sa TUI:** Piliin ang `training-data` sa **Mga volume** at pindutin ang `Enter`.

![Buksan ang detalye ng volume](inspect-en.png)

![Buksan ang detalye ng volume](gui-inspect-en.png)

## Burahin ang volume sa Desktop

Piliin ang **Alisin** at tiyaking `training-data` ang pangalan sa dialog. Mabubura ang volume at ang file nito.

- **Sa Podbag Desktop:** Piliin ang **Mga practice volume → training-data → Alisin** at kumpirmahin.
- **Sa TUI:** Piliin ang `training-data` sa **Mga volume**, pindutin ang `d`, saka ang `y`.

![Burahin ang volume sa Desktop](delete-en.png)

![Burahin ang volume sa Desktop](gui-delete-en.png)

## Tingnan ang listahan ng volume

Bumalik sa parehong terminal. Wala na ang `training-data` sa listahan ng volume.

```sh
podbag volume ls
```

![Tingnan ang listahan ng volume](checkVolumes-en.png)

## Tapusin ang practice session

Patakbuhin ang command sa huling hakbang. Itatala ng Training ang pagkumpleto pagkatapos maalis ang practice environment.

```sh
exit
```

![Tapusin ang practice session](finish-en.png)

![Ipinapakita ng Training na tapos ang lahat ng hakbang](complete-en.png)

[Susunod na module · Palitan at linisin ang web service](../web-service-lifecycle/)
