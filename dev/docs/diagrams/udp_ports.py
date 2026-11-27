"""The architecture of the udp-ports guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The container udp-server listens on UDP port 9999 and publishes 127.0.0.1:18111/udp; a client on the host network sends a datagram there, and podbag logs shows it',
    'ko': 'udp-server 컨테이너가 UDP 9999 포트에서 기다리고 127.0.0.1:18111/udp를 공개합니다. 호스트 네트워크의 클라이언트가 이 주소로 데이터그램을 보내고, podbag logs가 그 내용을 보여 줍니다',
    'ja': 'コンテナー udp-server が UDP ポート 9999 で待ち受け、127.0.0.1:18111/udp を公開します。ホストネットワーク上のクライアントがそこへデータグラムを送り、podbag logs がそれを表示します',
    'zh-CN': '容器 udp-server 在 UDP 端口 9999 上监听并发布 127.0.0.1:18111/udp；主机网络上的客户端向该地址发送数据报，podbag logs 显示它',
    'fil': 'Nakikinig ang container na udp-server sa UDP port 9999 at nagpa-publish ito ng 127.0.0.1:18111/udp; nagpapadala roon ng datagram ang client sa host network, at ipinapakita ito ng podbag logs',
    'es': 'El contenedor udp-server escucha en el puerto UDP 9999 y publica 127.0.0.1:18111/udp; un cliente en la red del host envía allí un datagrama, y podbag logs lo muestra',
    'vi': 'Container udp-server lắng nghe trên cổng UDP 9999 và công bố 127.0.0.1:18111/udp; một client trên mạng host gửi datagram tới đó, và podbag logs hiển thị nó',
}

WORDS = {
    'en': {'commands': 'podbag run · ps · logs', 'host': 'host network', 'datagram': 'datagram'},
    'ko': {'commands': 'podbag run · ps · logs', 'host': '호스트 네트워크', 'datagram': '데이터그램'},
    'ja': {'commands': 'podbag run · ps · logs', 'host': 'ホストネットワーク', 'datagram': 'データグラム'},
    'zh-CN': {'commands': 'podbag run · ps · logs', 'host': '主机网络', 'datagram': '数据报'},
    'fil': {'commands': 'podbag run · ps · logs', 'host': 'host network', 'datagram': 'datagram'},
    'es': {'commands': 'podbag run · ps · logs', 'host': 'red del host', 'datagram': 'datagrama'},
    'vi': {'commands': 'podbag run · ps · logs', 'host': 'mạng host', 'datagram': 'datagram'},
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 80, 210, 56, w["terminal"], w["commands"], mono_name=False)
    p.box(330, 214, 250, 64, "nc -u (--rm)", w["host"])
    p.box(630, 96, 280, 104, "udp-server", "nc -u -l -p 9999", port="127.0.0.1:18111/udp")
    p.arrow(580, 236, 680, 204, w["datagram"], dx=6, dy=20, color="accent")
    p.arrow(250, 108, 626, 130, w["logs"], at=0.75, dx=0, dy=-10, anchor="middle")
    p.arrow(250, 120, 326, 240, None, color="podbag")
