"""The architecture of the container-lifecycle guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The terminal takes the container app through create, start, stop, restart, kill and rm, and podbag ps -a shows each status',
    'ko': '터미널이 app 컨테이너를 create, start, stop, restart, kill, rm 순서로 다루고, podbag ps -a가 각 상태를 보여 줍니다',
}

WORDS = {
    "en": {"removed": "removed", "gone": "not in ps -a",
           "ps_note": "podbag ps -a shows the STATUS of app after each step"},
    "ko": {"removed": "삭제됨", "gone": "ps -a에 없음",
           "ps_note": "podbag ps -a가 단계마다 app의 STATUS를 보여 줍니다"},
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 96, 210, 56, w["terminal"], "create · start · stop", mono_name=False)
    p.box(40, 206, 210, 56, w["terminal"], "restart · kill · rm · ps -a", mono_name=False)
    # The first row goes right, the second comes back.
    p.box(330, 96, 160, 60, "created", "Created")
    p.box(540, 96, 160, 60, "running", "Up …", color="good")
    p.box(750, 96, 160, 60, "exited", "Exited (0)")
    p.box(750, 206, 160, 60, "running", "Up …", color="good")
    p.box(540, 206, 160, 60, "exited", "Exited (137)", color="bad")
    p.box(330, 206, 160, 60, w["removed"], w["gone"], mono_name=False)
    p.arrow(250, 124, 326, 124)
    p.arrow(490, 126, 536, 126, "start", dx=0, dy=-10, anchor="middle", mono=True)
    p.arrow(700, 126, 746, 126, "stop", dx=0, dy=-10, anchor="middle", mono=True)
    p.arrow(830, 156, 830, 202, "restart", dx=8, dy=4, mono=True)
    p.arrow(750, 236, 704, 236, "kill", dx=0, dy=-10, anchor="middle", mono=True, color="bad")
    p.arrow(540, 236, 494, 236, "rm", dx=0, dy=-10, anchor="middle", mono=True)
    p.text(330, 296, w["ps_note"], 11.5)
