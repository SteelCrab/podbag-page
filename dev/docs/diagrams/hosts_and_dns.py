"""The architecture of the hosts-and-dns guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'podbag run --add-host writes db.training into the container\'s /etc/hosts; --dns, --dns-search and --dns-option write the nameserver, search and options lines of /etc/resolv.conf in dns-demo',
    'ko': 'podbag run --add-host가 컨테이너의 /etc/hosts에 db.training을 씁니다. --dns, --dns-search, --dns-option은 dns-demo의 /etc/resolv.conf에 nameserver, search, options 줄을 씁니다',
    'ja': 'podbag run --add-host がコンテナーの /etc/hosts に db.training を書きます。--dns、--dns-search、--dns-option は dns-demo の /etc/resolv.conf に nameserver、search、options の行を書きます',
    'zh-CN': 'podbag run --add-host 把 db.training 写入容器的 /etc/hosts；--dns、--dns-search 和 --dns-option 在 dns-demo 的 /etc/resolv.conf 中写入 nameserver、search 和 options 行',
    'fil': 'Isinusulat ng podbag run --add-host ang db.training sa /etc/hosts ng container; isinusulat ng --dns, --dns-search at --dns-option ang mga linyang nameserver, search at options sa /etc/resolv.conf ng dns-demo',
    'es': 'podbag run --add-host escribe db.training en el /etc/hosts del contenedor; --dns, --dns-search y --dns-option escriben las líneas nameserver, search y options del /etc/resolv.conf de dns-demo',
    'vi': 'podbag run --add-host ghi db.training vào /etc/hosts của container; --dns, --dns-search và --dns-option ghi các dòng nameserver, search và options trong /etc/resolv.conf của dns-demo',
}

WORDS = {
    'en': {'commands': 'podbag run · exec · rm'},
    'ko': {'commands': 'podbag run · exec · rm'},
    'ja': {'commands': 'podbag run · exec · rm'},
    'zh-CN': {'commands': 'podbag run · exec · rm'},
    'fil': {'commands': 'podbag run · exec · rm'},
    'es': {'commands': 'podbag run · exec · rm'},
    'vi': {'commands': 'podbag run · exec · rm'},
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 80, 210, 56, w["terminal"], w["commands"], mono_name=False)
    p.box(330, 90, 230, 64, "cat (--rm)", "--add-host")
    p.box(650, 90, 260, 64, "/etc/hosts", "192.0.2.10 db.training")
    p.box(330, 214, 230, 64, "dns-demo", "--dns · --dns-search · --dns-option")
    p.box(650, 200, 260, 92, "/etc/resolv.conf", "nameserver 192.0.2.53 · search · options")
    p.arrow(560, 122, 646, 122, w["writes"], dx=-22, dy=-8, color="accent")
    p.arrow(560, 246, 646, 246, w["writes"], dx=-22, dy=-8, color="accent")
    p.arrow(250, 108, 326, 122, None, color="podbag")
    p.arrow(250, 120, 326, 240, None, color="podbag")
