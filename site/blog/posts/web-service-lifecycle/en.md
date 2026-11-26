---
title: "Podbag Training · Replace and clean up a web service"
date: 2026-11-21
author: team
categories: [how-to]
tags: [cli, containers, desktop, training]
summary: "Replace a running web service while keeping its content."
image: gui-ports-en.png
image_alt: "Replace and clean up a web service"
outline: "Training flow"
draft: false
---

Replace a running web service while keeping its content. Use the same volume and local address before and after the replacement.

**Time** 15 minutes

![site-v1 writes the page into the volume site-data and is replaced by site-v2, which serves the same page on 127.0.0.1:18081](architecture-en-light.svg)

## Beginner course

[Run your first container](../container-basics/) → [Open a web server in the browser](../web-basics/) → [Keep files across containers](../volume-persistence/) → **Replace and clean up a web service**

## Install the module

[Download web-service-lifecycle.podbag](web-service-lifecycle.podbag). In Desktop, select **Install module** at the top of **Training**. Choose the downloaded file and confirm.

```sh
podbag lab install web-service-lifecycle.podbag
```

![Install confirmation with the module and file name](install-en.png)

## Start the practice session

Expand **Training** in the sidebar and select the module. Copy the start command into your terminal. Continue when it shows the `training $` prompt.

```sh
podbag lab start web-service-lifecycle
```

![Start the practice session](start-en.png)

If the default port is already in use, use the port in Training. The command and browser address show the same port.

## Create the site volume

Create `site-data` to hold the web page.

```sh
podbag volume create site-data
```

![Create the site volume](create-en.png)

## Start the first server

Start `site-v1`. It writes `index.html` to the volume and serves it on the published port. The default is `18081` on your computer.

```sh
podbag run -d --name site-v1 -p 127.0.0.1:18081:8080 -v site-data:/site docker.io/library/busybox:1.37.0 sh -c 'printf "%s\n" "My Podbag site" > /site/index.html && exec httpd -f -p 8080 -h /site'
```

![Start the first server](runFirst-en.png)

## Check the first server ports

Select **Practice containers → site-v1 → View ports**. Check the address in the detail panel.

![Check the first server ports](ports-en.png)

![Check the first server ports](gui-ports-en.png)

## Open the first server page

Select **Open in browser**. Confirm that the page displays **My Podbag site**.

![Open the first server page](browser-en.png)

![Open the first server page](web-browser-en.png)

## Stop the first server

Select **Practice containers → site-v1 → Stop**.

![Stop the first server](stop-en.png)

![Stop the first server](gui-stop-en.png)

## Remove the first server

Run the removal command. The container disappears and `site-data` stays in the practice session.

```sh
podbag rm site-v1
```

![Remove the first server](remove-en.png)

## Start the replacement server

Start `site-v2` on the same port. Mount `site-data` read-only. The server uses the page already stored in the volume.

```sh
podbag run -d --name site-v2 -p 127.0.0.1:18081:8080 -v site-data:/site:ro docker.io/library/busybox:1.37.0 httpd -f -p 8080 -h /site
```

![Start the replacement server](runReplacement-en.png)

## Check the replacement server ports

Select **Practice containers → site-v2 → View ports**. Confirm the address matches the first server.

![Check the replacement server ports](portsReplacement-en.png)

![Check the replacement server ports](gui-ports-replacement-en.png)

## Open the replacement server page

Select **Open in browser** again. The page still displays **My Podbag site**. Desktop checks the response with a new request.

![Open the replacement server page](browserReplacement-en.png)

![Open the replacement server page](web-browserReplacement-en.png)

## Stop the replacement server

Select **Practice containers → site-v2 → Stop**.

![Stop the replacement server](stopReplacement-en.png)

![Stop the replacement server](gui-stop-replacement-en.png)

## Remove the replacement server

Remove the stopped container in the same terminal.

```sh
podbag rm site-v2
```

![Remove the replacement server](removeReplacement-en.png)

## Open the site volume details

Select **Practice volumes → site-data** to see the remaining volume.

![Open the site volume details](inspect-en.png)

![Open the site volume details](gui-inspect-en.png)

## Delete the site volume

Select **Remove** and confirm the volume name.

![Delete the site volume](delete-en.png)

![Delete the site volume](gui-delete-en.png)

## Check the container list

List all containers in the practice session. The list is empty.

```sh
podbag ps -a
```

![Check the container list](checkContainers-en.png)

## Check the volume list

List the practice volumes. The list is empty.

```sh
podbag volume ls
```

![Check the volume list](checkVolumes-en.png)

## Finish the practice session

Run the command shown in the final step. Training records completion after the practice environment has been removed.

```sh
exit
```

![Finish the practice session](finish-en.png)

![Training shows all steps complete](complete-en.png)

[Next Training module · Recover a web server with logs](../web-service-recovery/)
