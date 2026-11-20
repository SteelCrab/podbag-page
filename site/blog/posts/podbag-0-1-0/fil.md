---
title: "podbag 0.1.0: mga container na walang daemon, iniimbak file por file"
date: 2026-11-20
author: team
categories: [announcements]
tags: [release, docker, compose, rootless, macos, windows]
summary: "Labas na ang unang release ng podbag. Isang static binary ang nagpapatakbo ng mga Docker at OCI container nang walang daemon, at iniimbak nito ang mga image file por file: mas kaunting disk, mas kaunting memory, at nagsisimula sa mga 4 ms."
image: card-fil.png
image_alt: "podbag 0.1.0: mga container na walang daemon, iniimbak file por file"
draft: false
---

Ngayong araw, inilalabas namin ang podbag 0.1.0, ang unang bersyon ng podbag.

Ang podbag ay isang container engine. Pinapatakbo nito ang iyong mga Docker at OCI image mula sa isang static binary. Wala itong daemon. Iniimbak nito ang mga image file por file, hindi layer por layer.

Kulang sa oras? Panoorin ang [30 segundong intro](/media/intro.mp4) (sa English).

## Ano ang podbag

- **Walang daemon.** Kapag walang container na tumatakbo, walang tumatakbo.
- **Isang static binary.** Mga 4 MB sa Linux.
- **Mga file, hindi layer.** Ang file na ginagamit ng maraming image ay iniimbak at kina-cache nang isang beses.
- **Mabilis.** Nagsisimula ang isang container sa mga 4 ms sa Linux.
- **Gumagana sa mga Docker tool.** Ang `docker` CLI, Compose at buildx.
- **May root man o wala.** Gumagana ang iisang program sa dalawang paraan.
- **Linux, macOS at Windows.** Experimental pa ang suporta sa Windows.

## Walang daemon

Ang Docker ay isang client at dalawang daemon. Laging tumatakbo ang `dockerd` at `containerd`, may container man o wala. Kahit walang container, gumagamit pa rin sila ng {{n:203}} MiB.

Iisang program ang podbag:

- Ang `podbag` command mismo ang nag-aayos ng bawat container, at saka ito natatapos.
- Isang maliit na keeper bawat user (mga 2 MiB) ang nagbabantay sa mga tumatakbong container. Isinusulat nito ang kanilang mga log, at sinasagot nito ang `stop`, `kill` at `wait`.
- Nagsisimula ang keeper kasabay ng unang container. Humihinto ito 10 segundo pagkatapos ng huli.
- Kapag walang container, walang tumatakbo.

## Mga file, hindi layer

![Halos lahat ng file ay pareho sa dalawang image. Sa mga layer, isang file lang ang iba sa itaas na layer ng image B, kaya iniimbak ulit pati ang mga parehong file: 8 file. Iniimbak ng podbag ang bawat file nang isang beses: 6 na file.](/images/storage-fil-light.svg "Mga layer laban sa mga file: kapag may isang file na nagbago, iniimbak ulit ng layer store ang buong layer.")

Iniimbak ng ibang engine ang isang image bilang mga layer. Isang beses lang iniimbak ang layer kapag pareho ang buong layer. Kapag may isang file na nagbago, iniimbak ulit ang buong layer.

Hinahati ng podbag ang bawat layer sa mga file, at iniimbak ang bawat file nang isang beses. Ang image ay listahan ng mga path papunta sa mga file na ito. Kapag binasa ng dalawang container ang parehong file, iisang inode ang binabasa nila, kaya isang beses lang itong kina-cache ng kernel.

Sinukat namin ang 8 Spring service sa 2 release:

<!-- compare-columns: podbag docker -->
| | podbag | Docker | Natitipid ng podbag |
|---|--:|--:|--:|
| Disk para sa dalawang release | {{n:902}} MiB | {{n:2970}} MiB | 70% |
| Page cache para simulan ang 16 na service | {{n:324}} MiB | {{n:982}} MiB | 67% |

Pareho pa rin ang laki ng mga download. Mga layer ang ibinibigay ng mga registry, at buo itong dina-download ng podbag bago hatiin sa mga file.

## Oras ng pagsisimula at memory

![Paghahambing ng podbag sa Docker, Podman at Kiri sa isang Linux VM: oras ng pagsisimula, memory para sa 100 container, memory kapag walang container, disk at page cache.](/images/perf.svg "Ang podbag laban sa Docker, Podman at Kiri, bilang animation (sa English).")

Pinatakbo namin ang bawat tool sa iisang Linux VM: 4 na CPU, {{n:3.8}} GiB, arm64. Ang mga bersyon: podbag 0.1.0, Podman 5.7.0, Docker 29.1.3 at Kiri 0.2.1. Mga median ang mga numero. Mas mababa, mas mabuti.

<!-- compare-columns: podbag podbag kiri podman docker -->
| | podbag (rootless) | podbag (root) | Kiri | Podman | Docker |
|---|--:|--:|--:|--:|--:|
| Magsimula ng container | {{n:4.1}} ms | {{n:4.4}} ms | {{n:9.1}} ms | {{n:46.4}} ms | {{n:73.8}} ms |
| Memory para sa 100 container | {{n:117}} MiB | {{n:105}} MiB | {{n:109}} MiB | {{n:203}} MiB | {{n:562}} MiB |
| Mga process kapag walang container | {{n:0}} | {{n:0}} | {{n:1}} ({{n:5.9}} MiB) | {{n:1}} ({{n:0.6}} MiB) | {{n:4}} ({{n:203}} MiB) |

- Ang unang pagsisimula, kapag wala pang keeper, ay tumatagal ng {{n:12.8}}–{{n:16.0}} ms.
- Malapit ang Kiri sa memory. Nangunguna ang podbag kapag walang container, dahil wala itong pinapatakbo noon.
- Lahat ng numero, at kung paano namin sinukat: [mga benchmark](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks.md) at ang [benchmark ng Spring microservices](https://github.com/SteelCrab/podbag/blob/main/docs/benchmarks-msa.md) (sa English).
- Ang parehong paghahambing bilang video: [perf.mp4](/media/perf.mp4) (sa English).

## Gumagana sa iyong mga Docker tool

Nagbibigay ang `podbag system service` ng Docker Engine API sa isang socket. Dito kumakausap ang `docker` CLI, Compose at buildx.

```sh
podbag system service &
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podbag/docker.sock
docker compose up -d
```

- Hindi ito daemon. Hindi umaasa rito ang mga container.
- Humihinto ito pagkalipas ng 60 segundo kapag walang client.
- Sa systemd, puwede itong magsimula sa unang koneksyon.

## May root man o wala

- Gumagana ang iisang program sa dalawang paraan.
- Kapag root, mina-mount ng podbag ang mga image gamit ang composefs.
- Kapag walang root, gumagawa ito ng mga tree ng hard link, at ikinokonekta ng `pasta` ang mga container sa network.
- Ipinapakita ng `podbag check` kung ano pa ang kailangan ng iyong system, at kung paano ito idagdag.

## Linux, macOS at Windows

- **Linux:** x86_64 at arm64. Linux 5.12 o mas bago, na may cgroup v2.
- **macOS** (Apple silicon): nagpapatakbo ang podbag ng sarili nitong maliit na Linux VM. Sinisimulan ito ng unang command sa mga kalahating segundo. Namamatay ang VM 60 segundo pagkatapos ng huling container. Anim na minuto pagkatapos ng huling container, {{n:1.7}} MiB lang ng memory ng Mac ang hawak ng podbag.
- **Windows** (x86_64 at arm64): experimental. Pinapatakbo ng podbag ang Linux engine nito sa sarili nitong WSL 2 distribution. Bina-build at tine-test ito sa CI, pero hindi pa nasusubukan sa totoong Windows machine.

## I-install

Sa Linux at macOS:

```sh
curl -fsSL https://podbag.dev/install.sh | sh
```

Dina-download ng script ang file para sa iyong system, sinusuri ang SHA-256 sum nito, at ini-install ito sa `/usr/local/bin`.

Puwede ka ring kumuha ng file mula sa [page ng release](https://github.com/SteelCrab/podbag/releases/tag/v0.1.0). Suriin ito gamit ang `SHA256SUMS`.

| System | File |
|---|---|
| Linux, x86_64 | `podbag-x86_64-linux` |
| Linux, arm64 | `podbag-aarch64-linux` |
| macOS, Apple silicon | `podbag-aarch64-macos` |
| Windows, x86_64 (experimental) | `podbag-x86_64-windows.exe` |
| Windows, arm64 (experimental) | `podbag-aarch64-windows.exe` |

Pagkatapos, patakbuhin ang iyong unang container:

```sh
podbag run --rm alpine echo hello
```

## Mga limitasyon ng 0.1.0

Unang release ito. May ilang bagay na wala pa:

- **Build:** sa buildx lang (`docker buildx build`) nabi-build ang mga Dockerfile. Walang classic builder.
- **Registry:** mga public image lang ang napu-pull ng podbag. Walang login, walang private pull at walang push.
- **Mga Docker command:** walang `commit`, `export`, `diff`, `stats`, `top`, `pause`, `rename` o `update`.
- **Swarm:** walang swarm mode, at walang plugin.
- **Kubernetes:** walang CRI, kaya hindi magagamit ng Kubernetes node ang podbag bilang runtime.
- **Windows:** experimental. Hindi pa naaabot ng `docker` CLI sa Windows ang podbag.
- **Paggising sa Mac:** ang unang command pagkatapos mamatay ang VM ay tumatagal ng mga {{n:0.6}} s.

## Ang susunod

Nasa mga [bukas na pull request](https://github.com/SteelCrab/podbag/pulls) ang trabaho sa mga ito. Hindi pa tapos ang mga ito, at wala kaming ibinibigay na petsa:

- mga login sa registry, private pull, push at search;
- mga Dockerfile build, at `commit`, `export` at `diff`;
- isang Kubernetes runtime, para mapatakbo ng node ang mga pod nito gamit ang podbag;
- swarm mode sa isang node;
- `stats`, `top`, `pause`, `unpause`, `rename` at `update`;
- isang terminal UI at isang desktop app.

## Subukan at sabihin sa amin

- Basahin ang [gabay sa paggamit](https://github.com/SteelCrab/podbag/blob/main/docs/usage.md) (sa English) para sa lahat ng command.
- I-report ang mga bug at ideya sa [GitHub issues](https://github.com/SteelCrab/podbag/issues). Pinakamakakatulong ang mga report mula sa mga Windows machine.
- Open source ang podbag, sa ilalim ng Apache License 2.0.
