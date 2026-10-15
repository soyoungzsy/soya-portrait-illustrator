import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_asset_pack.py"
PRESETS = ROOT / "assets" / "presets.json"


def create_scene(path: Path, size: tuple[int, int]) -> None:
    image = Image.new("RGBA", size, (255, 248, 238, 255))
    draw = ImageDraw.Draw(image)
    width, height = size
    draw.ellipse((width * 0.34, height * 0.18, width * 0.66, height * 0.48), fill=(242, 198, 168, 255))
    draw.rectangle((width * 0.28, height * 0.46, width * 0.72, height * 0.9), fill=(231, 111, 81, 255))
    image.save(path)


def create_cutout_with_low_alpha_halo(path: Path) -> None:
    image = Image.new("RGBA", (300, 500), (100, 50, 30, 8))
    draw = ImageDraw.Draw(image)
    draw.ellipse((90, 30, 210, 150), fill=(242, 198, 168, 255))
    draw.rounded_rectangle((60, 140, 240, 470), radius=70, fill=(231, 111, 81, 255))
    image.save(path)


class ExportAssetPackTests(unittest.TestCase):
    def isolated_exporter(self, temp):
        source = temp / "skill-source"
        (source / "scripts").mkdir(parents=True)
        (source / "assets").mkdir()
        script = source / "scripts/export_asset_pack.py"
        shutil.copyfile(EXPORTER, script)
        presets = {"presets": [{"id": "probe", "category": "avatars", "width": 64, "height": 64,
                                "source": "square", "operation": "cover"}]}
        (source / "assets/presets.json").write_text(json.dumps(presets))
        square, cutout = temp / "square.png", temp / "cutout.png"
        create_scene(square, (64, 64))
        create_cutout_with_low_alpha_halo(cutout)
        command = [sys.executable, str(script), "--square", str(square), "--vertical", str(square),
                   "--wide", str(square), "--cutout", str(cutout), "--overwrite", "--out"]
        return source, command

    def test_source_repository_outputs_rejected_before_writing(self):
        with tempfile.TemporaryDirectory() as temp_value:
            temp = Path(temp_value)
            source, command = self.isolated_exporter(temp)
            before = {p.relative_to(source): p.read_bytes() for p in source.rglob("*") if p.is_file()}
            for output in (source, source / "generated", source / "scripts/../assets/exports"):
                with self.subTest(output=output):
                    result = subprocess.run([*command, str(output)], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("outside", result.stderr)
            after = {p.relative_to(source): p.read_bytes() for p in source.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

    def test_source_aliases_and_lexical_source_paths_rejected(self):
        with tempfile.TemporaryDirectory() as temp_value:
            temp = Path(temp_value)
            source, command = self.isolated_exporter(temp)
            alias = temp / "source-alias"
            alias.symlink_to(source, target_is_directory=True)
            external = temp / "external"
            external.mkdir()
            (source / "external-alias").symlink_to(external, target_is_directory=True)
            for output in (alias, alias / "generated", source / "external-alias/generated"):
                with self.subTest(output=output):
                    result = subprocess.run([*command, str(output)], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 2, result.stderr)
            self.assertFalse((source / "generated").exists())
            self.assertFalse((external / "generated").exists())

    def test_all_outputs_reject_existing_symlinks_before_export(self):
        with tempfile.TemporaryDirectory() as temp_value:
            temp = Path(temp_value)
            source, command = self.isolated_exporter(temp)
            victim = source / "protected.txt"
            victim.write_bytes(b"preserve existing data")
            for index, name in enumerate(("avatars", "avatars/probe.png", "contact-sheet.jpg", "pack-manifest.json")):
                with self.subTest(output=name):
                    output = temp / f"output-{index}"
                    link = output / name
                    link.parent.mkdir(parents=True)
                    link.symlink_to(source if name == "avatars" else victim, target_is_directory=name == "avatars")
                    result = subprocess.run([*command, str(output)], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertEqual(victim.read_bytes(), b"preserve existing data")
                    self.assertTrue(link.is_symlink())
                    self.assertEqual([p for p in output.rglob("*") if p.is_file() and not p.is_symlink()], [])

    def test_default_pack_dimensions_transparency_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_value:
            temp = Path(temp_value)
            square = temp / "square.png"
            vertical = temp / "vertical.png"
            wide = temp / "wide.png"
            cutout = temp / "cutout.png"
            output = temp / "output"
            create_scene(square, (512, 512))
            create_scene(vertical, (384, 832))
            create_scene(wide, (768, 432))
            create_cutout_with_low_alpha_halo(cutout)

            result = subprocess.run(
                [
                    sys.executable,
                    str(EXPORTER),
                    "--square",
                    str(square),
                    "--vertical",
                    str(vertical),
                    "--wide",
                    str(wide),
                    "--cutout",
                    str(cutout),
                    "--out",
                    str(output),
                    "--style",
                    "anime",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            manifest = json.loads((output / "pack-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["style"], "anime")
            self.assertEqual(len(manifest["outputs"]), 17)
            for item in manifest["outputs"]:
                with Image.open(output / item["file"]) as image:
                    self.assertEqual(image.size, (item["width"], item["height"]))

            with Image.open(output / "reusable/character-cutout.png") as image:
                alpha = image.convert("RGBA").getchannel("A")
                self.assertEqual(alpha.getpixel((0, 0)), 0)
                self.assertIsNotNone(alpha.getbbox())

            self.assertTrue((output / "contact-sheet.jpg").is_file())

    def test_unsafe_preset_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_value:
            temp = Path(temp_value)
            square = temp / "square.png"
            vertical = temp / "vertical.png"
            wide = temp / "wide.png"
            cutout = temp / "cutout.png"
            output = temp / "output"
            for path, size in ((square, (64, 64)), (vertical, (64, 128)), (wide, (128, 64))):
                create_scene(path, size)
            create_cutout_with_low_alpha_halo(cutout)

            unsafe = temp / "unsafe.json"
            unsafe.write_text(
                json.dumps(
                    {
                        "presets": [
                            {
                                "id": "probe",
                                "category": "../escaped",
                                "width": 64,
                                "height": 64,
                                "source": "square",
                                "operation": "cover",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(EXPORTER),
                    "--square",
                    str(square),
                    "--vertical",
                    str(vertical),
                    "--wide",
                    str(wide),
                    "--cutout",
                    str(cutout),
                    "--out",
                    str(output),
                    "--presets",
                    str(unsafe),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("safe lowercase path segment", result.stderr)
            self.assertFalse((temp / "escaped/probe.png").exists())


if __name__ == "__main__":
    unittest.main()
