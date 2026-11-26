"""The architecture of the system-checks guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 320

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'podbag check reads the system, podbag check-image reads the programs in busybox, and podbag system df and verify read the stored files',
    'ko': 'podbag check는 시스템을, podbag check-image는 busybox의 프로그램을, podbag system df와 verify는 저장된 파일을 확인합니다',
}

WORDS = {
    "en": {"system": "System", "system_note": "kernel · cgroup v2 · keeper",
           "programs": "programs and libraries", "store": "Stored files",
           "store_note": "sizes and hashes"},
    "ko": {"system": "시스템", "system_note": "커널 · cgroup v2 · keeper",
           "programs": "프로그램과 라이브러리", "store": "저장된 파일",
           "store_note": "크기와 해시"},
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 84, 210, 204, w["terminal"], "podbag check · system", mono_name=False)
    p.box(470, 84, 300, 56, w["system"], w["system_note"], mono_name=False)
    p.box(470, 158, 300, 56, "busybox:1.37.0", w["programs"])
    p.box(470, 232, 300, 56, w["store"], w["store_note"], mono_name=False)
    p.arrow(250, 112, 466, 112, "check", dx=0, dy=-8, anchor="middle", mono=True)
    p.arrow(250, 186, 466, 186, "check-image", dx=0, dy=-8, anchor="middle", mono=True)
    p.arrow(250, 260, 466, 260, "system df · verify", dx=0, dy=-8, anchor="middle", mono=True)
