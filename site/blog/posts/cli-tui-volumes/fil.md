---
title: "Podbag Training · Pamahalaan ang volume gamit ang CLI at GUI"
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

![Gumagawa at naglilista ang terminal ng volume na my-api sa practice session; tinitingnan at binubura ito ng Podbag Desktop o ng TUI](architecture-fil-light.svg)

## Ano ang volume?

Ang volume ay imbakan ng mga file na hiwalay sa container. Dito, sine-save ng `app-a` ang `note.txt` sa volume na `my-api`. Pagkatapos alisin ang `app-a`, magagamit ng bagong container na `app-b` ang file kapag ini-mount nito ang parehong volume. Kapag binura ang volume mismo, mabubura rin ang mga file nito.

[![Ano ang volume?](volume-life.webp)](volume-life.mp4)

## I-install ang module

Gumamit ng magkatugmang bersiyon ng Desktop at CLI. Sa itaas ng **Training**, piliin ang **I-install ang module**, piliin ang na-download na file, at kumpirmahin. Maaari mo ring patakbuhin ang command sa folder ng download.

```sh
podbag lab install cli-gui-volumes.podbag
```

## Tingnan ang progreso sa Desktop

Palawakin ang **Training** sa sidebar at piliin ang volume module. Makikita mo ang mga tapos na gawain, kasalukuyang gawain, at mga susunod pa. Piliin ang **Buksan ang gabay sa web** para bumalik sa pahinang ito.

## Simulan ang practice session

Kopyahin ang command ng kasalukuyang hakbang at patakbuhin ito sa terminal mo. Panatilihing bukas ang pahinang ito at magpatuloy kapag lumabas ang `volume-lab $`.

```sh
podbag lab start volume-basics
```

![Command sa pagsisimula at mga hakbang ng volume module](gui-ready-fil.png)

## Gumawa sa CLI

I-type ito sa prompt na volume-lab.

```sh
podbag volume create my-api
podbag volume ls
```

![podbag volume ls · my-api](gui-create.png)

## Siyasatin sa GUI

Kapag lumitaw ang volume, makikita sa Training na susunod ang pagtingin sa detalye sa GUI.

![Mga practice volume · my-api](gui-volumes-fil.png)

Sa Mga practice volume, piliin ang my-api at tingnan ang pangalan at lokasyon.

![my-api · Mountpoint](gui-inspect-fil.png)

## Burahin sa GUI

Piliin ang Remove sa my-api. Tiyakin ang pangalan at kumpirmahin.

![Burahin sa GUI · my-api](gui-dialog-fil.png)

Pagkatapos alisin ang volume, magiging walang laman ang listahan. Bumalik sa parehong practice terminal.

![Walang laman ang listahan ng mga practice volume matapos ang pag-alis](gui-empty-fil.png)

## Tiyakin sa CLI

Ilista muli ang mga volume sa practice shell.

```sh
podbag volume ls
```

![Tapusin ang session · Ginagawa](gui-verified-fil.png)

## Tapusin ang session

Kapag lumabas ang `Verified`, i-type ang `exit` para linisin ang pansamantalang storage. Ipapakita ng Training na tapos na ang module.

```sh
exit
```

![Verified · exit](gui-finish.png)

![Ipinapakita ng Training na tapos na ang volume module](gui-complete-fil.png)

## Alisin ang module

Patakbuhin ito sa orihinal na terminal para alisin ang module at ang tala ng pagkumpleto.

```sh
podbag lab remove volume-basics
```

![Alisin ang module · Module removed.](uninstall.png)
