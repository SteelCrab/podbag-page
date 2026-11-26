"""The architecture of the image-build guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'podbag build makes the image my-site:1 from the folder my-site; the container web runs it and publishes 127.0.0.1:18095',
    'ko': 'podbag build가 my-site 폴더로 my-site:1 이미지를 만듭니다. web 컨테이너가 이 이미지를 실행하고 127.0.0.1:18095를 공개합니다',
    'ja': 'podbag build がフォルダー my-site からイメージ my-site:1 を作ります。コンテナ web がそれを実行し、127.0.0.1:18095 を公開します',
    'zh-CN': 'podbag build 用文件夹 my-site 制作镜像 my-site:1；容器 web 运行该镜像并发布 127.0.0.1:18095',
    'fil': 'Ginagawa ng podbag build ang image na my-site:1 mula sa folder na my-site; pinapatakbo ito ng container na web at nagpa-publish ito ng 127.0.0.1:18095',
    'es': 'podbag build crea la imagen my-site:1 a partir de la carpeta my-site; el contenedor web la ejecuta y publica 127.0.0.1:18095',
    'vi': 'podbag build tạo image my-site:1 từ thư mục my-site; container web chạy image này và công bố 127.0.0.1:18095',
}

WORDS = {
    'en': {
        'build': 'build',
        'folder': 'Dockerfile · index.html',
    },
    'ko': {
        'build': '빌드',
        'folder': 'Dockerfile · index.html',
    },
    'ja': {
        'build': 'ビルド',
        'folder': 'Dockerfile · index.html',
    },
    'zh-CN': {
        'build': 'build',
        'folder': 'Dockerfile · index.html',
    },
    'fil': {
        'build': 'build',
        'folder': 'Dockerfile · index.html',
    },
    'es': {
        'build': 'build',
        'folder': 'Dockerfile · index.html',
    },
    'vi': {
        'build': 'build',
        'folder': 'Dockerfile · index.html',
    },
}


def draw(p, w):
    frame(p, w, 330)
    p.box(40, 80, 210, 56, w["terminal"], "podbag build · run · rm", mono_name=False)
    p.box(40, 152, 210, 56, w["desktop"], w["ports"], mono_name=False)
    p.box(40, 240, 210, 42, w["browser"], mono_name=False)
    p.box(330, 90, 210, 64, "my-site/", w["folder"])
    p.box(640, 90, 220, 64, "my-site:1", w["image"])
    p.box(600, 210, 310, 80, "web", "httpd :8080", port="127.0.0.1:18095")
    p.arrow(540, 122, 636, 122, w["build"], dx=-18, dy=-8)
    p.arrow(750, 154, 750, 206, w["runs"], dx=10, dy=4)
    p.arrow(250, 261, 596, 256, None, color="accent")
