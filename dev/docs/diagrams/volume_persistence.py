"""The architecture of the volume-persistence guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 320

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'app-a writes note.txt into the volume training-data and app-b reads it; the volume stays after both containers are removed',
    'ko': 'app-a가 training-data 볼륨에 note.txt를 쓰고 app-b가 읽습니다. 두 컨테이너를 지워도 볼륨은 남습니다',
}


def draw(p, w):
    frame(p, w, 320)
    p.box(40, 100, 210, 60, w["terminal"], "podbag run · rm", mono_name=False)
    p.box(40, 190, 210, 60, w["desktop"], w["inspect"], mono_name=False)
    p.box(340, 90, 230, 64, "app-a", "/data/note.txt")
    p.box(340, 200, 230, 64, "app-b", "/data:ro")
    p.volume(700, 125, 190, 90, "training-data", w["stays"])
    p.arrow(570, 122, 696, 158, w["writes"], dx=-10, dy=-12)
    p.arrow(696, 186, 570, 232, w["reads"], dx=0, dy=22)
