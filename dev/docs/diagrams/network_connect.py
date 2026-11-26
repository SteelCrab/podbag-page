"""The architecture of the network-connect guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 400

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The server api is on front-net with the alias backend and on back-net with the alias store; one-time containers on each network call it by those names',
    'ko': 'api 서버는 front-net에서 backend라는 별칭을, back-net에서 store라는 별칭을 가집니다. 각 네트워크의 일회용 컨테이너가 이 이름으로 api를 호출합니다',
    'ja': 'サーバー api は front-net ではエイリアス backend、back-net ではエイリアス store を持ちます。各ネットワークの 1 回だけ動くコンテナが、その名前で api を呼び出します',
    'zh-CN': '服务器 api 在 front-net 中使用别名 backend，在 back-net 中使用别名 store；每个网络中的一次性容器通过这些名称调用它',
    'fil': 'Nasa front-net ang server na api na may alias na backend, at nasa back-net na may alias na store; tinatawag ito ng mga isang beses na container sa bawat network gamit ang mga pangalang iyon',
    'es': 'El servidor api está en front-net con el alias backend y en back-net con el alias store; los contenedores de un solo uso de cada red lo llaman por esos nombres',
    'vi': 'Máy chủ api ở trong front-net với bí danh backend và trong back-net với bí danh store; các container dùng một lần trong mỗi mạng gọi nó bằng các tên đó',
}

WORDS = {
    'en': {
        'first': 'first network',
        'connected': 'connected while stopped',
    },
    'ko': {
        'first': '첫 번째 네트워크',
        'connected': '중지된 상태에서 연결',
    },
    'ja': {
        'first': '最初のネットワーク',
        'connected': '停止中に接続',
    },
    'zh-CN': {
        'first': '第一个网络',
        'connected': '停止时连接',
    },
    'fil': {
        'first': 'unang network',
        'connected': 'ikinonekta habang nakahinto',
    },
    'es': {
        'first': 'primera red',
        'connected': 'conectada con api detenido',
    },
    'vi': {
        'first': 'mạng đầu tiên',
        'connected': 'kết nối khi đã dừng',
    },
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 80, 210, 56, w["terminal"], "network create · run · rm", mono_name=False)
    p.box(40, 188, 210, 56, w["terminal"], "network connect · disconnect", mono_name=False)
    p.network(330, 76, 590, 130, "front-net")
    p.text(430, 98, w["first"], 11.5)
    p.network(330, 226, 590, 130, "back-net")
    p.text(424, 248, w["connected"], 11.5)
    p.box(360, 118, 230, 64, "wget (--rm)", "http://backend:8080/")
    p.box(360, 268, 230, 64, "wget (--rm)", "http://store:8080/")
    p.box(720, 112, 180, 220, "api", "httpd :8080")
    p.arrow(590, 150, 716, 150, "backend", dx=-30, dy=-10, color="accent", mono=True)
    p.arrow(590, 300, 716, 300, "store", dx=-24, dy=-10, color="accent", mono=True)
    p.arrow(250, 216, 716, 216)
