import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, PngImagePlugin

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from create_synthetic_demo import create_masters


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.lib = self.root / "library"
        create_masters(self.root / "inputs")
        self.brief = self.root / "brief.json"
        self.write_brief("A small experiment", "Try one useful idea.")

    def write_brief(self, title, point):
        self.brief.write_text(json.dumps({"schema_version": "1.0", "title": title, "point": point}))

    def cli(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/ip_library.py"), *map(str, args)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0 if ok else 2, result.stderr)
        return result

    def record(self, *extra, ok=True):
        return self.cli("record", "--library", self.lib, *extra, ok=ok)

    def initial(self):
        self.record("--identity-id", "demo", "--style", "anime", "--square", self.root / "inputs/square.png",
                    "--cutout", self.root / "inputs/cutout.png", "--synthetic", "--confirmed")

    def build(self, name="kit", version="v0001", ok=True):
        return self.cli("build", "--library", self.lib, "--version", version, "--brief", self.brief,
                        "--out", self.root / name, ok=ok)

    def test_reuse_preserves_identity_bytes_and_delivers_editable_text(self):
        self.initial()
        self.build()
        first = self.lib.joinpath("versions/v0001/cutout.png").read_bytes()
        self.write_brief("<script>alert('x')</script>", "一个虚构的主题 & a point")
        self.build("next")
        a = json.loads((self.root / "kit/kit-manifest.json").read_text())
        b = json.loads((self.root / "next/kit-manifest.json").read_text())
        self.assertEqual(a["master_hashes"], b["master_hashes"])
        self.assertEqual((self.root / "kit/avatar.png").read_bytes(), (self.root / "next/avatar.png").read_bytes())
        self.assertEqual(first, self.lib.joinpath("versions/v0001/cutout.png").read_bytes())
        svg = ET.parse(self.root / "next/cover.svg")
        self.assertTrue(svg.findall("{http://www.w3.org/2000/svg}text"))
        self.assertFalse(svg.findall(".//{http://www.w3.org/2000/svg}script"))
        self.assertNotIn("<script>", (self.root / "next/preview.html").read_text())
        for file, size in a["checks"]["dimensions"].items():
            with Image.open(self.root / "kit" / file) as image:
                self.assertEqual(image.size, tuple(size))
        with Image.open(self.root / "kit/ppt-cutout.png") as image:
            self.assertEqual(image.getchannel("A").getextrema(), (0, 255))
        for item in b["outputs"]:
            self.assertEqual(item["sha256"], hashlib.sha256((self.root / "next" / item["file"]).read_bytes()).hexdigest())
        self.assertNotIn(str(self.root), json.dumps(b))

    def test_palette_revision_preserves_masters_and_parent(self):
        self.initial()
        self.record("--base", "v0001", "--accent", "#29A398", "--confirmed")
        first, second = [self.lib / "versions" / v for v in ("v0001", "v0002")]
        for role in ("square", "cutout"):
            self.assertEqual((first / f"{role}.png").read_bytes(), (second / f"{role}.png").read_bytes())
        data = json.loads((second / "identity.json").read_text())
        self.assertEqual(data["parent_version"], "v0001")
        self.assertEqual(data["palette"]["accent"], "#29A398")

    def test_local_master_change_preserves_other_master_and_old_version(self):
        self.initial()
        old = (self.lib / "versions/v0001/cutout.png").read_bytes()
        Image.new("RGBA", (300, 300), "orange").save(self.root / "changed.png")
        self.record("--base", "v0001", "--square", self.root / "changed.png", "--confirmed")
        self.assertEqual(old, (self.lib / "versions/v0002/cutout.png").read_bytes())
        self.assertNotEqual((self.lib / "versions/v0001/square.png").read_bytes(), (self.lib / "versions/v0002/square.png").read_bytes())

    def test_failure_paths_do_not_create_deliveries(self):
        self.initial()
        self.build("bad", "../escape", ok=False)
        self.write_brief("长" * 80, "观点")
        self.assertIn("shorten", self.build("overflow", ok=False).stderr)
        self.assertFalse((self.root / "overflow").exists())
        self.write_brief("Title", "Point")
        (self.lib / "versions/v0001/cutout.png").write_bytes(b"corrupt")
        self.assertIn("integrity", self.build("tampered", ok=False).stderr)
        self.assertFalse((self.root / "tampered").exists())

    def test_confirmation_and_valid_alpha_required(self):
        result = self.record("--identity-id", "demo", "--style", "anime", "--square", self.root / "inputs/square.png",
                             "--cutout", self.root / "inputs/cutout.png", ok=False)
        self.assertIn("--confirmed", result.stderr)
        self.assertFalse(self.lib.exists())
        Image.new("RGBA", (100, 100), "white").save(self.root / "opaque.png")
        self.record("--identity-id", "demo", "--style", "anime", "--square", self.root / "inputs/square.png",
                    "--cutout", self.root / "opaque.png", "--confirmed", ok=False)
        self.assertFalse(self.lib.exists())

    def test_no_overwrite_and_no_lineage_reset(self):
        self.initial()
        self.build()
        self.assertIn("already exists", self.build(ok=False).stderr)
        self.assertIn("--base", self.record("--identity-id", "other", ok=False).stderr)

    def test_metadata_stripping_and_source_directory_guard(self):
        path = self.root / "inputs/square.png"
        with Image.open(path) as image:
            info = PngImagePlugin.PngInfo()
            info.add_text("private-note", "SYNTHETIC PRIVATE METADATA")
            image.save(self.root / "metadata.png", pnginfo=info)
        self.record("--identity-id", "demo", "--style", "anime", "--square", self.root / "metadata.png",
                    "--cutout", self.root / "inputs/cutout.png", "--confirmed")
        with Image.open(self.lib / "versions/v0001/square.png") as image:
            self.assertEqual(image.info, {})
        result = self.cli("record", "--library", ROOT / "private-library", ok=False)
        self.assertIn("outside", result.stderr)

    def test_low_contrast_palette_rejected(self):
        self.initial()
        self.record("--base", "v0001", "--text", "#FFF8EE", "--confirmed")
        self.assertIn("contrast", self.build("contrast", "v0002", ok=False).stderr)
        self.assertFalse((self.root / "contrast").exists())


if __name__ == "__main__":
    unittest.main()
