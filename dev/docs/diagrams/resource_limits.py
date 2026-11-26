"""The architecture of the resource-limits guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 310

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'The container app runs in a cgroup with memory.max and cpu.max; podbag update raises the memory limit from 64 MiB to 128 MiB while it runs',
    'ko': 'app 컨테이너는 memory.max와 cpu.max가 있는 cgroup 안에서 실행됩니다. podbag update가 실행 중에 메모리 제한을 64 MiB에서 128 MiB로 늘립니다',
    'ja': 'コンテナ app が memory.max と cpu.max を持つ cgroup の中で動きます。podbag update が実行中にメモリの制限を 64 MiB から 128 MiB に引き上げます',
    'zh-CN': '容器 app 在带有 memory.max 和 cpu.max 的 cgroup 中运行；podbag update 在运行时将内存限制从 64 MiB 提高到 128 MiB',
    'fil': 'Tumatakbo ang container na app sa isang cgroup na may memory.max at cpu.max; itinataas ng podbag update ang limitasyon sa memory mula 64 MiB hanggang 128 MiB habang tumatakbo ito',
    'es': 'El contenedor app se ejecuta en un cgroup con memory.max y cpu.max; podbag update sube el límite de memoria de 64 MiB a 128 MiB mientras se ejecuta',
    'vi': 'Container app chạy trong một cgroup có memory.max và cpu.max; podbag update nâng giới hạn bộ nhớ từ 64 MiB lên 128 MiB khi container đang chạy',
}

WORDS = {
    'en': {
        'limits': 'limits',
        'half_cpu': '50000 100000 · half a CPU',
    },
    'ko': {
        'limits': '제한',
        'half_cpu': '50000 100000 · CPU 절반',
    },
    'ja': {
        'limits': '制限',
        'half_cpu': '50000 100000 · CPU 半分',
    },
    'zh-CN': {
        'limits': '限制',
        'half_cpu': '50000 100000 · 半个 CPU',
    },
    'fil': {
        'limits': 'mga limitasyon',
        'half_cpu': '50000 100000 · kalahating CPU',
    },
    'es': {
        'limits': 'límites',
        'half_cpu': '50000 100000 · media CPU',
    },
    'vi': {
        'limits': 'giới hạn',
        'half_cpu': '50000 100000 · nửa CPU',
    },
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 100, 210, 110, w["terminal"], "podbag run · exec", mono_name=False)
    p.text(54, 188, "stats · top · update", 11.5)
    p.network(330, 80, 590, 190, "cgroup")
    p.box(360, 140, 210, 72, "app", "sleep 3600")
    p.box(660, 112, 230, 60, "memory.max", "64 MiB → 128 MiB")
    p.box(660, 188, 230, 60, "cpu.max", w["half_cpu"])
    p.arrow(656, 142, 574, 166, w["limits"], dx=-6, dy=-10, anchor="middle")
    p.arrow(656, 218, 574, 190, None)
    p.arrow(250, 132, 326, 132, None, color="accent")
    p.arrow(326, 180, 250, 180, None)
