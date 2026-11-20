---
title: "Podbag 0.3.0"
date: 2026-11-21
author: team
categories: [announcements]
tags: [release, desktop, windows, training, tui]
summary: "Instala Podbag Desktop en Windows, inicia su máquina virtual Linux en Mac con chip de Apple y aprende a usar contenedores con cuatro prácticas guiadas."
image: card-es.png
image_alt: "Podbag 0.3.0"
draft: false
---

Podbag 0.3.0 ya está disponible. Esta versión incluye instaladores de Windows, un paquete de Desktop para macOS con el motor integrado y cuatro módulos de iniciación.

## Instala Podbag Desktop

- **Windows x86_64 y ARM64.** Descarga el MSI para tu CPU. Abre **Podbag Desktop** en el menú Inicio. Activa WSL 2 para ejecutar contenedores.
- **Mac con chip de Apple.** Descomprime el ZIP de Desktop y abre `podbag.app`. Desktop inicia la máquina virtual Linux con el motor incluido.
- **Linux x86_64 y ARM64.** Instala el DEB o RPM que corresponda a tu distribución y CPU. El paquete incluye el motor.

[Descarga Podbag 0.3.0](https://github.com/SteelCrab/podbag/releases/tag/v0.3.0)

## Aprende con las prácticas de Podbag

Abre **Training** en Desktop. Los cuatro módulos enseñan a ejecutar un contenedor, publicar una página web local, conservar archivos en un volumen y sustituir un servicio web. Sigue cada guía para instalar su módulo. Desktop muestra el progreso y ejecuta los ejercicios en sesiones aisladas. [Ejecuta tu primer contenedor (en inglés)](/blog/container-basics/)

![Podbag Desktop muestra los módulos de iniciación y el comando del paso actual](https://podbag.dev/blog/web-basics/start-en.png)

## Trabaja desde la terminal

Usa `podbag tui` para crear volúmenes, iniciar sesión en registros, importar imágenes o consultar recursos de Kubernetes. La CLI añade `podbag engine`, `podbag import`, `podbag kube`, `podbag settings` y `podbag tutorial`.

Instala la CLI en Linux o Mac con chip de Apple. El instalador verifica la suma SHA-256 del archivo descargado.

```sh
curl -fsSL https://podbag.dev/install.sh | PODBAG_VERSION=v0.3.0 sh
podbag --version
```

[Registro de cambios completo](https://github.com/SteelCrab/podbag/blob/v0.3.0/CHANGELOG.md#v030-2026-11-21)
