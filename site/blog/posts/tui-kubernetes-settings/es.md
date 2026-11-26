---
title: "Podbag TUI · Kubernetes y ajustes"
date: 2026-11-27
author: team
categories: [how-to]
tags: [tui, kubernetes, settings]
summary: "Mira los pods, servicios, despliegues y solicitudes de volumen de un clúster, y cambia el motor, la VM, el idioma y el tema en Ajustes."
image: tui-settings-es.png
image_alt: "El menú Ajustes de podbag tui"
outline: "En esta guía"
draft: false
---

La TUI muestra los recursos de un clúster de Kubernetes. Su página **Ajustes** cambia cómo funcionan podbag y la TUI.

**Tiempo** 5 minutos.

## Mira un clúster de Kubernetes

La TUI usa `kubectl` y sus contextos. Instala `kubectl` primero.

1. Pulsa `F6`.
2. Elige el contexto del clúster: **Contexto actual** o un contexto por su nombre.
3. Elige el espacio de nombres: el del contexto o **Todos los espacios de nombres**.
4. Elige el tipo de recurso. Cada tipo muestra su número de elementos.

![Los recursos de Kubernetes en podbag tui con su número de elementos](tui-kubernetes-es.png)

La lista muestra cada recurso como `namespace/nombre`. Pulsa `Enter` para verlo en JSON. **Actualizar** vuelve a leer la lista. La TUI solo lee el clúster. No lo cambia.

## Cambia los ajustes

Pulsa `F9`.

![El menú Ajustes de podbag tui](tui-settings-es.png)

- **Motor:** conéctate a otro motor o mira la versión del motor.
- **Máquina virtual:** con podbag en macOS y Windows. Mira la VM, iníciala, detenla o reiníciala. **Aplicar** cambia las CPU, la memoria y el tiempo de inactividad. Pregunta si el cambio se aplica ahora o en el próximo inicio.
- **Actualizaciones:** mira la versión, busca una actualización y actualiza podbag.
- **Idioma:** el idioma del sistema o uno de siete idiomas.
- **Tema:** los colores del sistema, claro u oscuro.
- **Abrir Podbag Desktop al iniciar sesión:** actívalo o desactívalo.
- **Terminal:** abre tu shell. Escribe `exit` para volver a la TUI.
- **Acerca de** y **Abrir GitHub.**

La TUI guarda el idioma, el tema y la barra lateral en `terminal.json`. La carpeta es `~/.podbag` en macOS, `~/.config/podbag` en Linux y `%LOCALAPPDATA%\podbag` en Windows.

## Usa los menús

Estas páginas son menús. `↑` `↓` eligen, al escribir se filtra el menú, `Enter` abre y `Esc` vuelve atrás.

## Más

La [guía de uso de podbag](https://github.com/SteelCrab/podbag/blob/main/docs/usage.md) tiene todas las teclas y opciones de la TUI. Vuelve a [cómo usar la TUI](/es/training/tui/).
