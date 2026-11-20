---
title: "Práctica · Gestiona un volumen con la CLI y la GUI"
date: 2026-11-20
author: team
categories: [how-to]
tags: [cli, desktop, tutorials, volumes]
summary: "Crea un volumen en la CLI, inspecciónalo y elimínalo en Desktop siguiendo el progreso."
image: gui-volumes-es.png
image_alt: "Volúmenes de práctica · my-api"
draft: false
---

Crea un volumen en la CLI, inspecciónalo y elimínalo en Desktop siguiendo el progreso.

[Descargar el módulo](cli-gui-volumes.podbag)

## ¿Qué es un volumen?

Un volumen guarda archivos por separado del contenedor. Aquí, `app-a` guarda `note.txt` en el volumen `my-api`. Después de eliminar `app-a`, el nuevo contenedor `app-b` monta el mismo volumen y lee el archivo. Al eliminar el propio volumen también se borran sus archivos.

[![¿Qué es un volumen?](volume-life.webp)](volume-life.mp4)

## Instala el módulo

Usa versiones compatibles de Desktop y la CLI. Descarga el archivo e instálalo desde los tutoriales de Desktop o ejecuta este comando en la carpeta de descarga.

```sh
podbag lab install cli-gui-volumes.podbag
```

![Instala el módulo](gui-install.png)

## Abre la práctica en Desktop

Selecciona **Abrir la guía web** en **Training** para volver a esta página. Training muestra el estado del módulo y la tarea actual.

![Módulo de volúmenes y sus acciones en Training](gui-ready-es.png)

## Abrir la terminal

Abre **Volúmenes de práctica** en la barra lateral de Desktop y selecciona Terminal. Mantén abierta esta página y la terminal.

![Volúmenes de práctica con la terminal abierta](gui-shell-es.png)

## Crear el volumen en la CLI

Escribe este comando en el prompt volume-lab.

```sh
podbag volume create my-api
podbag volume ls
```

![podbag volume ls · my-api](gui-create.png)

## Ver detalles en la GUI

Cuando aparezca el volumen, Training indica que toca inspeccionarlo en la GUI.

![Volúmenes de práctica · my-api](gui-volumes-es.png)

En Volúmenes de práctica, selecciona my-api para ver su nombre y ruta.

![my-api · Mountpoint](gui-inspect-es.png)

## Eliminarlo en la GUI

Pulsa Eliminar en my-api. Comprueba el nombre y confirma.

![Eliminarlo en la GUI · my-api](gui-dialog-es.png)

Tras eliminarlo, la lista queda vacía. Vuelve a la misma terminal de prácticas.

![Verificarlo en la CLI · En curso](gui-empty-es.png)

## Verificarlo en la CLI

Vuelve a listar los volúmenes en la terminal de prácticas.

```sh
podbag volume ls
```

![Terminar la sesión · En curso](gui-verified-es.png)

## Terminar la sesión

Cuando aparezca `Verified`, escribe `exit` para limpiar el almacenamiento temporal. Training marca el módulo como completado.

```sh
exit
```

![Verified · exit](gui-finish.png)

![Progreso de la práctica · Completado](gui-complete-es.png)

## Desinstala el módulo

Ejecuta el comando en la terminal original para eliminar el módulo y su registro de finalización.

```sh
podbag lab remove volume-basics
```

![Desinstala el módulo · Module removed.](uninstall.png)
