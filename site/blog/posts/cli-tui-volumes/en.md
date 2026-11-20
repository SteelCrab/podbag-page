---
title: "Lab · Manage a volume with the CLI and GUI"
date: 2026-11-20
author: team
categories: [how-to]
tags: [cli, desktop, tutorials, volumes]
summary: "Create a volume in the CLI, inspect and remove it in Podbag Desktop, and watch your progress update."
image: gui-volumes-en.png
image_alt: "Practice volumes · my-api"
draft: false
---

Create a volume in the CLI, inspect and remove it in Podbag Desktop, and watch your progress update.

[Download the lab module](cli-gui-volumes.podbag)

## What is a volume?

A volume stores files separately from a container. Here, `app-a` saves `note.txt` in the `my-api` volume. After `app-a` is removed, a new container, `app-b`, mounts the same volume and reads the file. Deleting the volume itself removes its files.

[![What is a volume?](volume-life.webp)](volume-life.mp4)

## Install the module

Use a matching build of Podbag Desktop and the CLI. Download the module and install it under **Training → Choose file → Install module**, or run the command below from the download folder.

```sh
podbag lab install cli-gui-volumes.podbag
```

![Install the module](gui-install.png)

## Open the lab in Desktop

Select **Open web guide** in **Training** to return to this page. Training shows the installed module and the current task while you work.

![Installed volume module and its actions in Training](gui-ready-en.png)

## Open the practice shell

Open **Practice volumes** in the Desktop sidebar and select **Terminal**. Keep this page and the terminal open as you work.

![Practice volumes with the terminal open](gui-shell-en.png)

## Create a volume in the CLI

Type this command at the volume-lab prompt.

```sh
podbag volume create my-api
podbag volume ls
```

![podbag volume ls · my-api](gui-create.png)

## Inspect it in the GUI

After a volume appears, Training shows the GUI inspection task in progress.

![Practice volumes · my-api](gui-volumes-en.png)

In Practice volumes, select my-api to inspect its name and storage path.

![my-api · Mountpoint](gui-inspect-en.png)

## Delete it in the GUI

Select Remove for my-api. Check the name in the dialog and confirm.

![Delete it in the GUI · my-api](gui-dialog-en.png)

After deletion the list is empty. Return to the same practice shell.

![Empty Practice volumes list after deletion](gui-empty-en.png)

## Verify removal in the CLI

List the volumes again in the practice shell.

```sh
podbag volume ls
```

![End the session · In progress](gui-verified-en.png)

## End the session

When the shell reports `Verified`, type `exit` to clean up the temporary store. Training marks the module complete.

```sh
exit
```

![Verified · exit](gui-finish.png)

![Training marks the volume module complete](gui-complete-en.png)

## Uninstall the module

Run this command outside the practice shell to remove the module and its completion record. You can reinstall the downloaded file.

```sh
podbag lab remove volume-basics
```

![Uninstall the module · Module removed.](uninstall.png)
