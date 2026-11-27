---
title: "Podbag Desktop · Pamahalaan ang mga container"
date: 2026-11-27
author: team
categories: [how-to]
tags: [desktop, gui, containers]
summary: "Simulan, ihinto, i-pause at alisin ang mga container. Basahin ang mga log at detalye nila, magbukas ng shell at linisin ang mga nakahinto."
image: gui-logs-fil.png
image_alt: "Ang tab na Mga log ng container na web sa Podbag Desktop"
outline: "Sa gabay na ito"
draft: false
---

Buksan ang **Mga container** sa sidebar. Ipinapakita ng listahan ang pangalan at ID ng bawat container, ang image nito, ang estado nito, ang mga port nito at kung kailan ito ginawa.

**Oras** 5 minuto.

## Simulan at ihinto ang container

Nagbabago ang mga button sa dulo ng row ayon sa estado ng container.

- **Tumatakbo:** **Ihinto**, **I-restart**, **I-pause**, **Mga log**, **Buksan ang shell** at **Alisin**.
- **Naka-pause:** **Ituloy**, **Ihinto**, **Mga log** at **Alisin**.
- **Nakahinto:** **Simulan**, **Mga log** at **Alisin**.

Lumalabas ang **I-pause**, **Ituloy** at **Palitan ang pangalan** kapag kaya ng engine ang mga ito. Kaya ito ng podbag. Nagbabago ang estado sa listahan kapag tapos na ang aksyon.

## Magbukas ng container

I-click ang row. May tatlong tab ang mga detalye.

- **Impormasyon:** ang ID, ang image, ang command, ang status, ang mga port at kung kailan ginawa ang container.
- **Mga log:** ang output ng container. Kapag naka-on ang **Sundan**, lumalabas ang mga bagong linya sa ibaba.
- **Buong data:** lahat ng alam ng engine tungkol sa container, bilang JSON.

![Ang tab na Impormasyon ng container na web sa Podbag Desktop](gui-detail-fil.png)

Gumagawa sa container na ito ang mga button sa kanang itaas. Nandoon din ang **Palitan ang pangalan**. Pindutin ang `Esc` o i-click ang arrow na pabalik para bumalik sa listahan.

![Ang tab na Mga log ng container na web sa Podbag Desktop](gui-logs-fil.png)

## Magbukas ng shell

Nagbubukas ang **Buksan ang shell** ng terminal na may shell sa loob ng tumatakbong container. Kapag walang mahanap na terminal app ang app, ipinapakita nito ang command. I-click ang **Kopyahin** at patakbuhin ang command sa terminal.

## Alisin ang container

I-click ang **Alisin**. Nagtatanong muna ang app. Ang tumatakbong container ay ihihinto muna, saka aalisin.

![Nagtatanong ang Podbag Desktop bago nito alisin ang tumatakbong container na web](gui-remove-fil.png)

## Maglinis

Inaalis ng **Linisin** sa itaas ng listahan ang lahat ng nakahintong container. Nagtatanong muna ang app. Pagkatapos, ipinapakita nito kung ilan ang inalis nito at kung gaano kalaking espasyo ang nabakante.

## Susunod

[Kumuha at pamahalaan ang mga image](../gui-images/).
