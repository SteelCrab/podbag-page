"""The architecture of the container-changes guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The container app writes /hello.txt; podbag commit turns its changes into the image app-snapshot:1, and podbag export writes its files to app.tar',
    'ko': 'app 컨테이너가 /hello.txt를 씁니다. podbag commit은 변경 내용을 app-snapshot:1 이미지로 만들고, podbag export는 파일을 app.tar로 씁니다',
    'ja': 'コンテナ app が /hello.txt を書きます。podbag commit がその変更をイメージ app-snapshot:1 にし、podbag export がファイルを app.tar に書き出します',
    'zh-CN': '容器 app 写入 /hello.txt；podbag commit 把它的更改变成镜像 app-snapshot:1，podbag export 把它的文件写入 app.tar',
    'fil': 'Isinusulat ng container na app ang /hello.txt; ginagawang image na app-snapshot:1 ng podbag commit ang mga pagbabago nito, at isinusulat ng podbag export ang mga file nito sa app.tar',
    'es': 'El contenedor app escribe /hello.txt; podbag commit convierte sus cambios en la imagen app-snapshot:1, y podbag export escribe sus archivos en app.tar',
    'vi': 'Container app ghi /hello.txt; podbag commit biến các thay đổi của nó thành image app-snapshot:1, còn podbag export ghi các tệp của nó vào app.tar',
}

WORDS = {
    'en': {
        'commit': 'commit',
        'export': 'export',
        'changed': 'A /hello.txt · exited (0)',
        'tar': 'all files of app',
    },
    'ko': {
        'commit': 'commit',
        'export': 'export',
        'changed': 'A /hello.txt · 종료됨 (0)',
        'tar': 'app의 모든 파일',
    },
    'ja': {
        'commit': 'commit',
        'export': 'export',
        'changed': 'A /hello.txt · 終了 (0)',
        'tar': 'app のすべてのファイル',
    },
    'zh-CN': {
        'commit': 'commit',
        'export': 'export',
        'changed': 'A /hello.txt · 已退出 (0)',
        'tar': 'app 的所有文件',
    },
    'fil': {
        'commit': 'commit',
        'export': 'export',
        'changed': 'A /hello.txt · nakahinto (0)',
        'tar': 'lahat ng file ng app',
    },
    'es': {
        'commit': 'commit',
        'export': 'export',
        'changed': 'A /hello.txt · exited (0)',
        'tar': 'todos los archivos de app',
    },
    'vi': {
        'commit': 'commit',
        'export': 'export',
        'changed': 'A /hello.txt · exited (0)',
        'tar': 'mọi tệp của app',
    },
}


def draw(p, w):
    frame(p, w, 330)
    p.box(40, 110, 210, 60, w["terminal"], "podbag diff · commit · export", mono_name=False)
    p.box(330, 90, 240, 64, "app", w["changed"])
    p.box(680, 90, 230, 64, "app-snapshot:1", w["image"])
    p.box(330, 220, 240, 64, "app.tar", w["tar"])
    p.box(680, 220, 230, 64, "run --rm", "cat /hello.txt")
    p.arrow(250, 140, 326, 122, None, color="podbag")
    p.arrow(570, 122, 676, 122, w["commit"], dx=-24, dy=-8)
    p.arrow(450, 154, 450, 216, w["export"], dx=10, dy=4)
    p.arrow(795, 154, 795, 216, w["runs"], dx=10, dy=4)
