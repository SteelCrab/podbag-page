"""The architecture of the local-registry guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The container registry serves a registry on 127.0.0.1:18105; podbag tags busybox with that address, pushes it there and pulls it back',
    'ko': 'registry 컨테이너가 127.0.0.1:18105에서 레지스트리를 엽니다. podbag은 이 주소로 busybox에 태그를 붙이고 push한 뒤 다시 pull합니다',
    'ja': 'コンテナ registry が 127.0.0.1:18105 でレジストリを提供します。podbag は busybox にそのアドレスでタグを付け、そこに push して pull で取り戻します',
    'zh-CN': '容器 registry 在 127.0.0.1:18105 上提供镜像仓库；podbag 用这个地址标记 busybox，推送到仓库，再拉取回来',
    'fil': 'Naghahain ang container na registry ng registry sa 127.0.0.1:18105; tina-tag ng podbag ang busybox gamit ang address na iyon, ipinu-push ito roon at ipinu-pull ulit',
    'es': 'El contenedor registry sirve un registro en 127.0.0.1:18105; podbag etiqueta busybox con esa dirección, la sube allí y la vuelve a descargar',
    'vi': 'Container registry phục vụ một registry tại 127.0.0.1:18105; podbag gắn tag địa chỉ đó cho busybox, đẩy image lên đó và kéo về lại',
}

WORDS = {
    'en': {
        'commands': 'tag · push · rmi · pull',
        'tag': 'tag',
        'push_pull': 'push · pull',
        'registry_note': 'registry:2.8.3 · :5000',
        'tagged': '127.0.0.1:18105/… · image',
    },
    'ko': {
        'commands': 'tag · push · rmi · pull',
        'tag': '태그',
        'push_pull': 'push · pull',
        'registry_note': 'registry:2.8.3 · :5000',
        'tagged': '127.0.0.1:18105/… · 이미지',
    },
    'ja': {
        'commands': 'tag · push · rmi · pull',
        'tag': 'タグ',
        'push_pull': 'push · pull',
        'registry_note': 'registry:2.8.3 · :5000',
        'tagged': '127.0.0.1:18105/… · イメージ',
    },
    'zh-CN': {
        'commands': 'tag · push · rmi · pull',
        'tag': 'tag',
        'push_pull': 'push · pull',
        'registry_note': 'registry:2.8.3 · :5000',
        'tagged': '127.0.0.1:18105/… · 镜像',
    },
    'fil': {
        'commands': 'tag · push · rmi · pull',
        'tag': 'tag',
        'push_pull': 'push · pull',
        'registry_note': 'registry:2.8.3 · :5000',
        'tagged': '127.0.0.1:18105/… · image',
    },
    'es': {
        'commands': 'tag · push · rmi · pull',
        'tag': 'tag',
        'push_pull': 'push · pull',
        'registry_note': 'registry:2.8.3 · :5000',
        'tagged': '127.0.0.1:18105/… · imagen',
    },
    'vi': {
        'commands': 'tag · push · rmi · pull',
        'tag': 'tag',
        'push_pull': 'push · pull',
        'registry_note': 'registry:2.8.3 · :5000',
        'tagged': '127.0.0.1:18105/… · image',
    },
}


def draw(p, w):
    frame(p, w, 330)
    p.box(40, 80, 210, 56, w["terminal"], w["commands"], mono_name=False)
    p.box(330, 90, 230, 64, "busybox:1.37.0", w["image"])
    p.box(330, 214, 270, 64, "training/busybox:1", w["tagged"])
    p.box(680, 150, 230, 96, "registry", w["registry_note"], port="127.0.0.1:18105")
    p.arrow(445, 154, 445, 210, w["tag"], dx=10, dy=4)
    p.arrow(600, 238, 676, 214, w["push_pull"], dx=-30, dy=22, both=True, color="accent")
