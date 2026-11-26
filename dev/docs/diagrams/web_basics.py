"""The architecture of the web-basics guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 300

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The browser opens 127.0.0.1:18080, which leads to port 8080 of the web server lab-web in the practice session',
    'ko': '브라우저가 127.0.0.1:18080을 열면 실습 환경에 있는 웹 서버 lab-web의 8080 포트로 연결됩니다',
}


def draw(p, w):
    frame(p, w, 300)
    p.box(40, 80, 210, 56, w["terminal"], "podbag run · rm", mono_name=False)
    p.box(40, 152, 210, 56, w["desktop"], w["ports"], mono_name=False)
    p.box(40, 224, 210, 42, w["browser"], mono_name=False)
    p.box(600, 130, 300, 72, "lab-web", "httpd :8080", port="127.0.0.1:18080")
    p.arrow(250, 245, 596, 186, None, color="accent")
    p.arrow(250, 108, 596, 150, None, color="podbag")
    p.arrow(250, 180, 596, 166, None, color="podbag")
