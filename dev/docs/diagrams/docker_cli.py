"""The architecture of the docker-cli guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The docker command talks to the Docker API that podbag serves; it runs the container web, which publishes 127.0.0.1:18106',
    'ko': 'docker 명령은 podbag이 제공하는 Docker API에 연결합니다. 이 API로 web 컨테이너를 실행하고 127.0.0.1:18106을 공개합니다',
    'ja': 'docker コマンドが podbag の提供する Docker API と通信し、コンテナ web を実行します。web は 127.0.0.1:18106 を公開します',
    'zh-CN': 'docker 命令与 podbag 提供的 Docker API 通信；它运行容器 web，该容器发布 127.0.0.1:18106',
    'fil': 'Nakikipag-usap ang docker command sa Docker API na inihahain ng podbag; pinapatakbo nito ang container na web, na nagpa-publish ng 127.0.0.1:18106',
    'es': 'El comando docker habla con la API de Docker que sirve podbag; ejecuta el contenedor web, que publica 127.0.0.1:18106',
    'vi': 'Lệnh docker giao tiếp với Docker API do podbag phục vụ; nó chạy container web, container này công bố 127.0.0.1:18106',
}

WORDS = {
    'en': {
        'api': 'Docker API',
        'api_note': 'served by podbag',
        'sends': 'docker …',
        'desk': 'ports, open page',
    },
    'ko': {
        'api': 'Docker API',
        'api_note': 'podbag이 제공',
        'sends': 'docker …',
        'desk': '포트 확인, 페이지 열기',
    },
    'ja': {
        'api': 'Docker API',
        'api_note': 'podbag が提供',
        'sends': 'docker …',
        'desk': 'ポート確認、ページを開く',
    },
    'zh-CN': {
        'api': 'Docker API',
        'api_note': '由 podbag 提供',
        'sends': 'docker …',
        'desk': '查看端口、打开页面',
    },
    'fil': {
        'api': 'Docker API',
        'api_note': 'inihahain ng podbag',
        'sends': 'docker …',
        'desk': 'mga port, buksan ang page',
    },
    'es': {
        'api': 'API de Docker',
        'api_note': 'servida por podbag',
        'sends': 'docker …',
        'desk': 'puertos, abrir página',
    },
    'vi': {
        'api': 'Docker API',
        'api_note': 'do podbag phục vụ',
        'sends': 'docker …',
        'desk': 'cổng, mở trang',
    },
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
