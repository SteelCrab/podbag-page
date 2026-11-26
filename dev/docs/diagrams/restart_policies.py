"""The architecture of the restart-policies guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 310

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'podbag __restart starts job again three times after it fails, and starts app again after each exit until podbag stop',
    'ko': 'podbag __restart가 실패한 job을 세 번 다시 시작하고, app은 podbag stop 전까지 끝날 때마다 다시 시작합니다',
    'ja': 'podbag __restart は、失敗した job を 3 回再起動します。app は終了するたびに再起動し、podbag stop で止まります',
    'zh-CN': 'podbag __restart 在 job 失败后重新启动它三次，并在 app 每次退出后重新启动它，直到 podbag stop',
    'fil': 'Sinisimulan ulit ng podbag __restart ang job nang tatlong beses pagkatapos itong mabigo, at sinisimulan ulit ang app pagkatapos ng bawat paglabas hanggang sa podbag stop',
    'es': 'podbag __restart vuelve a iniciar job tres veces después de que falla, e inicia app de nuevo después de cada salida hasta podbag stop',
    'vi': 'podbag __restart chạy lại job ba lần sau khi nó lỗi, và chạy lại app sau mỗi lần thoát cho đến khi có podbag stop',
}

WORDS = {
    'en': {
        'three': '3 times',
        'until_stop': 'until stop',
        'stopped': 'stopped',
        'starts_again': 'starts it again',
    },
    'ko': {
        'three': '3번',
        'until_stop': 'stop 전까지',
        'stopped': '중지됨',
        'starts_again': '다시 시작',
    },
    'ja': {
        'three': '3 回',
        'until_stop': 'stop まで',
        'stopped': '停止',
        'starts_again': '再起動',
    },
    'zh-CN': {
        'three': '3 次',
        'until_stop': '直到 stop',
        'stopped': '已停止',
        'starts_again': '重新启动',
    },
    'fil': {
        'three': '3 beses',
        'until_stop': 'hanggang stop',
        'stopped': 'nakahinto',
        'starts_again': 'sinisimulan ulit',
    },
    'es': {
        'three': '3 veces',
        'until_stop': 'hasta stop',
        'stopped': 'detenido',
        'starts_again': 'lo inicia de nuevo',
    },
    'vi': {
        'three': '3 lần',
        'until_stop': 'đến khi stop',
        'stopped': 'đã dừng',
        'starts_again': 'chạy lại',
    },
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
