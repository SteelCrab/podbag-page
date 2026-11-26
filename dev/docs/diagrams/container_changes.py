"""The architecture of the container-changes guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The container app writes /hello.txt; podbag commit turns its changes into the image app-snapshot:1, and podbag export writes its files to app.tar',
    'ko': 'app 컨테이너가 /hello.txt를 씁니다. podbag commit은 변경 내용을 app-snapshot:1 이미지로 만들고, podbag export는 파일을 app.tar로 씁니다',
}

WORDS = {
    "en": {"commit": "commit", "export": "export", "changed": "A /hello.txt · exited (0)",
           "tar": "all files of app"},
    "ko": {"commit": "commit", "export": "export", "changed": "A /hello.txt · 종료됨 (0)",
           "tar": "app의 모든 파일"},
}


def draw(p, w):
    frame(p, w, 330)
    p.box(40, 110, 210, 60, w["terminal"], "podbag diff · commit · export", mono_name=False)
    p.box(330, 90, 240, 64, "app", w["changed"])
    p.box(680, 90, 230, 64, "app-snapshot:1", w["image"])
    p.box(330, 220, 240, 64, "app.tar", w["tar"])
    p.box(680, 220, 230, 64, "run --rm", "cat /hello.txt")
    p.arrow(250, 140, 326, 122, None, color="podbag")
    p.arrow(570, 122, 676, 122, w["commit"], dx=-24, dy=-8)
    p.arrow(450, 154, 450, 216, w["export"], dx=10, dy=4)
    p.arrow(795, 154, 795, 216, w["runs"], dx=10, dy=4)
