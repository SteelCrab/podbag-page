"""The architecture of the image-compression guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'podbag system compress stores the files of busybox with zstd; a container that uses the image decompresses it first, and system compression saves the idle setting',
    'ko': 'podbag system compress가 busybox의 파일을 zstd로 압축해 저장합니다. 이 이미지를 쓰는 컨테이너는 먼저 압축을 풀고, system compression은 idle 설정을 저장합니다',
    'ja': 'podbag system compress が busybox のファイルを zstd で圧縮して保存します。このイメージを使うコンテナーは先に展開し、system compression が idle の設定を保存します',
    'zh-CN': 'podbag system compress 用 zstd 压缩并保存 busybox 的文件；使用该镜像的容器会先解压它，system compression 保存 idle 设置',
    'fil': 'Iniimbak ng podbag system compress ang mga file ng busybox gamit ang zstd; dine-decompress muna ito ng container na gumagamit ng image, at sine-save ng system compression ang idle na setting',
    'es': 'podbag system compress guarda los archivos de busybox con zstd; un contenedor que usa la imagen la descomprime primero, y system compression guarda el ajuste idle',
    'vi': 'podbag system compress lưu các tệp của busybox bằng zstd; container dùng image này sẽ giải nén nó trước, còn system compression lưu cài đặt idle',
}

WORDS = {
    'en': {
        'commands': 'compress · df · decompress',
        'files': 'image · plain files',
        'compressed': 'Compressed store',
        'zstd': 'zstd, file by file',
        'compress': 'compress',
        'first': 'decompress first',
        'container': 'run --rm',
        'setting': 'image_compression = idle',
    },
    'ko': {
        'commands': 'compress · df · decompress',
        'files': '이미지 · 일반 파일',
        'compressed': '압축된 저장소',
        'zstd': '파일마다 zstd',
        'compress': '압축',
        'first': '먼저 압축 해제',
        'container': 'run --rm',
        'setting': 'image_compression = idle',
    },
    'ja': {
        'commands': 'compress · df · decompress',
        'files': 'イメージ · 通常のファイル',
        'compressed': '圧縮したストア',
        'zstd': 'ファイルごとに zstd',
        'compress': '圧縮',
        'first': '先に展開',
        'container': 'run --rm',
        'setting': 'image_compression = idle',
    },
    'zh-CN': {
        'commands': 'compress · df · decompress',
        'files': '镜像 · 普通文件',
        'compressed': '压缩的存储',
        'zstd': '逐个文件用 zstd',
        'compress': '压缩',
        'first': '先解压',
        'container': 'run --rm',
        'setting': 'image_compression = idle',
    },
    'fil': {
        'commands': 'compress · df · decompress',
        'files': 'image · karaniwang file',
        'compressed': 'Naka-compress na store',
        'zstd': 'zstd, bawat file',
        'compress': 'compress',
        'first': 'decompress muna',
        'container': 'run --rm',
        'setting': 'image_compression = idle',
    },
    'es': {
        'commands': 'compress · df · decompress',
        'files': 'imagen · archivos normales',
        'compressed': 'Almacén comprimido',
        'zstd': 'zstd, archivo por archivo',
        'compress': 'comprime',
        'first': 'descomprime antes',
        'container': 'run --rm',
        'setting': 'image_compression = idle',
    },
    'vi': {
        'commands': 'compress · df · decompress',
        'files': 'image · tệp thường',
        'compressed': 'Kho đã nén',
        'zstd': 'zstd, từng tệp',
        'compress': 'nén',
        'first': 'giải nén trước',
        'container': 'run --rm',
        'setting': 'image_compression = idle',
    },
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 80, 210, 56, w["terminal"], w["commands"], mono_name=False)
    p.box(330, 214, 240, 64, "config.toml", w["setting"])
    p.box(330, 90, 240, 64, "busybox:1.37.0", w["files"])
    p.box(670, 90, 240, 64, w["compressed"], w["zstd"], mono_name=False, color="podbag")
    p.box(670, 214, 240, 64, w["container"], 'echo "Hello …"')
    p.arrow(570, 122, 666, 122, w["compress"], dx=-26, dy=-8, color="podbag")
    p.arrow(790, 154, 790, 210, w["first"], dx=10, dy=4)
    p.arrow(250, 108, 326, 122, None, color="podbag")
    p.arrow(250, 120, 326, 240, None)
