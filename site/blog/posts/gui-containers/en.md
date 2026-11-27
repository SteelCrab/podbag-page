---
title: "Podbag Desktop · Manage containers"
date: 2026-11-27
author: team
categories: [how-to]
tags: [desktop, gui, containers]
summary: "Run a container, stop, pause and remove containers, read their logs and details, open a shell, and clean up the stopped ones."
image: gui-logs-en.png
image_alt: "The Logs tab of the web container in Podbag Desktop"
outline: "In this guide"
draft: false
---

Open **Containers** in the sidebar. The list shows each container's name and ID, its image, its state, its ports and when it was created.

**Time** 5 minutes.

## Run a container

Click **Run container** at the top of the list. A form opens.

1. Type the **Image**, for example `nginx:alpine`. The field suggests the images you already have.
2. Type a **Name**. You can leave it empty.
3. Under **Ports**, type a host port and a container port, for example `8081` and `80`. Choose TCP or UDP. Leave the host port empty to let the engine choose one. **Add port** adds a row.
4. Click **Run**.

![The Run a container form of Podbag Desktop](gui-run-en.png)

**More options** shows more fields.

- **Environment variables:** one `KEY=VALUE` on each row.
- **Volumes:** a volume name or a full host path, then the path in the container. Check **Read-only** if the container must not write there.
- **Command:** leave it empty to use the image's command.
- **Restart policy:** **Do not restart**, **When it fails**, **Always** or **Unless stopped**.
- **Remove when it stops:** removes the container when it stops. This turns the restart policy off.

The form checks your input before it sends anything. When the engine does not have the image, the app pulls it first. It uses your registry login, as **Pull image** does. Then the new container opens with its logs.

## Start and stop a container

The buttons at the end of a row change with the container's state.

- **Running:** **Stop**, **Restart**, **Pause**, **Logs**, **Open shell** and **Remove**.
- **Paused:** **Resume**, **Stop**, **Logs** and **Remove**.
- **Stopped:** **Start**, **Logs** and **Remove**.

**Pause**, **Resume** and **Rename** show when the engine can do them. podbag can. The state in the list changes when the action is done.

## Open a container

Click a row. The details have three tabs.

- **Info:** the ID, the image, the command, the status, the ports and when the container was created.
- **Logs:** the container's output. With **Follow**, new lines show at the bottom.
- **Inspect:** all that the engine knows about the container, as JSON.

![The Info tab of the web container in Podbag Desktop](gui-detail-en.png)

The buttons at the top right act on this container. **Rename** is also there. Press `Esc` or click the back arrow to go back to the list.

![The Logs tab of the web container in Podbag Desktop](gui-logs-en.png)

## Open a shell

**Open shell** opens a terminal with a shell in a running container. When the app finds no terminal app, it shows the command. Click **Copy** and run the command in a terminal.

## Remove a container

Click **Remove**. The app asks first. A running container is stopped, then removed.

![Podbag Desktop asks before it removes the running container web](gui-remove-en.png)

## Clean up

**Clean up** at the top of the list removes all stopped containers. The app asks first. Then it shows how many it removed and how much space it freed.

## Next

[Pull and manage images](../gui-images/).
