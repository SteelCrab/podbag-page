"""The architecture of the health-checks guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'podbag __health runs wget in the web server every 2 seconds; ps and inspect show it healthy, and the page is on 127.0.0.1:18100',
    'ko': 'podbag __health가 2초마다 web 서버 안에서 wget을 실행합니다. ps와 inspect가 healthy를 보여 주고, 페이지는 127.0.0.1:18100에 있습니다',
}

WORDS = {
    "en": {"ports": "ports, page", "healthy": "healthy", "every": "wget · every 2 s",
           "checks": "checks", "states": "ps · inspect: starting → healthy"},
    "ko": {"ports": "포트 확인, 페이지 열기", "healthy": "healthy", "every": "wget · 2초마다",
           "checks": "검사", "states": "ps · inspect: starting → healthy"},
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 80, 210, 56, w["terminal"], "podbag run · ps · inspect", mono_name=False)
    p.box(40, 152, 210, 56, w["desktop"], w["ports"], mono_name=False)
    p.box(40, 240, 210, 42, w["browser"], mono_name=False)
    p.box(330, 140, 300, 84, "web", "httpd :8080", color="good",
          badge=(w["healthy"], "good"), port="127.0.0.1:18100")
    p.box(730, 146, 180, 72, "podbag __health", w["every"])
    p.arrow(726, 182, 634, 182, w["checks"], dx=0, dy=-8, anchor="middle")
    p.text(330, 252, w["states"], 11.5, mono=True)
    p.arrow(250, 261, 326, 212, None, color="accent")
