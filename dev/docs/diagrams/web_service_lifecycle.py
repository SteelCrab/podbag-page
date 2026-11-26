"""The architecture of the web-service-lifecycle guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'site-v1 writes the page into the volume site-data and is replaced by site-v2, which serves the same page on 127.0.0.1:18081',
    'ko': 'site-v1이 site-data 볼륨에 페이지를 쓰고, 같은 페이지를 127.0.0.1:18081로 보여 주는 site-v2로 교체됩니다',
}


def draw(p, w):
    frame(p, w, 330)
    p.box(40, 80, 210, 56, w["terminal"], "podbag run · rm", mono_name=False)
    p.box(40, 152, 210, 56, w["desktop"], w["ports"], mono_name=False)
    p.box(40, 232, 210, 42, w["browser"], mono_name=False)
    p.box(340, 96, 230, 64, "site-v1", "/site · " + w["writes"], port="127.0.0.1:18081")
    p.box(340, 216, 230, 64, "site-v2", "/site:ro", port="127.0.0.1:18081")
    p.arrow(455, 160, 455, 212, w["replaces"], dx=10, dy=4)
    p.volume(720, 140, 180, 90, "site-data")
    p.arrow(570, 128, 716, 168, None, color="podbag")
    p.arrow(716, 200, 570, 248, None, color="podbag")
    p.arrow(250, 253, 336, 250, None, color="accent")
