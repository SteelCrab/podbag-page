"""The architecture of the swarm-service guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 330

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'In a one-node swarm, the service web runs its replicas as the containers web.1, web.2 and web.3 on the network ingress',
    'ko': '노드가 하나인 swarm에서 web 서비스가 복제본을 ingress 네트워크의 web.1, web.2, web.3 컨테이너로 실행합니다',
}

WORDS = {
    "en": {"commands": "swarm · service · podbag ps", "service": "service web",
           "replicas": "replicas: 2, then 3", "swarm_note": "one node: this session",
           "task": "task · httpd :8080", "added": "added by scale", "runs_tasks": "runs tasks"},
    "ko": {"commands": "swarm · service · podbag ps", "service": "서비스 web",
           "replicas": "복제본: 2개, 그다음 3개", "swarm_note": "노드 하나: 이 실습 환경",
           "task": "작업 · httpd :8080", "added": "scale로 추가", "runs_tasks": "작업 실행"},
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
