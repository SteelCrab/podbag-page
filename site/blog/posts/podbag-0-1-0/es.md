---
title: "podbag 0.1.0: contenedores sin demonio, guardados archivo por archivo"
date: 2026-11-20
author: team
categories: [announcements]
tags: [release, docker, compose, rootless, macos, windows]
summary: "Ya está aquí la primera versión de podbag. Un solo binario estático ejecuta contenedores Docker y OCI sin demonio, y guarda las imágenes archivo por archivo: menos disco, menos memoria y un arranque en unos 4 ms."
image: card-es.png
image_alt: "podbag 0.1.0: contenedores sin demonio, guardados archivo por archivo"
draft: false
---

Hoy publicamos podbag 0.1.0, la primera versión de podbag.

podbag es un motor de contenedores. Ejecuta tus imágenes Docker y OCI desde un solo binario estático. No tiene demonio. Guarda las imágenes archivo por archivo, no capa por capa.

¿Poco tiempo? Mira la [introducción de 30 segundos](/media/intro.mp4) (en inglés).

## Qué es podbag

- **Sin demonio.** Cuando no hay contenedores, no se ejecuta nada.
- **Un solo binario estático.** Unos 4 MB en Linux.
- **Archivos, no capas.** Un archivo que comparten muchas imágenes se guarda y se cachea una vez.
- **Rápido.** Un contenedor arranca en unos 4 ms en Linux.
- **Funciona con las herramientas de Docker.** La CLI `docker`, Compose y buildx.
- **Con o sin root.** El mismo programa funciona de las dos formas.
- **Linux, macOS y Windows.** El soporte de Windows es experimental.

## Sin demonio

Docker es un cliente y dos demonios. `dockerd` y `containerd` se ejecutan todo el tiempo, haya contenedores o no. Sin contenedores, siguen ocupando {{n:203}} MiB.

podbag es un solo programa:

- El comando `podbag` prepara cada contenedor él mismo y luego termina.
- Un pequeño keeper por usuario (unos 2 MiB) vigila los contenedores en marcha. Escribe sus registros y responde a `stop`, `kill` y `wait`.
- El keeper arranca con el primer contenedor. Se detiene 10 segundos después del último.
- Sin contenedores, no se ejecuta nada.

## Archivos, no capas

![Dos imágenes comparten casi todos sus archivos. Con capas, la capa superior de la imagen B cambia en un solo archivo, así que sus archivos compartidos se guardan otra vez: 8 archivos. podbag guarda cada archivo una vez: 6 archivos.](/images/storage-es-light.svg "Capas frente a archivos: si cambia un archivo, un almacén por capas guarda otra vez toda la capa.")

Otros motores guardan una imagen como capas. Una capa se guarda una sola vez solo si toda la capa es igual. Si cambia un archivo, se guarda otra vez toda la capa.

podbag divide cada capa en archivos y guarda cada archivo una sola vez. Una imagen es una lista de rutas a esos archivos. Cuando dos contenedores leen el mismo archivo, leen el mismo inodo, así que el kernel lo cachea una vez.

Medimos 8 servicios Spring en 2 versiones:

<!-- compare-columns: podbag docker -->
| | podbag | Docker | Ahorro de podbag |
|---|--:|--:|--:|
| Disco para las dos versiones | {{n:902}} MiB | {{n:2970}} MiB | 70 % |
| Caché de páginas para arrancar sus 16 servicios | {{n:324}} MiB | {{n:982}} MiB | 67 % |

Las descargas no cambian. Los registros sirven capas, y podbag las descarga enteras antes de dividirlas en archivos.

## Arranque y memoria

![Comparación de podbag con Docker, Podman y Kiri en una VM Linux: tiempo de arranque, memoria para 100 contenedores, memoria sin contenedores, disco y caché de páginas.](/images/perf.svg "podbag frente a Docker, Podman y Kiri, en una animación (en inglés).")

Ejecutamos todas las herramientas en la misma VM Linux: 4 CPU, {{n:3.8}} GiB, arm64. Las versiones: podbag 0.1.0, Podman 5.7.0, Docker 29.1.3 y Kiri 0.2.1. Los números son medianas. Menos es mejor.

<!-- compare-columns: podbag podbag kiri podman docker -->
| | podbag (rootless) | podbag (root) | Kiri | Podman | Docker |
|---|--:|--:|--:|--:|--:|
| Iniciar un contenedor | {{n:4.1}} ms | {{n:4.4}} ms | {{n:9.1}} ms | {{n:46.4}} ms | {{n:73.8}} ms |
| Memoria para 100 contenedores | {{n:117}} MiB | {{n:105}} MiB | {{n:109}} MiB | {{n:203}} MiB | {{n:562}} MiB |
| Procesos sin contenedores | {{n:0}} | {{n:0}} | {{n:1}} ({{n:5.9}} MiB) | {{n:1}} ({{n:0.6}} MiB) | {{n:4}} ({{n:203}} MiB) |

- El primer arranque, cuando todavía no hay keeper, tarda {{n:12.8}}–{{n:16.0}} ms.
- Kiri está cerca en memoria. podbag va por delante cuando no hay contenedores, porque entonces no se ejecuta nada suyo.
- Todos los números y cómo los medimos: [pruebas de rendimiento](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks.md) y la [prueba de microservicios Spring](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks-msa.md) (en inglés).
- La misma comparación en vídeo: [perf.mp4](/media/perf.mp4) (en inglés).

## Funciona con tus herramientas de Docker

`podbag system service` ofrece la API de Docker Engine en un socket. La CLI `docker`, Compose y buildx hablan con él.

```sh
podbag system service &
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podbag/docker.sock
docker compose up -d
```

- No es un demonio. Los contenedores no dependen de él.
- Se detiene tras 60 segundos sin clientes.
- Con systemd, puede arrancar con la primera conexión.

## Con o sin root

- El mismo programa funciona de las dos formas.
- Como root, podbag monta las imágenes con composefs.
- Sin root, crea árboles de enlaces duros, y `pasta` conecta los contenedores a la red.
- `podbag check` muestra lo que aún necesita tu sistema y cómo añadirlo.

## Linux, macOS y Windows

- **Linux:** x86_64 y arm64. Linux 5.12 o posterior, con cgroup v2.
- **macOS** (Apple silicon): podbag ejecuta una pequeña VM Linux propia. El primer comando la arranca en medio segundo, más o menos. La VM se apaga 60 segundos después del último contenedor. Seis minutos después del último contenedor, podbag ocupaba {{n:1.7}} MiB de la memoria del Mac.
- **Windows** (x86_64 y arm64): experimental. podbag ejecuta su motor Linux en una distribución WSL 2 propia. Se compila y se prueba en CI, pero todavía no se ha probado en una máquina Windows.

## Instalar

En Linux y macOS:

```sh
curl -fsSL https://podbag.dev/install.sh | sh
```

El script descarga el archivo para tu sistema, comprueba su suma SHA-256 y lo instala en `/usr/local/bin`.

También puedes descargar un archivo de la [página de la versión](https://github.com/SteelCrab/podbag/releases/tag/v0.1.0). Compruébalo con `SHA256SUMS`.

| Sistema | Archivo |
|---|---|
| Linux, x86_64 | `podbag-x86_64-linux` |
| Linux, arm64 | `podbag-aarch64-linux` |
| macOS, Apple silicon | `podbag-aarch64-macos` |
| Windows, x86_64 (experimental) | `podbag-x86_64-windows.exe` |
| Windows, arm64 (experimental) | `podbag-aarch64-windows.exe` |

Después, ejecuta tu primer contenedor:

```sh
podbag run --rm alpine echo hello
```

## Los límites de 0.1.0

Es una primera versión. Algunas cosas todavía no están:

- **Compilación:** los Dockerfile se compilan solo con buildx (`docker buildx build`). No hay compilador clásico.
- **Registros:** podbag descarga imágenes públicas. No hay inicio de sesión, ni descargas privadas, ni push.
- **Comandos de Docker:** no hay `commit`, `export`, `diff`, `stats`, `top`, `pause`, `rename` ni `update`.
- **Swarm:** no hay modo swarm ni plugins.
- **Kubernetes:** no hay CRI, así que un nodo de Kubernetes no puede usar podbag como runtime.
- **Windows:** experimental. La CLI `docker` de Windows todavía no llega a podbag.
- **Despertar en Mac:** el primer comando después de que la VM se apague tarda unos {{n:0.6}} s.

## Lo que viene

El trabajo en estos puntos está en [pull requests abiertas](https://github.com/SteelCrab/podbag/pulls). No está terminado y no damos fechas:

- inicio de sesión en registros, descargas privadas, push y search;
- compilación de Dockerfile, y `commit`, `export` y `diff`;
- un runtime para Kubernetes, para que un nodo ejecute sus pods con podbag;
- modo swarm en un nodo;
- `stats`, `top`, `pause`, `unpause`, `rename` y `update`;
- una interfaz de terminal y una aplicación de escritorio.

## Pruébalo y cuéntanos

- Lee la [guía de uso](https://github.com/SteelCrab/podbag/blob/main/docs/usage.md) (en inglés) para ver todos los comandos.
- Informa de errores e ideas en las [incidencias de GitHub](https://github.com/SteelCrab/podbag/issues). Los informes desde máquinas Windows son los que más ayudan.
- podbag es código abierto, con la Apache License 2.0.
