---
title: "Podbag Training · Run your first container"
date: 2026-11-21
author: team
categories: [how-to]
tags: [cli, containers, desktop, training]
summary: "Start a small web server in the CLI, stop it in Podbag Desktop, and check its status in the same terminal."
image: running-en.png
image_alt: "A running hello-web container in Podbag Desktop"
draft: false
---

An image contains the files a program needs. A container runs the program from that image. In this lab, you run a small web server called `hello-web` and stop it with Podbag Desktop.

## Install the training module

[Download container-basics.podbag](https://github.com/SteelCrab/podbag/releases/download/training/container-basics/v1.0.0/container-basics.podbag). Open a training-compatible build of Podbag Desktop. In **Training**, choose the file and select **Install module**. You can also install it from your download folder.

```sh
podbag lab install container-basics.podbag
```

If you already installed this training module, install the new file over it to keep your completion record. Run `podbag lab list` to see your installed modules.

![The container module in Training with the practice terminal open](training-en.png)

## Run the web server in the CLI

On the Training card, select **Terminal**. Wait for the `container-lab $` prompt, then run the command. Podbag downloads the practice image on the first run.

```sh
podbag run -d --name hello-web --network none docker.io/library/busybox:1.37.0 httpd -f -p 8080
```

`-d` runs the container in the background. `--name hello-web` gives it a name. The server listens on port 8080 inside the container. This lab focuses on the container's lifecycle, so the command leaves the server isolated from the host network.

![The practice terminal prints the new container ID](cli-run.png)

## Stop the container in Desktop

Leave the practice terminal open. Select **Practice containers** in Desktop. Find `hello-web` with a running status and select **Stop** in its row. You can also open the container details and select **Stop** there.

![Practice containers shows hello-web running and the Stop action](running-en.png)

Desktop shows the container's exited status. The current task changes to **Check the status in the CLI**.

![Desktop shows hello-web exited and the CLI check in progress](stopped-en.png)

## Check the result in the CLI

Return to the same practice terminal and list all containers. The `-a` option includes stopped containers.

```sh
podbag ps -a
```

Confirm that `hello-web` shows `Exited`. The practice terminal prints `Verified`.

![The CLI shows hello-web Exited and confirms verification](cli-check.png)

## Finish the practice session

Type `exit`. Podbag removes the practice container, its downloaded image, and the temporary store. The module and its completion record remain available in Training.

![Podbag Desktop shows the finished training after cleanup](complete-en.png)
