"""The architecture of the container-basics guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 300

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The terminal runs the container hello-web from the busybox image in the practice session; Podbag Desktop stops it',
    'ko': '터미널이 실습 환경에서 busybox 이미지로 hello-web 컨테이너를 실행하고, Podbag Desktop이 이 컨테이너를 중지합니다',
    'ja': 'ターミナルが実習環境で busybox イメージから hello-web コンテナを実行し、Podbag Desktop がそれを停止します',
    'zh-CN': '终端在练习环境中用 busybox 镜像运行容器 hello-web，Podbag Desktop 停止该容器',
    'fil': 'Pinapatakbo ng terminal ang container na hello-web mula sa image na busybox sa practice session; inihihinto ito ng Podbag Desktop',
    'es': 'La terminal ejecuta el contenedor hello-web desde la imagen busybox en la sesión de práctica; Podbag Desktop lo detiene',
    'vi': 'Terminal chạy container hello-web từ image busybox trong phiên thực hành; Podbag Desktop dừng container này',
}


def draw(p, w):
    frame(p, w, 300)
    p.box(40, 90, 210, 60, w["terminal"], "podbag run …", mono_name=False)
    p.box(40, 180, 210, 60, w["desktop"], w["stop"], mono_name=False)
    p.box(650, 86, 270, 72, "hello-web", "httpd · --network none")
    p.box(340, 196, 200, 60, "busybox:1.37.0", w["image"])
    p.arrow(540, 226, 700, 162, w["runs"], dx=8, dy=14)
    p.arrow(250, 120, 646, 120, None, color="podbag")
    p.arrow(250, 210, 646, 146, None, color="podbag")
