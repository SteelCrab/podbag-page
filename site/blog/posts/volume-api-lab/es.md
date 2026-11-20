---
title: "Práctica · Leer por HTTP el JSON de un volumen"
date: 2026-11-20
author: team
categories: [how-to]
tags: [desktop, tutorials, volumes, http]
summary: "Crea un volumen, escribe un archivo y lee tu mensaje desde un servidor local."
image: 08-response-es.png
image_alt: "Respuesta HTTP 200 con el JSON leído del volumen."
draft: false
---

Usa una versión de Podbag Desktop con **Tutoriales** en la barra lateral. La práctica usa almacenamiento temporal local. Puedes hacerla sin descargar imágenes ni ejecutar contenedores.

[Descargar el módulo de práctica](volume-api.podbag)

Guarda `volume-api.podbag` y recuerda su ubicación.

## Abre Tutoriales

Selecciona **Tutoriales** en la barra lateral. La primera vez verás el instalador.

![El instalador ofrece Elegir archivo.](01-open-es.png)

## Elige el módulo

Pulsa **Elegir archivo** y abre `volume-api.podbag`. Comprueba el título y el nombre antes de continuar.

![Título y nombre del archivo seleccionado.](02-file-es.png)

## Instala e inicia la práctica

Pulsa **Instalar módulo**. Cuando aparezca como instalado, pulsa **Iniciar práctica** para abrir un espacio vacío.

![Módulo instalado con el objetivo de la práctica.](03-installed-es.png)

## Crea un volumen

Escribe `my-api` como nombre y pulsa **Crear volumen**. El nombre aparecerá al principio de la ruta en la siguiente pantalla.

![Campo de nombre con el valor my-api.](04-volume-es.png)

## Escribe la respuesta

Cambia el valor de `message` por tu saludo, por ejemplo `Hello from my lab!`. Conserva las comillas y las llaves. Pulsa **Guardar archivo**.

![El editor de response.json contiene el saludo personalizado.](05-write-es.png)

## Inicia el servidor

Revisa el JSON guardado y pulsa **Iniciar servidor**. La aplicación elige un puerto libre en `127.0.0.1`.

![JSON guardado y botón para iniciar el servidor.](06-saved-es.png)

## Envía una solicitud

Pulsa **Enviar GET /** para leer la ruta raíz. También puedes copiar la URL en un navegador de este equipo. El puerto puede cambiar en cada sesión.

![URL local y botón para enviar GET /.](07-server-es.png)

## Comprueba y modifica la respuesta

Busca tu mensaje debajo de `HTTP 200`. Pulsa **Editar archivo**, cambia el saludo y guárdalo. Envía otra solicitud a la misma URL para ver el cambio.

![Respuesta HTTP 200 con el JSON leído del volumen.](08-response-es.png)

## Finaliza la práctica

Pulsa **Finalizar práctica** y confirma. El servidor se detiene y se eliminan el volumen temporal y sus archivos. Se conservan el módulo y el registro de finalización.

![Cuadro de confirmación para cerrar el servidor y eliminar los archivos temporales.](09-end-es.png)
