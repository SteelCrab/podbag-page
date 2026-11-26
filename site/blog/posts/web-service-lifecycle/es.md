---
title: "Podbag Training · Sustituye y limpia un servicio web"
date: 2026-11-21
author: team
categories: [how-to]
tags: [cli, containers, desktop, training]
summary: "Sustituye un servicio web en ejecución sin perder su contenido."
image: gui-ports-en.png
image_alt: "Sustituye y limpia un servicio web"
outline: "Flujo de la práctica"
draft: false
---

Sustituye un servicio web en ejecución sin perder su contenido. Usa el mismo volumen y la misma dirección local antes y después del cambio.

**Tiempo** 15 minutos

![site-v1 escribe la página en el volumen site-data y site-v2 lo sustituye y sirve la misma página en 127.0.0.1:18081](architecture-es-light.svg)

## Curso de iniciación

[Ejecuta tu primer contenedor](../container-basics/) → [Abre un servidor web en el navegador](../web-basics/) → [Conserva archivos entre contenedores](../volume-persistence/) → **Sustituye y limpia un servicio web**

## Instala el módulo

[Descargar web-service-lifecycle.podbag](web-service-lifecycle.podbag). En Desktop, selecciona **Instalar módulo** en la parte superior de **Training**. Elige el archivo descargado y confirma.

```sh
podbag lab install web-service-lifecycle.podbag
```

![Confirmación de instalación con el nombre del módulo y del archivo](install-en.png)

## Inicia la sesión de práctica

Despliega **Training** en la barra lateral y selecciona el módulo. Copia el comando de inicio en tu terminal. Continúa cuando aparezca el prompt `training $`.

```sh
podbag lab start web-service-lifecycle
```

![Inicia la sesión de práctica](start-en.png)

Si el puerto predeterminado ya está en uso, usa el puerto que indica Training. El comando y la dirección del navegador muestran el mismo puerto.

## Crea el volumen del sitio

Crea `site-data` para guardar la página web.

```sh
podbag volume create site-data
```

![Crea el volumen del sitio](create-en.png)

## Inicia el primer servidor

Inicia `site-v1`. Escribe `index.html` en el volumen y lo sirve en el puerto publicado. El puerto predeterminado en tu computadora es `18081`.

```sh
podbag run -d --name site-v1 -p 127.0.0.1:18081:8080 -v site-data:/site docker.io/library/busybox:1.37.0 sh -c 'printf "%s\n" "My Podbag site" > /site/index.html && exec httpd -f -p 8080 -h /site'
```

![Inicia el primer servidor](runFirst-en.png)

## Comprueba los puertos del primer servidor

Selecciona **Contenedores de práctica → site-v1 → Ver puertos**. Comprueba la dirección en el panel de detalles.

![Comprueba los puertos del primer servidor](ports-en.png)

![Comprueba los puertos del primer servidor](gui-ports-en.png)

## Abre la página del primer servidor

Selecciona **Abrir en el navegador**. Comprueba que la página muestra **My Podbag site**.

![Abre la página del primer servidor](browser-en.png)

![Abre la página del primer servidor](web-browser-en.png)

## Detén el primer servidor

Selecciona **Contenedores de práctica → site-v1 → Detener**.

![Detén el primer servidor](stop-en.png)

![Detén el primer servidor](gui-stop-en.png)

## Elimina el primer servidor

Ejecuta el comando de eliminación. El contenedor desaparece y `site-data` sigue en la sesión de práctica.

```sh
podbag rm site-v1
```

![Elimina el primer servidor](remove-en.png)

## Inicia el servidor de sustitución

Inicia `site-v2` en el mismo puerto. Monta `site-data` en modo de solo lectura. El servidor usa la página que ya está guardada en el volumen.

```sh
podbag run -d --name site-v2 -p 127.0.0.1:18081:8080 -v site-data:/site:ro docker.io/library/busybox:1.37.0 httpd -f -p 8080 -h /site
```

![Inicia el servidor de sustitución](runReplacement-en.png)

## Comprueba los puertos del servidor de sustitución

Selecciona **Contenedores de práctica → site-v2 → Ver puertos**. Comprueba que la dirección es la misma que la del primer servidor.

![Comprueba los puertos del servidor de sustitución](portsReplacement-en.png)

![Comprueba los puertos del servidor de sustitución](gui-ports-replacement-en.png)

## Abre la página del servidor de sustitución

Selecciona de nuevo **Abrir en el navegador**. La página sigue mostrando **My Podbag site**. Desktop comprueba la respuesta con una solicitud nueva.

![Abre la página del servidor de sustitución](browserReplacement-en.png)

![Abre la página del servidor de sustitución](web-browserReplacement-en.png)

## Detén el servidor de sustitución

Selecciona **Contenedores de práctica → site-v2 → Detener**.

![Detén el servidor de sustitución](stopReplacement-en.png)

![Detén el servidor de sustitución](gui-stop-replacement-en.png)

## Elimina el servidor de sustitución

Elimina el contenedor detenido en la misma terminal.

```sh
podbag rm site-v2
```

![Elimina el servidor de sustitución](removeReplacement-en.png)

## Abre los detalles del volumen del sitio

Selecciona **Volúmenes de práctica → site-data** para ver el volumen que queda.

![Abre los detalles del volumen del sitio](inspect-en.png)

![Abre los detalles del volumen del sitio](gui-inspect-en.png)

## Elimina el volumen del sitio

Selecciona **Eliminar** y confirma el nombre del volumen.

![Elimina el volumen del sitio](delete-en.png)

![Elimina el volumen del sitio](gui-delete-en.png)

## Comprueba la lista de contenedores

Lista todos los contenedores de la sesión de práctica. La lista está vacía.

```sh
podbag ps -a
```

![Comprueba la lista de contenedores](checkContainers-en.png)

## Comprueba la lista de volúmenes

Lista los volúmenes de práctica. La lista está vacía.

```sh
podbag volume ls
```

![Comprueba la lista de volúmenes](checkVolumes-en.png)

## Termina la sesión de práctica

Ejecuta el comando del último paso. Training registra la finalización cuando se ha eliminado el entorno de práctica.

```sh
exit
```

![Termina la sesión de práctica](finish-en.png)

![Training muestra todos los pasos completados](complete-en.png)

[Siguiente módulo de Training · Recupera un servidor web con los registros](../web-service-recovery/)
