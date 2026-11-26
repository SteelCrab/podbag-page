"""The architecture of the docker-compose guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 350

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'docker compose reads compose.yaml and starts api and web on the network lab_default; web reaches api by name and publishes 127.0.0.1:18107',
    'ko': 'docker compose가 compose.yaml을 읽고 lab_default 네트워크에 api와 web을 시작합니다. web은 이름으로 api에 접속하고 127.0.0.1:18107을 공개합니다',
}

WORDS = {
    "en": {"commands": "up · ps · exec · down", "starts": "up -d", "file_note": "name: lab · 2 services", "desk": "ports, open page"},
    "ko": {"commands": "up · ps · exec · down", "starts": "up -d", "file_note": "name: lab · 서비스 2개", "desk": "포트 확인, 페이지 열기"},
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
