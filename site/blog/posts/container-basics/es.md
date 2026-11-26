---
title: "Podbag Training · Ejecuta tu primer contenedor"
date: 2026-11-21
author: team
categories: [how-to]
tags: [cli, containers, desktop, training]
summary: "Inicia un pequeño servidor web en la CLI, detenlo en Podbag Desktop y comprueba su estado en la misma terminal."
image: running-en.png
image_alt: "Un contenedor hello-web en ejecución en Podbag Desktop"
outline: "Flujo de la práctica"
draft: false
---

Una imagen contiene los archivos que necesita un programa. Un contenedor ejecuta el programa de esa imagen. En esta práctica, ejecutas un pequeño servidor web llamado `hello-web` y lo detienes con Podbag Desktop.

![La terminal ejecuta el contenedor hello-web desde la imagen busybox en la sesión de práctica; Podbag Desktop lo detiene](architecture-es-light.svg)

## Curso de iniciación

**Ejecuta tu primer contenedor** → [Abre un servidor web en el navegador](../web-basics/) → [Conserva archivos entre contenedores](../volume-persistence/) → [Sustituye y limpia un servicio web](../web-service-lifecycle/)

## Instala el módulo de práctica

[Descargar container-basics.podbag](https://github.com/SteelCrab/podbag/releases/download/training/container-basics/v1.0.0/container-basics.podbag). Abre una versión de Podbag Desktop compatible con Training. En **Training**, selecciona **Instalar módulo** en la parte superior, elige el archivo descargado y confirma. También puedes instalarlo desde tu carpeta de descargas.

```sh
podbag lab install container-basics.podbag
```

![Podbag muestra el módulo y el archivo seleccionados antes de instalarlo](install-en.png)

Si ya instalaste este módulo, instala el archivo nuevo encima para conservar tu registro de finalización. Ejecuta `podbag lab list` para ver los módulos instalados.

## Inicia la sesión de práctica

En la barra lateral, despliega **Training** y selecciona **Ejecuta un contenedor**. El módulo muestra el paso actual y los pasos siguientes. Copia el comando de abajo y ejecútalo en tu terminal. Continúa cuando aparezca `container-lab $`.

```sh
podbag lab start container-basics
```

![El módulo de contenedores muestra el comando de inicio y los pasos de la práctica](training-en.png)

## Ejecuta el servidor web en la CLI

Escribe este comando en la terminal de práctica. Podbag descarga la imagen de práctica la primera vez.

```sh
podbag run -d --name hello-web --network none docker.io/library/busybox:1.37.0 httpd -f -p 8080
```

`-d` ejecuta el contenedor en segundo plano. `--name hello-web` le da un nombre. El servidor escucha en el puerto 8080 dentro del contenedor. Esta práctica trata del ciclo de vida del contenedor. Por eso el comando deja el servidor aislado de la red del host.

![La terminal de práctica muestra el ID del nuevo contenedor](cli-run.png)

## Detén el contenedor en Desktop

Deja abierta la terminal de práctica. Selecciona **Contenedores de práctica** en Desktop. Busca `hello-web` en estado de ejecución y selecciona **Detener** en su fila. También puedes abrir los detalles del contenedor y seleccionar **Detener** allí.

![Contenedores de práctica muestra hello-web en ejecución y la acción Detener](running-en.png)

La fila del contenedor muestra **Detenido**. Selecciona el módulo en **Training** para ver **Comprueba el estado en la CLI** y copia su comando.

![La fila del contenedor de práctica muestra hello-web detenido](stopped-en.png)

## Comprueba el resultado en la CLI

Vuelve a la misma terminal de práctica y lista todos los contenedores. La opción `-a` incluye los contenedores detenidos.

```sh
podbag ps -a
```

![Training resalta la comprobación del estado en la CLI y muestra su comando](progress-en.png)

Comprueba que `hello-web` muestra `Exited`. La terminal de práctica muestra `Verified`.

![La CLI muestra hello-web como Exited y confirma la verificación](cli-check.png)

## Termina la sesión de práctica

Escribe `exit`. Podbag elimina el contenedor de práctica, la imagen descargada y el almacenamiento temporal. El módulo y su registro de finalización siguen disponibles en Training.

![Todos los pasos de la práctica muestran Completado tras la limpieza](complete-en.png)

[Siguiente módulo · Abre un servidor web en el navegador](../web-basics/)
