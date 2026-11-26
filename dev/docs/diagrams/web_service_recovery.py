"""The architecture of the web-service-recovery guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The first lab-web exits because SITE_TITLE is missing and its log says so; the second lab-web gets the setting and serves 127.0.0.1:18082',
    'ko': '첫 번째 lab-web은 SITE_TITLE이 없어 종료되고 로그가 이유를 알려 줍니다. 설정을 받은 두 번째 lab-web이 127.0.0.1:18082로 페이지를 보여 줍니다',
}


def draw(p, w):
    frame(p, w, 330)
    p.box(40, 80, 210, 56, w["terminal"], "podbag run · logs · rm", mono_name=False)
    p.box(40, 152, 210, 56, w["desktop"], w["ports"], mono_name=False)
    p.box(40, 232, 210, 42, w["browser"], mono_name=False)
    p.box(360, 92, 300, 72, "lab-web", "SITE_TITLE is required", color="bad",
          badge=(w["exited"], "bad"))
    p.box(360, 212, 300, 72, "lab-web", "-e SITE_TITLE=…", color="good",
          badge=(w["running"], "good"), port="127.0.0.1:18082")
    p.arrow(356, 120, 254, 110, w["logs"], dx=-8, dy=-8, color="bad", anchor="middle")
    p.arrow(250, 253, 356, 250, None, color="accent")
