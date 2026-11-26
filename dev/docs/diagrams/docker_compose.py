"""The architecture of the docker-compose guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 350

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'docker compose reads compose.yaml and starts api and web on the network lab_default; web reaches api by name and publishes 127.0.0.1:18107',
    'ko': 'docker compose가 compose.yaml을 읽고 lab_default 네트워크에 api와 web을 시작합니다. web은 이름으로 api에 접속하고 127.0.0.1:18107을 공개합니다',
    'ja': 'docker compose が compose.yaml を読み、ネットワーク lab_default 上で api と web を起動します。web は名前で api に接続し、127.0.0.1:18107 を公開します',
    'zh-CN': 'docker compose 读取 compose.yaml，在网络 lab_default 中启动 api 和 web；web 通过名称访问 api，并发布 127.0.0.1:18107',
    'fil': 'Binabasa ng docker compose ang compose.yaml at sinisimulan ang api at web sa network na lab_default; naaabot ng web ang api gamit ang pangalan at nagpa-publish ito ng 127.0.0.1:18107',
    'es': 'docker compose lee compose.yaml e inicia api y web en la red lab_default; web llega a api por su nombre y publica 127.0.0.1:18107',
    'vi': 'docker compose đọc compose.yaml và chạy api cùng web trong mạng lab_default; web gọi api bằng tên và công bố 127.0.0.1:18107',
}

WORDS = {
    'en': {
        'commands': 'up · ps · exec · down',
        'starts': 'up -d',
        'file_note': 'name: lab · 2 services',
        'desk': 'ports, open page',
    },
    'ko': {
        'commands': 'up · ps · exec · down',
        'starts': 'up -d',
        'file_note': 'name: lab · 서비스 2개',
        'desk': '포트 확인, 페이지 열기',
    },
    'ja': {
        'commands': 'up · ps · exec · down',
        'starts': 'up -d',
        'file_note': 'name: lab · サービス 2 つ',
        'desk': 'ポート確認、ページを開く',
    },
    'zh-CN': {
        'commands': 'up · ps · exec · down',
        'starts': 'up -d',
        'file_note': 'name: lab · 2 个服务',
        'desk': '查看端口、打开页面',
    },
    'fil': {
        'commands': 'up · ps · exec · down',
        'starts': 'up -d',
        'file_note': 'name: lab · 2 service',
        'desk': 'mga port, buksan ang page',
    },
    'es': {
        'commands': 'up · ps · exec · down',
        'starts': 'up -d',
        'file_note': 'name: lab · 2 servicios',
        'desk': 'puertos, abrir página',
    },
    'vi': {
        'commands': 'up · ps · exec · down',
        'starts': 'up -d',
        'file_note': 'name: lab · 2 dịch vụ',
        'desk': 'cổng, mở trang',
    },
}


def draw(p, w):
    frame(p, w, 350)
    p.box(40, 80, 210, 56, w["terminal"], w["commands"], mono_name=False)
    p.box(40, 152, 210, 56, w["desktop"], w["desk"], mono_name=False)
    p.box(40, 250, 210, 42, w["browser"], mono_name=False)
    p.box(600, 76, 240, 56, "compose.yaml", w["file_note"])
    p.network(330, 160, 590, 150, "lab_default")
    p.box(360, 200, 260, 80, "web", "httpd :8080", port="127.0.0.1:18107")
    p.box(720, 200, 180, 72, "api", "httpd :8080 · " + w["no_port"])
    p.arrow(720, 132, 720, 156, w["starts"], dx=10, dy=4)
    p.arrow(620, 236, 716, 236, w["by_name"], dx=-40, dy=-10, color="accent")
    p.arrow(250, 271, 356, 266, None, color="accent")
