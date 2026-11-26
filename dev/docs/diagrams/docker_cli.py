"""The architecture of the docker-cli guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The docker command talks to the Docker API that podbag serves; it runs the container web, which publishes 127.0.0.1:18106',
    'ko': 'docker 명령은 podbag이 제공하는 Docker API에 연결합니다. 이 API로 web 컨테이너를 실행하고 127.0.0.1:18106을 공개합니다',
}

WORDS = {
    "en": {"api": "Docker API", "api_note": "served by podbag", "sends": "docker …", "desk": "ports, open page"},
    "ko": {"api": "Docker API", "api_note": "podbag이 제공", "sends": "docker …", "desk": "포트 확인, 페이지 열기"},
}


def draw(p, w):
    frame(p, w, 330)
    p.box(40, 80, 210, 56, w["terminal"], "docker · podbag ps", mono_name=False)
    p.box(40, 152, 210, 56, w["desktop"], w["desk"], mono_name=False)
    p.box(40, 240, 210, 42, w["browser"], mono_name=False)
    p.box(380, 80, 240, 64, w["api"], w["api_note"], mono_name=False)
    p.box(600, 200, 310, 80, "web", "httpd :8080", port="127.0.0.1:18106")
    p.arrow(250, 108, 376, 112, w["sends"], dx=-5, dy=-10)
    p.arrow(620, 120, 720, 196, w["runs"], dx=8, dy=-6)
    p.arrow(250, 261, 596, 248, None, color="accent")
