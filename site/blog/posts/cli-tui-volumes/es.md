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

## Instala el módulo

Usa versiones compatibles de Desktop y la CLI. Descarga el archivo e instálalo desde los tutoriales de Desktop o ejecuta este comando en la carpeta de descarga.

```sh
podbag lab install cli-gui-volumes.podbag
```

![Instala el módulo](gui-install.png)

## Abre la práctica en Desktop

Selecciona el módulo instalado en los tutoriales. El panel indica la tarea en curso. Abre la terminal con el botón de la práctica.

![Progreso de la práctica · Pendiente](gui-ready-es.png)

## Abrir la terminal

Deja la terminal abierta y elige Volúmenes de práctica en la barra lateral. El paso actual muestra el comando que debes escribir.

![Crear el volumen en la CLI · En curso](gui-shell-es.png)

## Crear el volumen en la CLI

Escribe este comando en el prompt volume-lab.

```sh
podbag volume create my-api
podbag volume ls
```

![podbag volume ls · my-api](gui-create.png)

## Ver detalles en la GUI

Al aparecer my-api, la creación queda completada y la inspección en la GUI pasa a estar en curso.

![Volúmenes de práctica · my-api](gui-volumes-es.png)

En Volúmenes de práctica, selecciona my-api para ver su nombre y ruta.

![my-api · Mountpoint](gui-inspect-es.png)

## Eliminarlo en la GUI

Pulsa Eliminar en my-api. Comprueba el nombre y confirma.

![Eliminarlo en la GUI · my-api](gui-dialog-es.png)

Tras eliminar el volumen, la lista queda vacía. Vuelve a la misma terminal para comprobarlo.

![Verificarlo en la CLI · En curso](gui-empty-es.png)

## Verificarlo en la CLI

Vuelve a listar los volúmenes en la terminal de prácticas.

```sh
podbag volume ls
```

![Terminar la sesión · En curso](gui-verified-es.png)

## Terminar la sesión

Cuando aparezca Verified, escribe exit. El servicio se detiene, el almacén temporal se borra y todos los pasos quedan completados.

```sh
exit
```

![Verified · exit](gui-finish.png)

![Progreso de la práctica · Completado](gui-complete-es.png)

## Desinstala el módulo

Ejecuta el comando en la terminal original para eliminar el módulo y su registro de finalización.

```sh
podbag lab remove
```

![Desinstala el módulo · Module removed.](uninstall.png)
