"""The architecture of the swarm-service guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'In a one-node swarm, the service web runs its replicas as the containers web.1, web.2 and web.3 on the network ingress',
    'ko': '노드가 하나인 swarm에서 web 서비스가 복제본을 ingress 네트워크의 web.1, web.2, web.3 컨테이너로 실행합니다',
    'ja': '1 ノードの swarm で、サービス web がレプリカをネットワーク ingress 上のコンテナ web.1、web.2、web.3 として実行します',
    'zh-CN': '在单节点 swarm 中，服务 web 在网络 ingress 上以容器 web.1、web.2 和 web.3 运行副本',
    'fil': 'Sa swarm na may iisang node, pinapatakbo ng service na web ang mga replica nito bilang mga container na web.1, web.2 at web.3 sa network na ingress',
    'es': 'En un swarm de un nodo, el servicio web ejecuta sus réplicas como los contenedores web.1, web.2 y web.3 en la red ingress',
    'vi': 'Trong swarm một nút, dịch vụ web chạy các bản sao dưới dạng container web.1, web.2 và web.3 trong mạng ingress',
}

WORDS = {
    'en': {
        'commands': 'swarm · service · podbag ps',
        'service': 'service web',
        'replicas': 'replicas: 2, then 3',
        'swarm_note': 'one node: this session',
        'task': 'task · httpd :8080',
        'added': 'added by scale',
        'runs_tasks': 'runs tasks',
    },
    'ko': {
        'commands': 'swarm · service · podbag ps',
        'service': '서비스 web',
        'replicas': '복제본: 2개, 그다음 3개',
        'swarm_note': '노드 하나: 이 실습 환경',
        'task': '작업 · httpd :8080',
        'added': 'scale로 추가',
        'runs_tasks': '작업 실행',
    },
    'ja': {
        'commands': 'swarm · service · podbag ps',
        'service': 'サービス web',
        'replicas': 'レプリカ: 2、次に 3',
        'swarm_note': '1 ノード: この実習環境',
        'task': 'タスク · httpd :8080',
        'added': 'scale で追加',
        'runs_tasks': 'タスクを実行',
    },
    'zh-CN': {
        'commands': 'swarm · service · podbag ps',
        'service': '服务 web',
        'replicas': '副本：2，然后 3',
        'swarm_note': '单节点：本练习环境',
        'task': '任务 · httpd :8080',
        'added': '由 scale 添加',
        'runs_tasks': '运行任务',
    },
    'fil': {
        'commands': 'swarm · service · podbag ps',
        'service': 'service na web',
        'replicas': 'replica: 2, saka 3',
        'swarm_note': 'iisang node: ang session na ito',
        'task': 'task · httpd :8080',
        'added': 'idinagdag ng scale',
        'runs_tasks': 'nagpapatakbo ng mga task',
    },
    'es': {
        'commands': 'swarm · service · podbag ps',
        'service': 'servicio web',
        'replicas': 'réplicas: 2, luego 3',
        'swarm_note': 'un nodo: esta sesión',
        'task': 'tarea · httpd :8080',
        'added': 'añadida con scale',
        'runs_tasks': 'ejecuta tareas',
    },
    'vi': {
        'commands': 'swarm · service · podbag ps',
        'service': 'dịch vụ web',
        'replicas': 'bản sao: 2, rồi 3',
        'swarm_note': 'một nút: phiên này',
        'task': 'task · httpd :8080',
        'added': 'thêm bằng scale',
        'runs_tasks': 'chạy các task',
    },
}


def draw(p, w):
    frame(p, w, 330)
    p.box(40, 80, 210, 56, w["terminal"], w["commands"], mono_name=False)
    p.box(330, 80, 250, 64, w["service"], w["replicas"], mono_name=False)
    p.box(640, 80, 270, 64, "swarm", w["swarm_note"])
    p.network(330, 176, 590, 116, "ingress")
    p.box(350, 210, 170, 64, "web.1", w["task"])
    p.box(540, 210, 170, 64, "web.2", w["task"])
    p.box(730, 210, 170, 64, "web.3", w["added"], color="accent")
    p.arrow(455, 144, 455, 206, w["runs_tasks"], dx=10, dy=-14)
