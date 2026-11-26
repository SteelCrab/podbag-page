"""The architecture of the health-checks guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'podbag __health runs wget in the web server every 2 seconds; ps and inspect show it healthy, and the page is on 127.0.0.1:18100',
    'ko': 'podbag __health가 2초마다 web 서버 안에서 wget을 실행합니다. ps와 inspect가 healthy를 보여 주고, 페이지는 127.0.0.1:18100에 있습니다',
    'ja': 'podbag __health が 2 秒ごとに Web サーバーの中で wget を実行します。ps と inspect が healthy と表示し、ページは 127.0.0.1:18100 にあります',
    'zh-CN': 'podbag __health 每 2 秒在 Web 服务器中运行一次 wget；ps 和 inspect 显示它是健康的，页面位于 127.0.0.1:18100',
    'fil': 'Pinapatakbo ng podbag __health ang wget sa web server tuwing 2 segundo; ipinapakita ng ps at inspect na healthy ito, at nasa 127.0.0.1:18100 ang page',
    'es': 'podbag __health ejecuta wget en el servidor web cada 2 segundos; ps e inspect lo muestran en buen estado, y la página está en 127.0.0.1:18100',
    'vi': 'podbag __health chạy wget trong máy chủ web mỗi 2 giây; ps và inspect cho thấy nó healthy, và trang web có tại 127.0.0.1:18100',
}

WORDS = {
    'en': {
        'ports': 'ports, page',
        'healthy': 'healthy',
        'every': 'wget · every 2 s',
        'checks': 'checks',
        'states': 'ps · inspect: starting → healthy',
    },
    'ko': {
        'ports': '포트 확인, 페이지 열기',
        'healthy': 'healthy',
        'every': 'wget · 2초마다',
        'checks': '검사',
        'states': 'ps · inspect: starting → healthy',
    },
    'ja': {
        'ports': 'ポート確認、ページを開く',
        'healthy': 'healthy',
        'every': 'wget · 2 秒ごと',
        'checks': 'チェック',
        'states': 'ps · inspect: starting → healthy',
    },
    'zh-CN': {
        'ports': '端口、页面',
        'healthy': '健康',
        'every': 'wget · 每 2 秒',
        'checks': '检查',
        'states': 'ps · inspect：starting → healthy',
    },
    'fil': {
        'ports': 'mga port, page',
        'healthy': 'healthy',
        'every': 'wget · tuwing 2 s',
        'checks': 'sumusuri',
        'states': 'ps · inspect: starting → healthy',
    },
    'es': {
        'ports': 'puertos, página',
        'healthy': 'healthy',
        'every': 'wget · cada 2 s',
        'checks': 'comprueba',
        'states': 'ps · inspect: starting → healthy',
    },
    'vi': {
        'ports': 'cổng, trang',
        'healthy': 'healthy',
        'every': 'wget · mỗi 2 giây',
        'checks': 'kiểm tra',
        'states': 'ps · inspect: starting → healthy',
    },
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 80, 210, 56, w["terminal"], "podbag run · ps · inspect", mono_name=False)
    p.box(40, 152, 210, 56, w["desktop"], w["ports"], mono_name=False)
    p.box(40, 240, 210, 42, w["browser"], mono_name=False)
    p.box(330, 140, 300, 84, "web", "httpd :8080", color="good",
          badge=(w["healthy"], "good"), port="127.0.0.1:18100")
    p.box(730, 146, 180, 72, "podbag __health", w["every"])
    p.arrow(726, 182, 634, 182, w["checks"], dx=0, dy=-8, anchor="middle")
    p.text(330, 252, w["states"], 11.5, mono=True)
    p.arrow(250, 261, 326, 212, None, color="accent")
