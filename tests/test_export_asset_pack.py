import json
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
