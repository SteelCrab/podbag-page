"""The architecture of the network-connect guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 400

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The server api is on front-net with the alias backend and on back-net with the alias store; one-time containers on each network call it by those names',
    'ko': 'api 서버는 front-net에서 backend라는 별칭을, back-net에서 store라는 별칭을 가집니다. 각 네트워크의 일회용 컨테이너가 이 이름으로 api를 호출합니다',
}

WORDS = {
    "en": {"first": "first network", "connected": "connected while stopped"},
    "ko": {"first": "첫 번째 네트워크", "connected": "중지된 상태에서 연결"},
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 80, 210, 56, w["terminal"], "network create · run · rm", mono_name=False)
    p.box(40, 188, 210, 56, w["terminal"], "network connect · disconnect", mono_name=False)
    p.network(330, 76, 590, 130, "front-net")
    p.text(430, 98, w["first"], 11.5)
    p.network(330, 226, 590, 130, "back-net")
    p.text(424, 248, w["connected"], 11.5)
    p.box(360, 118, 230, 64, "wget (--rm)", "http://backend:8080/")
    p.box(360, 268, 230, 64, "wget (--rm)", "http://store:8080/")
    p.box(720, 112, 180, 220, "api", "httpd :8080")
    p.arrow(590, 150, 716, 150, "backend", dx=-30, dy=-10, color="accent", mono=True)
    p.arrow(590, 300, 716, 300, "store", dx=-24, dy=-10, color="accent", mono=True)
    p.arrow(250, 216, 716, 216)
