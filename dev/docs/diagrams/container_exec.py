"""The architecture of the container-exec guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The terminal runs the container app with the variable GREETING=hello and then runs commands inside it with podbag exec',
    'ko': '터미널이 GREETING=hello 변수를 넣어 app 컨테이너를 실행하고, podbag exec로 그 안에서 명령을 실행합니다',
    'ja': 'ターミナルが変数 GREETING=hello を付けてコンテナ app を実行し、podbag exec でその中のコマンドを実行します',
    'zh-CN': '终端运行带有变量 GREETING=hello 的容器 app，然后用 podbag exec 在其中运行命令',
    'fil': 'Pinapatakbo ng terminal ang container na app na may variable na GREETING=hello, at saka nagpapatakbo ng mga command sa loob nito gamit ang podbag exec',
    'es': 'La terminal ejecuta el contenedor app con la variable GREETING=hello y luego ejecuta comandos dentro de él con podbag exec',
    'vi': 'Terminal chạy container app với biến GREETING=hello, rồi chạy các lệnh bên trong nó bằng podbag exec',
}

WORDS = {
    'en': {
        'exec_note': 'a new process in the same container',
        'lists': 'lists',
        'writes_reads': 'writes, reads',
    },
    'ko': {
        'exec_note': '같은 컨테이너의 새 프로세스',
        'lists': '목록',
        'writes_reads': '쓰기, 읽기',
    },
    'ja': {
        'exec_note': '同じコンテナの新しいプロセス',
        'lists': '一覧',
        'writes_reads': '書き込み、読み取り',
    },
    'zh-CN': {
        'exec_note': '同一容器中的新进程',
        'lists': '列出',
        'writes_reads': '写入、读取',
    },
    'fil': {
        'exec_note': 'bagong proseso sa parehong container',
        'lists': 'naglilista',
        'writes_reads': 'nagsusulat, nagbabasa',
    },
    'es': {
        'exec_note': 'un proceso nuevo en el mismo contenedor',
        'lists': 'lista',
        'writes_reads': 'escribe, lee',
    },
    'vi': {
        'exec_note': 'tiến trình mới trong cùng container',
        'lists': 'liệt kê',
        'writes_reads': 'ghi, đọc',
    },
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
