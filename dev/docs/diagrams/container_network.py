"""The architecture of the container-network guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 350

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'On the network lab-net, a one-time container and the web server reach api by name; only web publishes a port, 127.0.0.1:18083',
    'ko': 'lab-net 네트워크에서 일회용 컨테이너와 web 서버가 이름으로 api에 접속합니다. 포트는 web만 127.0.0.1:18083으로 공개합니다',
}


def draw(p, w):
    frame(p, w, 350)
    p.box(40, 80, 210, 56, w["terminal"], "podbag network · run · rm", mono_name=False)
    p.box(40, 152, 210, 56, w["desktop"], w["ports"], mono_name=False)
    p.box(40, 240, 210, 42, w["browser"], mono_name=False)
    p.network(330, 76, 590, 236, "lab-net")
    p.box(720, 112, 180, 72, "api", "httpd :8080 · " + w["no_port"])
    p.box(360, 112, 220, 64, "wget (--rm)", "http://api:8080/")
    p.box(360, 216, 260, 72, "web", "httpd :8080", port="127.0.0.1:18083")
    p.arrow(580, 144, 716, 144, w["by_name"], dx=-40, dy=-10, color="accent")
    p.arrow(620, 246, 716, 176, w["copies"], at=0.5, dx=4, dy=24, color="accent")
    p.arrow(250, 261, 356, 256, None, color="accent")
