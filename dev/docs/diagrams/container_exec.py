"""The architecture of the container-exec guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The terminal runs the container app with the variable GREETING=hello and then runs commands inside it with podbag exec',
    'ko': '터미널이 GREETING=hello 변수를 넣어 app 컨테이너를 실행하고, podbag exec로 그 안에서 명령을 실행합니다',
}

WORDS = {
    "en": {"exec_note": "a new process in the same container", "lists": "lists",
           "writes_reads": "writes, reads"},
    "ko": {"exec_note": "같은 컨테이너의 새 프로세스", "lists": "목록",
           "writes_reads": "쓰기, 읽기"},
}


def draw(p, w):
    frame(p, w, HEIGHT)
    t = p.t
    p.box(40, 96, 210, 56, w["terminal"], "podbag run -d · rm", mono_name=False)
    p.box(40, 220, 210, 56, w["terminal"], "podbag exec app …", mono_name=False)
    # The container app, with what lives inside it.
    p.o.append(f'<rect x="340" y="80" width="580" height="212" rx="10" fill="{t["panel"]}" '
               f'stroke="{t["line"]}" stroke-width="1.4"/>')
    p.text(356, 104, "app", 14, "ink", 600, mono=True)
    p.text(392, 104, "busybox · sleep 3600", 11.5)
    p.box(360, 120, 170, 60, "env", "GREETING=hello")
    p.box(550, 120, 170, 60, "/etc", "hosts, hostname …")
    p.box(740, 120, 160, 60, "/tmp", "note.txt")
    p.box(360, 220, 540, 56, "printenv · ls · sh -c · cat", w["exec_note"])
    p.arrow(250, 124, 338, 124, w["runs"], dx=-22, dy=-8)
    p.arrow(250, 248, 356, 248, "exec", dx=-22, dy=-8, color="accent", mono=True)
    p.arrow(445, 220, 445, 182, w["reads"], dx=8, dy=4, color="accent")
    p.arrow(635, 220, 635, 182, w["lists"], dx=8, dy=4, color="accent")
    p.arrow(820, 220, 820, 182, w["writes_reads"], dx=8, dy=4, color="accent")
