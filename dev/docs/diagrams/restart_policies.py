"""The architecture of the restart-policies guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 310

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'podbag __restart starts job again three times after it fails, and starts app again after each exit until podbag stop',
    'ko': 'podbag __restart가 실패한 job을 세 번 다시 시작하고, app은 podbag stop 전까지 끝날 때마다 다시 시작합니다',
}

WORDS = {
    "en": {"three": "3 times", "until_stop": "until stop", "stopped": "stopped",
           "starts_again": "starts it again"},
    "ko": {"three": "3번", "until_stop": "stop 전까지", "stopped": "중지됨",
           "starts_again": "다시 시작"},
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 100, 210, 150, w["terminal"], "podbag run · stop · start", mono_name=False)
    p.box(340, 90, 300, 72, "job", "--restart on-failure:3", color="bad",
          badge=(w["exited"], "bad"))
    p.box(340, 200, 300, 72, "app", "--restart always", badge=(w["stopped"], "ink2"))
    p.box(750, 145, 180, 72, "podbag __restart", w["starts_again"])
    p.arrow(746, 170, 644, 132, w["three"], at=0.45, dx=0, dy=-10, anchor="middle")
    p.arrow(746, 192, 644, 230, w["until_stop"], at=0.45, dx=0, dy=24, anchor="middle")
    p.arrow(250, 236, 336, 236, None, color="accent")
