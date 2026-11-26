"""The architecture of the web-service-recovery guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The first lab-web exits because SITE_TITLE is missing and its log says so; the second lab-web gets the setting and serves 127.0.0.1:18082',
    'ko': '첫 번째 lab-web은 SITE_TITLE이 없어 종료되고 로그가 이유를 알려 줍니다. 설정을 받은 두 번째 lab-web이 127.0.0.1:18082로 페이지를 보여 줍니다',
    'ja': '1 つ目の lab-web は SITE_TITLE がないので終了し、ログにその理由が出ます。2 つ目の lab-web は設定を受け取り、127.0.0.1:18082 で配信します',
    'zh-CN': '第一个 lab-web 因缺少 SITE_TITLE 而退出，日志中写明了原因；第二个 lab-web 获得该设置，并在 127.0.0.1:18082 上提供服务',
    'fil': 'Lumalabas ang unang lab-web dahil walang SITE_TITLE, at sinasabi iyon ng log nito; nakukuha ng pangalawang lab-web ang setting at naghahain ito sa 127.0.0.1:18082',
    'es': 'El primer lab-web termina porque falta SITE_TITLE, y su registro lo indica; el segundo lab-web recibe el ajuste y sirve 127.0.0.1:18082',
    'vi': 'lab-web đầu tiên thoát vì thiếu SITE_TITLE và nhật ký của nó báo điều đó; lab-web thứ hai có cài đặt này và phục vụ 127.0.0.1:18082',
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
