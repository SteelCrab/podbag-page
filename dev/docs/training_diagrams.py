#!/usr/bin/env python3
"""The architecture picture at the top of each Training guide: what the module builds.

site/blog/posts/<guide>/architecture-<lang>-{light,dark}.svg, for each language the guide is
written in. The left side is your computer (terminal, Podbag Desktop, browser); the right side
is the temporary practice session with its containers, volumes and networks.

Each guide has its own file, dev/docs/diagrams/<guide>.py (dashes as underscores):
HEIGHT, ALT (the picture's text in each language) and draw(p, w), which uses Picture and
frame from here. WORDS there adds or overrides words of this file's WORDS.

usage: python3 dev/docs/training_diagrams.py    # writes the pictures; commit them
"""
from html import escape
from pathlib import Path

POSTS = Path(__file__).resolve().parents[2] / "site" / "blog" / "posts"
FONT = "ui-sans-serif, -apple-system, 'Segoe UI', 'Apple SD Gothic Neo', 'Hiragino Sans', 'PingFang SC', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
THEMES = {
    "light": {"surface": "#fcfcfb", "panel": "#ffffff", "box": "#f2f1ed", "line": "#c3c2b7",
              "ink": "#0b0b0b", "ink2": "#52514e", "arrow": "#898781", "accent": "#2a78d6",
              "net": "#eaf1fb", "podbag": "#8853b4", "bad": "#c2410c", "good": "#15803d",
              "on": "#ffffff"},
    "dark": {"surface": "#1a1a19", "panel": "#141413", "box": "#242422", "line": "#45453f",
             "ink": "#f0efec", "ink2": "#c3c2b7", "arrow": "#9a988f", "accent": "#3987e5",
             "net": "#17263a", "podbag": "#b88ae0", "bad": "#fb923c", "good": "#4ade80",
             "on": "#ffffff"},
}
W = 960

WORDS = {
    "en": {"computer": "Your computer", "session": "Practice session",
           "session_note": "temporary: removed when you type exit", "terminal": "Terminal",
           "browser": "Browser", "desktop": "Podbag Desktop", "image": "image",
           "volume": "volume", "network": "network", "runs": "runs", "writes": "writes",
           "reads": "reads", "stop": "stop", "ports": "ports, stop", "inspect": "inspect, delete",
           "logs": "logs", "replaces": "replaces", "exited": "exited (1)", "running": "running",
           "by_name": "by name", "copies": "copies the page", "no_port": "no published port",
           "stays": "stays after the containers go",
           "or_tui": "or the TUI"},
    "ko": {"computer": "내 컴퓨터", "session": "실습 환경",
           "session_note": "임시 환경: exit를 입력하면 삭제됩니다", "terminal": "터미널",
           "browser": "브라우저", "desktop": "Podbag Desktop", "image": "이미지",
           "volume": "볼륨", "network": "네트워크", "runs": "실행", "writes": "쓰기",
           "reads": "읽기", "stop": "중지", "ports": "포트 확인, 중지", "inspect": "확인, 삭제",
           "logs": "로그", "replaces": "교체", "exited": "종료됨 (1)", "running": "실행 중",
           "by_name": "이름으로 접속", "copies": "페이지 복사", "no_port": "공개 포트 없음",
           "stays": "컨테이너를 지워도 남음",
           "or_tui": "또는 TUI"},
    "ja": {"computer": "このコンピューター", "session": "練習環境",
           "session_note": "一時的: exit で削除されます", "terminal": "ターミナル",
           "browser": "ブラウザー", "desktop": "Podbag Desktop", "volume": "ボリューム",
           "inspect": "確認、削除", "or_tui": "または TUI"},
    "zh-CN": {"computer": "你的电脑", "session": "练习环境",
              "session_note": "临时环境：输入 exit 后删除", "terminal": "终端",
              "browser": "浏览器", "desktop": "Podbag Desktop", "volume": "卷",
              "inspect": "查看、删除", "or_tui": "或 TUI"},
    "fil": {"computer": "Iyong computer", "session": "Practice session",
            "session_note": "pansamantala: nabubura kapag nag-exit ka", "terminal": "Terminal",
            "browser": "Browser", "desktop": "Podbag Desktop", "volume": "volume",
            "inspect": "tingnan, burahin", "or_tui": "o ang TUI"},
    "es": {"computer": "Tu computadora", "session": "Sesión de práctica",
           "session_note": "temporal: se borra al escribir exit", "terminal": "Terminal",
           "browser": "Navegador", "desktop": "Podbag Desktop", "volume": "volumen",
           "inspect": "ver, eliminar", "or_tui": "o la TUI"},
    "vi": {"computer": "Máy tính của bạn", "session": "Phiên thực hành",
           "session_note": "tạm thời: bị xóa khi bạn gõ exit", "terminal": "Terminal",
           "browser": "Trình duyệt", "desktop": "Podbag Desktop", "volume": "volume",
           "inspect": "xem, xóa", "or_tui": "hoặc TUI"},
}

class Picture:
    def __init__(self, t, height):
        self.t, self.h, self.o = t, height, []

    def text(self, x, y, s, size=12.5, color="ink2", weight=None, anchor="start", mono=False):
        w = f' font-weight="{weight}"' if weight else ""
        f = f' font-family="{MONO}"' if mono else ""
        self.o.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{self.t[color]}"{w}{f} '
                      f'text-anchor="{anchor}">{escape(s)}</text>')

    def panel(self, x, y, w, h, title, note=None, dashed=False):
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
                      f'fill="{self.t["panel"]}" stroke="{self.t["line"]}"{dash}/>')
        self.text(x + 18, y + 28, title, 15, "ink", 700)
        if note:
            self.text(x + 18, y + 47, note, 11.5)

    def box(self, x, y, w, h, name, note=None, color="line", mono_name=True, badge=None, port=None):
        self.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
                      f'fill="{self.t["box"]}" stroke="{self.t[color]}" stroke-width="1.4"/>')
        if note:
            self.text(x + 14, y + h / 2 - 3, name, 14, "ink", 600, mono=mono_name)
            self.text(x + 14, y + h / 2 + 15, note, 11.5)
        else:
            self.text(x + 14, y + h / 2 + 5, name, 14, "ink", 600, mono=mono_name)
        if badge:
            label, tone = badge
            bw = 7.2 * len(label) + 18
            self.o.append(f'<rect x="{x + w - bw - 10}" y="{y + 10}" width="{bw}" height="20" rx="10" '
                          f'fill="none" stroke="{self.t[tone]}"/>')
            self.text(x + w - bw / 2 - 10, y + 24, label, 11, tone, 600, "middle")
        if port:
            # The address the box publishes on this computer.
            pw = 7 * len(port) + 18
            self.o.append(f'<rect x="{x + w - pw - 10}" y="{y + h - 30}" width="{pw}" height="20" '
                          f'rx="10" fill="{self.t["accent"]}"/>')
            self.text(x + w - pw / 2 - 10, y + h - 16, port, 11, "on", 600, "middle", mono=True)

    def volume(self, x, y, w, h, name, note=None):
        t, ry = self.t, 9
        self.o.append(f'<path d="M{x} {y + ry} a{w / 2} {ry} 0 0 1 {w} 0 v{h - 2 * ry} '
                      f'a{w / 2} {ry} 0 0 1 {-w} 0 z" fill="{t["box"]}" stroke="{t["podbag"]}" '
                      f'stroke-width="1.4"/>')
        self.o.append(f'<path d="M{x} {y + ry} a{w / 2} {ry} 0 0 0 {w} 0" fill="none" '
                      f'stroke="{t["podbag"]}" stroke-width="1.4"/>')
        self.text(x + w / 2, y + h / 2 + 6, name, 14, "ink", 600, "middle", mono=True)
        if note:
            self.text(x + w / 2, y + h + 18, note, 11.5, anchor="middle")

    def network(self, x, y, w, h, name):
        self.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{self.t["net"]}" '
                      f'stroke="{self.t["accent"]}" stroke-dasharray="4 4"/>')
        self.text(x + 14, y + 22, name, 12.5, "accent", 700, mono=True)

    def arrow(self, x1, y1, x2, y2, label=None, at=0.5, dx=8, dy=-6, color="arrow", both=False,
              anchor="start", mono=False):
        t = self.t
        self.o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t[color]}" '
                      f'stroke-width="1.6" marker-end="url(#head-{color})"'
                      f'{f" marker-start=\"url(#tail-{color})\"" if both else ""}/>')
        if label:
            lx, ly = x1 + (x2 - x1) * at + dx, y1 + (y2 - y1) * at + dy
            for i, line in enumerate(label.split("\n")):
                self.text(lx, ly + i * 15, line, 11.5, "ink2", None, anchor, mono=mono)

    def document(self, title):
        t = self.t
        heads = "".join(
            f'<marker id="head-{c}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
            f'markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{t[c]}"/></marker>'
            f'<marker id="tail-{c}" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="8" '
            f'markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{t[c]}"/></marker>'
            for c in ("arrow", "accent", "podbag", "bad"))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{self.h}" '
                f'viewBox="0 0 {W} {self.h}" role="img" aria-label="{escape(title, quote=True)}" '
                f'font-family="{FONT}">\n<title>{escape(title)}</title>\n<defs>{heads}</defs>\n'
                f'<rect width="{W}" height="{self.h}" rx="12" fill="{t["surface"]}"/>\n'
                + "\n".join(self.o) + "\n</svg>\n")


def frame(p, w, height):
    """The two sides; the computer on the left, the session on the right."""
    p.panel(20, 20, 250, height - 40, w["computer"])
    p.panel(300, 20, W - 320, height - 40, w["session"], w["session_note"], dashed=True)


def guides():
    """{guide: module} from dev/docs/diagrams/<guide>.py (dashes as underscores)."""
    import importlib
    folder = Path(__file__).resolve().parent / "diagrams"
    found = {}
    for file in sorted(folder.glob("*.py")):
        if file.stem.startswith("_"):
            continue
        found[file.stem.replace("_", "-")] = importlib.import_module(f"diagrams.{file.stem}")
    return found


def pictures():
    """{(guide, file name): svg text} for every guide and the languages it is written in."""
    out = {}
    for guide, module in guides().items():
        for page in sorted((POSTS / guide).glob("*.md")):
            lang = page.stem
            words = {**WORDS["en"], **WORDS.get(lang, {}),
                     **getattr(module, "WORDS", {}).get("en", {}),
                     **getattr(module, "WORDS", {}).get(lang, {})}
            title = module.ALT.get(lang) or module.ALT["en"]
            for theme, t in THEMES.items():
                p = Picture(t, module.HEIGHT)
                module.draw(p, words)
                out[(guide, f"architecture-{lang}-{theme}.svg")] = p.document(title)
    return out


def main():
    for (guide, name), text in pictures().items():
        (POSTS / guide / name).write_text(text)
        print(f"wrote site/blog/posts/{guide}/{name}")


if __name__ == "__main__":
    main()
