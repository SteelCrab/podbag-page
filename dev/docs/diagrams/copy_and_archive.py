"""The architecture of the copy-and-archive guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 350

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'docker cp copies note.txt into the container app and reply.txt out of it; podbag save and load move the busybox image through busybox.tar',
    'ko': 'docker cp가 note.txt를 app 컨테이너에 넣고 reply.txt를 꺼냅니다. podbag save와 load는 busybox 이미지를 busybox.tar로 옮깁니다',
    'ja': 'docker cp が note.txt をコンテナ app にコピーし、reply.txt を取り出します。podbag save と load が busybox.tar を使って busybox イメージを移します',
    'zh-CN': 'docker cp 将 note.txt 复制到容器 app 中，并将 reply.txt 复制出来；podbag save 和 load 通过 busybox.tar 迁移 busybox 镜像',
    'fil': 'Kinokopya ng docker cp ang note.txt papasok sa container na app at ang reply.txt palabas dito; inililipat ng podbag save at load ang image na busybox sa pamamagitan ng busybox.tar',
    'es': 'docker cp copia note.txt al contenedor app y reply.txt desde él; podbag save y load mueven la imagen busybox a través de busybox.tar',
    'vi': 'docker cp sao chép note.txt vào container app và sao chép reply.txt ra ngoài; podbag save và load chuyển image busybox qua busybox.tar',
}

WORDS = {
    'en': {
        'folder': 'practice folder',
        'cp': 'docker cp',
        'save_load': 'save / load',
    },
    'ko': {
        'folder': '실습 폴더',
        'cp': 'docker cp',
        'save_load': 'save / load',
    },
    'ja': {
        'folder': '実習フォルダー',
        'cp': 'docker cp',
        'save_load': 'save / load',
    },
    'zh-CN': {
        'folder': '练习目录',
        'cp': 'docker cp',
        'save_load': 'save / load',
    },
    'fil': {
        'folder': 'practice folder',
        'cp': 'docker cp',
        'save_load': 'save / load',
    },
    'es': {
        'folder': 'carpeta de práctica',
        'cp': 'docker cp',
        'save_load': 'save / load',
    },
    'vi': {
        'folder': 'thư mục thực hành',
        'cp': 'docker cp',
        'save_load': 'save / load',
    },
}


def draw(p, w):
    frame(p, w, 350)
    p.box(40, 110, 210, 60, w["terminal"], "podbag · docker cp", mono_name=False)
    p.box(330, 86, 200, 52, "note.txt", w["folder"])
    p.box(330, 158, 200, 52, "reply.txt", w["folder"])
    p.box(680, 96, 230, 96, "app", "/tmp/note.txt · /reply.txt")
    p.box(330, 256, 200, 56, "busybox.tar", w["folder"])
    p.box(680, 256, 230, 56, "busybox:1.37.0", w["image"])
    p.arrow(530, 112, 676, 124, w["cp"], dx=-30, dy=-10, mono=True)
    p.arrow(676, 166, 530, 184, w["cp"], dx=-30, dy=24, mono=True)
    p.arrow(530, 284, 676, 284, w["save_load"], dx=-32, dy=-8, both=True)
    p.arrow(795, 252, 795, 196, w["runs"], dx=10, dy=4)
