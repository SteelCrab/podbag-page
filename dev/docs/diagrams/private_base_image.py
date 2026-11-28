"""The architecture of the private-base-image guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The container registry asks for a login on 127.0.0.1:18112; podbag login saves it, podbag push sends the base image there, and podbag build pulls it with the login for FROM',
    'ko': 'registry 컨테이너가 127.0.0.1:18112에서 로그인을 요구합니다. podbag login이 로그인을 저장하고, podbag push가 베이스 이미지를 보내며, podbag build가 그 로그인으로 FROM 이미지를 받습니다',
    'ja': 'コンテナー registry が 127.0.0.1:18112 でログインを求めます。podbag login がログインを保存し、podbag push がベースイメージを送り、podbag build がそのログインで FROM のイメージを取得します',
    'zh-CN': '容器 registry 在 127.0.0.1:18112 上要求登录；podbag login 保存登录，podbag push 把基础镜像推送过去，podbag build 用该登录拉取 FROM 镜像',
    'fil': 'Humihingi ng login ang container na registry sa 127.0.0.1:18112; sine-save ito ng podbag login, ipinapadala roon ng podbag push ang base image, at pini-pull ito ng podbag build gamit ang login para sa FROM',
    'es': 'El contenedor registry pide un inicio de sesión en 127.0.0.1:18112; podbag login lo guarda, podbag push envía allí la imagen base y podbag build la descarga con ese inicio de sesión para FROM',
    'vi': 'Container registry yêu cầu đăng nhập tại 127.0.0.1:18112; podbag login lưu thông tin đăng nhập, podbag push đẩy image nền lên đó, và podbag build dùng thông tin đó để kéo image trong FROM',
}

WORDS = {
    'en': {'commands': 'login · push · build · logout', 'login': 'the login',
           'registry_note': 'registry:2.8.3 · htpasswd', 'push': 'push', 'pull': 'pull with login'},
    'ko': {'commands': 'login · push · build · logout', 'login': '로그인 정보',
           'registry_note': 'registry:2.8.3 · htpasswd', 'push': 'push', 'pull': '로그인으로 pull'},
    'ja': {'commands': 'login · push · build · logout', 'login': 'ログイン情報',
           'registry_note': 'registry:2.8.3 · htpasswd', 'push': 'push', 'pull': 'ログインで pull'},
    'zh-CN': {'commands': 'login · push · build · logout', 'login': '登录信息',
              'registry_note': 'registry:2.8.3 · htpasswd', 'push': 'push', 'pull': '用登录拉取'},
    'fil': {'commands': 'login · push · build · logout', 'login': 'ang login',
            'registry_note': 'registry:2.8.3 · htpasswd', 'push': 'push', 'pull': 'pull gamit ang login'},
    'es': {'commands': 'login · push · build · logout', 'login': 'el inicio de sesión',
           'registry_note': 'registry:2.8.3 · htpasswd', 'push': 'push', 'pull': 'pull con login'},
    'vi': {'commands': 'login · push · build · logout', 'login': 'thông tin đăng nhập',
           'registry_note': 'registry:2.8.3 · htpasswd', 'push': 'push', 'pull': 'pull bằng đăng nhập'},
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 80, 210, 56, w["terminal"], w["commands"], mono_name=False)
    p.box(40, 176, 210, 64, "docker/config.json", w["login"])
    p.box(330, 90, 250, 64, "training/base:1", w["image"])
    p.box(330, 214, 250, 64, "hello-app:1", "FROM ${BASE}")
    p.box(680, 140, 230, 104, "registry", w["registry_note"], port="127.0.0.1:18112")
    p.arrow(580, 122, 676, 170, w["push"], dx=-10, dy=-10, color="accent")
    p.arrow(676, 214, 580, 246, w["pull"], dx=-34, dy=30, color="accent")
    p.arrow(250, 208, 676, 192, None, color="podbag")
