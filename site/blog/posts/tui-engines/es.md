---
title: "Podbag TUI · Cambia de motor y migra"
date: 2026-11-27
author: team
categories: [how-to]
tags: [tui, engines, docker, migration]
summary: "Usa la TUI con podbag, Docker, Podman u otro motor con la API de Docker, haz que el comando docker use podbag y copia contenedores, imágenes y volúmenes entre motores."
image: tui-docker-es.png
image_alt: "podbag tui después de pulsar E: la línea superior muestra Docker como motor"
outline: "En esta guía"
draft: false
---

La TUI funciona con cualquier motor que tenga la API de Docker: podbag, Docker, Podman, Kiri, un contexto de Docker o un socket Unix. La línea superior muestra el motor que la TUI usa ahora.

**Tiempo** 5 minutos.

## Qué motor usa la TUI

La TUI toma el primero de esta lista:

1. La opción `--engine`, solo para esta ejecución: `podbag tui --engine podman`.
2. El motor que elegiste antes en la TUI. La TUI lo recuerda.
3. `DOCKER_HOST`, cuando es un socket Unix (`unix://…`).
4. podbag.

La TUI nunca inicia Docker. Si un motor no responde, la línea de mensajes lo indica.

## Cambia entre podbag y Docker

Pulsa `E`. La TUI cambia de podbag a Docker, o de Docker a podbag. Desde cualquier otro motor, `E` cambia a podbag. Las listas se vuelven a cargar y la TUI recuerda la elección. También puedes hacer clic en el nombre del motor en la línea superior.

![podbag tui después de pulsar E: la línea superior muestra Docker como motor](tui-docker-es.png)

## Elige cualquier motor

1. Pulsa `F9` para abrir **Ajustes**.
2. Elige **Motor** y luego **Conectar**.
3. Elige el motor. **Socket Unix personalizado…** pide la ruta de un socket.

![La lista de motores de podbag tui: podbag, docker, podman, kiri, un contexto de Docker y un socket Unix personalizado](tui-engine-es.png)

**Ajustes → Motor → Detalles** muestra la versión del motor.

## Haz que el comando docker use podbag

Si el comando `docker` está instalado, la línea superior muestra adónde va, por ejemplo `docker → Docker Desktop`. Pulsa `D` para que use podbag. La TUI pregunta antes. Pulsa `D` otra vez para volver al motor anterior.

## Copia a otro motor

La migración copia contenedores, imágenes y volúmenes de un motor a otro. El origen no cambia.

1. Pulsa `F7` y elige **Motor**.
2. En **Origen**, elige el motor de origen o **Todos los motores locales**.
3. Elige el tipo de recurso: contenedores, imágenes o volúmenes.
4. Elige el recurso y luego el motor en **Destino**.
5. Elige **Iniciar migración**. La TUI muestra el progreso y comprueba la copia.

![La lista Origen de la migración en podbag tui](tui-migrate-es.png)

- Detén un contenedor antes de copiarlo.
- Si en el destino hay un contenedor o un volumen con el mismo nombre, la copia se detiene.

La [guía de uso](https://github.com/SteelCrab/podbag/blob/main/docs/usage.md) explica qué se copia y cómo copiar entre clústeres de Kubernetes.

## Siguiente

[Kubernetes y ajustes](../tui-kubernetes-settings/).
