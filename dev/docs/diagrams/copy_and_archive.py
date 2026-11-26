"""The architecture of the copy-and-archive guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 350

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'docker cp copies note.txt into the container app and reply.txt out of it; podbag save and load move the busybox image through busybox.tar',
    'ko': 'docker cp가 note.txt를 app 컨테이너에 넣고 reply.txt를 꺼냅니다. podbag save와 load는 busybox 이미지를 busybox.tar로 옮깁니다',
}

WORDS = {
    "en": {"folder": "practice folder", "cp": "docker cp", "save_load": "save / load"},
    "ko": {"folder": "실습 폴더", "cp": "docker cp", "save_load": "save / load"},
}


def draw(p, w):
    frame(p, w, 350)
    p.box(40, 110, 210, 60, w["terminal"], "podbag · docker cp", mono_name=False)
    p.box(330, 86, 200, 52, "note.txt", w["folder"])
    p.box(330, 158, 200, 52, "reply.txt", w["folder"])
    p.box(680, 96, 230, 96, "app", "/tmp/note.txt · /reply.txt")
    p.box(330, 256, 200, 56, "busybox.tar", w["folder"])
    p.box(680, 256, 230, 56, "busybox:1.37.0", w["image"])
    p.arrow(530, 112, 676, 124, w["cp"], dx=-30, dy=-10, mono=True)
    p.arrow(676, 166, 530, 184, w["cp"], dx=-30, dy=24, mono=True)
    p.arrow(530, 284, 676, 284, w["save_load"], dx=-32, dy=-8, both=True)
    p.arrow(795, 252, 795, 196, w["runs"], dx=10, dy=4)
