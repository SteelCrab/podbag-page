"""The architecture of the pause-and-rename guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The terminal runs the web server web with the port 127.0.0.1:18090, pauses and unpauses it and renames it to site; the browser opens the page',
    'ko': '터미널이 127.0.0.1:18090 포트로 web 서버를 실행하고, 일시 정지와 재개를 한 뒤 이름을 site로 바꿉니다. 브라우저가 페이지를 엽니다',
    'ja': 'ターミナルがポート 127.0.0.1:18090 で Web サーバー web を実行し、一時停止と再開をしてから名前を site に変更します。ブラウザーがそのページを開きます',
    'zh-CN': '终端运行 Web 服务器 web 并发布端口 127.0.0.1:18090，暂停后再恢复，并将它重命名为 site；浏览器打开页面',
    'fil': 'Pinapatakbo ng terminal ang web server na web na may port na 127.0.0.1:18090, ipina-pause at ina-unpause ito, at pinapalitan ang pangalan nito ng site; binubuksan ng browser ang page',
    'es': 'La terminal ejecuta el servidor web web con el puerto 127.0.0.1:18090, lo pausa, lo reanuda y le cambia el nombre a site; el navegador abre la página',
    'vi': 'Terminal chạy máy chủ web web với cổng 127.0.0.1:18090, tạm dừng rồi cho chạy tiếp, sau đó đổi tên thành site; trình duyệt mở trang',
}

WORDS = {
    'en': {
        'paused': 'paused: frozen',
        'open_page': 'view ports, open page',
        'new_name': 'new name',
    },
    'ko': {
        'paused': '일시 정지: 멈춤',
        'open_page': '포트 보기, 페이지 열기',
        'new_name': '새 이름',
    },
    'ja': {
        'paused': '一時停止: 凍結',
        'open_page': 'ポートを表示、ページを開く',
        'new_name': '新しい名前',
    },
    'zh-CN': {
        'paused': '已暂停：冻结',
        'open_page': '查看端口、打开页面',
        'new_name': '新名称',
    },
    'fil': {
        'paused': 'naka-pause: naka-freeze',
        'open_page': 'tingnan ang mga port, buksan ang page',
        'new_name': 'bagong pangalan',
    },
    'es': {
        'paused': 'en pausa: congelado',
        'open_page': 'ver puertos, abrir página',
        'new_name': 'nombre nuevo',
    },
    'vi': {
        'paused': 'paused: đóng băng',
        'open_page': 'xem cổng, mở trang',
        'new_name': 'tên mới',
    },
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 80, 210, 56, w["terminal"], "run · pause · unpause · rename", mono_name=False)
    p.box(40, 152, 210, 56, w["desktop"], w["open_page"], mono_name=False)
    p.box(40, 240, 210, 42, w["browser"], mono_name=False)
    port = "127.0.0.1:18090"
    p.box(340, 86, 230, 72, "web", w["running"], color="good", port=port)
    p.box(680, 86, 230, 72, "web", w["paused"], color="podbag")
    p.box(680, 206, 230, 72, "web", w["running"], color="good", port=port)
    p.box(340, 206, 230, 72, "site", w["new_name"], color="good", port=port)
    p.arrow(570, 122, 676, 122, "pause", dx=0, dy=-10, anchor="middle", mono=True)
    p.arrow(795, 158, 795, 202, "unpause", dx=8, dy=4, mono=True)
    p.arrow(680, 242, 574, 242, "rename", dx=0, dy=-10, anchor="middle", mono=True)
    p.arrow(250, 261, 336, 261, None, color="accent")
