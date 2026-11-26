"""The architecture of the cli-tui-volumes guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 300

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The terminal creates and lists the volume my-api in the practice session; Podbag Desktop or the TUI inspects and deletes it',
    'ko': '터미널이 실습 환경에서 my-api 볼륨을 만들고 확인합니다. Podbag Desktop 또는 TUI가 이 볼륨을 살펴보고 삭제합니다',
    'ja': 'ターミナルが練習環境でボリューム my-api を作成して一覧表示し、Podbag Desktop または TUI が確認して削除します',
    'zh-CN': '终端在练习环境中创建并列出卷 my-api，Podbag Desktop 或 TUI 查看并删除它',
    'fil': 'Gumagawa at naglilista ang terminal ng volume na my-api sa practice session; tinitingnan at binubura ito ng Podbag Desktop o ng TUI',
    'es': 'La terminal crea y lista el volumen my-api en la sesión de práctica; Podbag Desktop o la TUI lo revisa y lo elimina',
    'vi': 'Terminal tạo và liệt kê volume my-api trong phiên thực hành; Podbag Desktop hoặc TUI xem và xóa nó',
}


def draw(p, w):
    frame(p, w, 300)
    p.box(40, 90, 210, 60, w["terminal"], "podbag volume create · ls", mono_name=False)
    p.box(40, 180, 210, 60, w["desktop"], w["or_tui"] + ": " + w["inspect"], mono_name=False)
    p.volume(620, 100, 200, 100, "my-api", w["volume"])
    p.arrow(250, 120, 616, 140, None, color="podbag")
    p.arrow(250, 210, 616, 166, None, color="podbag")
