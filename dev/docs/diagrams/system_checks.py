"""The architecture of the system-checks guide."""
from training_diagrams import frame  # noqa: F401

HEIGHT = 320

# The alt text, also the picture's title: what the module builds.
ALT = {
    'en': 'podbag check reads the system, podbag check-image reads the programs in busybox, and podbag system df and verify read the stored files',
    'ko': 'podbag check는 시스템을, podbag check-image는 busybox의 프로그램을, podbag system df와 verify는 저장된 파일을 확인합니다',
    'ja': 'podbag check がシステムを、podbag check-image が busybox 内のプログラムを、podbag system df と verify が保存されたファイルを読みます',
    'zh-CN': 'podbag check 读取系统信息，podbag check-image 读取 busybox 中的程序，podbag system df 和 verify 读取已存储的文件',
    'fil': 'Binabasa ng podbag check ang system, binabasa ng podbag check-image ang mga program sa busybox, at binabasa ng podbag system df at verify ang mga naka-imbak na file',
    'es': 'podbag check lee el sistema, podbag check-image lee los programas de busybox, y podbag system df y verify leen los archivos guardados',
    'vi': 'podbag check đọc hệ thống, podbag check-image đọc các chương trình trong busybox, còn podbag system df và verify đọc các tệp đã lưu',
}

WORDS = {
    'en': {
        'system': 'System',
        'system_note': 'kernel · cgroup v2 · keeper',
        'programs': 'programs and libraries',
        'store': 'Stored files',
        'store_note': 'sizes and hashes',
    },
    'ko': {
        'system': '시스템',
        'system_note': '커널 · cgroup v2 · keeper',
        'programs': '프로그램과 라이브러리',
        'store': '저장된 파일',
        'store_note': '크기와 해시',
    },
    'ja': {
        'system': 'システム',
        'system_note': 'カーネル · cgroup v2 · keeper',
        'programs': 'プログラムとライブラリ',
        'store': '保存されたファイル',
        'store_note': 'サイズとハッシュ',
    },
    'zh-CN': {
        'system': '系统',
        'system_note': '内核 · cgroup v2 · keeper',
        'programs': '程序和库',
        'store': '已存储的文件',
        'store_note': '大小和哈希值',
    },
    'fil': {
        'system': 'System',
        'system_note': 'kernel · cgroup v2 · keeper',
        'programs': 'mga program at library',
        'store': 'Mga naka-imbak na file',
        'store_note': 'mga laki at hash',
    },
    'es': {
        'system': 'Sistema',
        'system_note': 'kernel · cgroup v2 · keeper',
        'programs': 'programas y bibliotecas',
        'store': 'Archivos guardados',
        'store_note': 'tamaños y hashes',
    },
    'vi': {
        'system': 'Hệ thống',
        'system_note': 'kernel · cgroup v2 · keeper',
        'programs': 'chương trình và thư viện',
        'store': 'Tệp đã lưu',
        'store_note': 'dung lượng và hash',
    },
}


def draw(p, w):
    frame(p, w, HEIGHT)
    p.box(40, 84, 210, 204, w["terminal"], "podbag check · system", mono_name=False)
    p.box(470, 84, 300, 56, w["system"], w["system_note"], mono_name=False)
    p.box(470, 158, 300, 56, "busybox:1.37.0", w["programs"])
    p.box(470, 232, 300, 56, w["store"], w["store_note"], mono_name=False)
    p.arrow(250, 112, 466, 112, "check", dx=0, dy=-8, anchor="middle", mono=True)
    p.arrow(250, 186, 466, 186, "check-image", dx=0, dy=-8, anchor="middle", mono=True)
    p.arrow(250, 260, 466, 260, "system df · verify", dx=0, dy=-8, anchor="middle", mono=True)
