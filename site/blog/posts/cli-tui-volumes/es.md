---
title: "Podbag Training · Gestiona un volumen con la CLI y la GUI"
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

![La terminal crea y lista el volumen my-api en la sesión de práctica; Podbag Desktop o la TUI lo revisa y lo elimina](architecture-es-light.svg)

## ¿Qué es un volumen?

Un volumen guarda archivos por separado del contenedor. Aquí, `app-a` guarda `note.txt` en el volumen `my-api`. Después de eliminar `app-a`, el nuevo contenedor `app-b` monta el mismo volumen y lee el archivo. Al eliminar el propio volumen también se borran sus archivos.

[![¿Qué es un volumen?](volume-life.webp)](volume-life.mp4)

## Instala el módulo

Usa versiones compatibles de Desktop y la CLI. En **Training**, elige **Instalar módulo** en la parte superior, selecciona el archivo descargado y confirma. También puedes ejecutar este comando en la carpeta de descarga.

```sh
podbag lab install cli-gui-volumes.podbag
```

## Consulta el progreso en Desktop

Despliega **Training** en la barra lateral y selecciona el módulo de volúmenes. Puedes ver las tareas completadas, en curso y pendientes. Selecciona **Abrir la guía web** para volver a esta página.

## Inicia la sesión de práctica

Copia el comando del paso actual y ejecútalo en tu terminal. Mantén abierta esta página y continúa cuando aparezca `volume-lab $`.

```sh
podbag lab start volume-basics
```

![Comando de inicio y pasos del módulo de volúmenes](gui-ready-es.png)

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

![Lista vacía de volúmenes de práctica tras la eliminación](gui-empty-es.png)

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

![Training muestra el módulo de volúmenes completado](gui-complete-es.png)

## Desinstala el módulo

Ejecuta el comando en la terminal original para eliminar el módulo y su registro de finalización.

```sh
podbag lab remove volume-basics
```

![Desinstala el módulo · Module removed.](uninstall.png)
