---
title: "Lab · Basahin ang JSON mula sa volume gamit ang HTTP"
date: 2026-11-20
author: team
categories: [how-to]
tags: [desktop, tutorials, volumes, http]
summary: "Gumawa ng volume, sumulat ng file at basahin ang sarili mong mensahe mula sa lokal na server."
image: 08-response-fil.png
image_alt: "Tugong HTTP 200 na may JSON mula sa volume."
draft: false
---

Gumamit ng Podbag Desktop na may **Mga tutorial** sa sidebar. Pansamantalang storage sa device ang gamit ng lab. Hindi kailangan ng container o image download.

[I-download ang module ng lab](volume-api.podbag)

I-save ang `volume-api.podbag` at tandaan ang folder nito.

## Buksan ang Mga tutorial

Piliin ang **Mga tutorial** sa kaliwang sidebar. Lalabas ang installer sa unang pagbisita.

![Installer na may button na Pumili ng file.](01-open-fil.png)

## Piliin ang module

I-click ang **Pumili ng file** at buksan ang `volume-api.podbag`. Tingnan ang pamagat at pangalan ng file.

![Pamagat ng lab at pangalan ng napiling file.](02-file-fil.png)

## I-install at simulan ang lab

I-click ang **I-install ang module**. Kapag naka-install na, i-click ang **Simulan ang lab** para magbukas ng bagong workspace.

![Naka-install na module at button para simulan ang lab.](03-installed-fil.png)

## Gumawa ng volume

Ilagay ang `my-api` bilang pangalan at i-click ang **Gumawa ng volume**. Makikita ang pangalang ito sa path ng file sa susunod na screen.

![Nasa field ng pangalan ang my-api.](04-volume-fil.png)

## Isulat ang tugon

Palitan ang halaga ng `message` ng sarili mong pagbati, gaya ng `Hello from my lab!`. Panatilihin ang mga panipi at brace. I-click ang **I-save ang file**.

![Sariling pagbati sa editor ng response.json.](05-write-fil.png)

## Simulan ang server

Basahin ang na-save na JSON at i-click ang **Simulan ang server**. Pipili ang app ng libreng port sa `127.0.0.1`.

![Na-save na JSON at button para simulan ang server.](06-saved-fil.png)

## Magpadala ng request

I-click ang **Ipadala ang GET /**. Maaari ring kopyahin ang URL sa browser ng device na ito. Maaaring mag-iba ang port sa bawat lab.

![Lokal na URL at button para sa GET request.](07-server-fil.png)

## Tingnan at baguhin ang tugon

Hanapin ang sarili mong mensahe sa ilalim ng `HTTP 200`. I-click ang **I-edit ang file**, palitan ang pagbati at i-save ito. Magpadala ulit sa parehong URL.

![Tugong HTTP 200 na may JSON mula sa volume.](08-response-fil.png)

## Tapusin ang lab

I-click ang **Tapusin ang lab** at kumpirmahin. Hihinto ang server at aalisin ang pansamantalang volume at mga file. Mananatili ang module at ang tala ng pagkumpleto.

![Dialog na nagkukumpirma ng pagtanggal ng mga pansamantalang resource.](09-end-fil.png)
