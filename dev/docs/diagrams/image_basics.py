"""The architecture of the image-basics guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 320

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The terminal pulls busybox:1.37.0, gives it a second name my-busybox:1 and runs a container from that name; then it removes both names',
    'ko': '터미널이 busybox:1.37.0을 내려받고 my-busybox:1이라는 두 번째 이름을 붙인 뒤 그 이름으로 컨테이너를 실행합니다. 마지막에 두 이름을 모두 삭제합니다',
    'ja': 'ターミナルが busybox:1.37.0 を取得し、2 つ目の名前 my-busybox:1 を付け、その名前でコンテナを実行します。その後、両方の名前を削除します',
    'zh-CN': '终端拉取 busybox:1.37.0，为它添加第二个名称 my-busybox:1，并用这个名称运行容器；然后删除这两个名称',
    'fil': 'Kinukuha ng terminal ang busybox:1.37.0, binibigyan ito ng pangalawang pangalan na my-busybox:1 at nagpapatakbo ng container mula sa pangalang iyon; pagkatapos, inaalis nito ang dalawang pangalan',
    'es': 'La terminal descarga busybox:1.37.0, le da un segundo nombre my-busybox:1 y ejecuta un contenedor con ese nombre; después elimina los dos nombres',
    'vi': 'Terminal kéo busybox:1.37.0, đặt thêm tên my-busybox:1 và chạy container từ tên đó; sau đó xóa cả hai tên',
}

WORDS = {
    'en': {
        'pull': 'pull',
        'tag': 'tag',
        'from_hub': 'image · from docker.io',
        'same_image': 'another name, same image',
        'once': 'removed when it ends',
    },
    'ko': {
        'pull': '내려받기',
        'tag': '이름 붙이기',
        'from_hub': '이미지 · docker.io에서',
        'same_image': '다른 이름, 같은 이미지',
        'once': '끝나면 삭제됨',
    },
    'ja': {
        'pull': '取得',
        'tag': 'タグ付け',
        'from_hub': 'イメージ · docker.io から',
        'same_image': '別の名前、同じイメージ',
        'once': '終了すると削除',
    },
    'zh-CN': {
        'pull': 'pull',
        'tag': 'tag',
        'from_hub': '镜像 · 来自 docker.io',
        'same_image': '另一个名称，同一个镜像',
        'once': '结束后删除',
    },
    'fil': {
        'pull': 'pull',
        'tag': 'tag',
        'from_hub': 'image · mula sa docker.io',
        'same_image': 'ibang pangalan, parehong image',
        'once': 'naaalis kapag natapos',
    },
    'es': {
        'pull': 'pull',
        'tag': 'tag',
        'from_hub': 'imagen · de docker.io',
        'same_image': 'otro nombre, misma imagen',
        'once': 'se elimina al terminar',
    },
    'vi': {
        'pull': 'pull',
        'tag': 'tag',
        'from_hub': 'image · từ docker.io',
        'same_image': 'tên khác, cùng image',
        'once': 'bị xóa khi kết thúc',
    },
}


def draw(p, w):
    frame(p, w, 320)
    p.box(40, 100, 210, 60, w["terminal"], "podbag pull · tag · rmi", mono_name=False)
    p.box(340, 90, 250, 64, "busybox:1.37.0", w["from_hub"])
    p.box(340, 210, 250, 64, "my-busybox:1", w["same_image"])
    p.box(680, 210, 230, 64, "run --rm", w["once"])
    p.arrow(250, 128, 336, 122, w["pull"], dx=-18, dy=-8, color="podbag")
    p.arrow(465, 154, 465, 206, w["tag"], dx=10, dy=4)
    p.arrow(590, 242, 676, 242, w["runs"], dx=-16, dy=-8)
