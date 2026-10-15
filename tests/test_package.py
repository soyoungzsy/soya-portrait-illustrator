import hashlib
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_reproducible_archive_and_installed_offline_workflow(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            packages = [folder / name for name in ("one.zip", "two.zip")]
            for path in packages:
                subprocess.run([sys.executable, str(ROOT / "scripts/package_skill.py"), "--out", str(path)], check=True, capture_output=True)
            self.assertEqual(hashlib.sha256(packages[0].read_bytes()).digest(), hashlib.sha256(packages[1].read_bytes()).digest())
            with zipfile.ZipFile(packages[0]) as archive:
                names = archive.namelist()
                self.assertTrue(all(name.startswith("soya-portrait-illustrator/") for name in names))
                self.assertFalse(any(part in name.split("/") for part in (".git", "private-photos", "library", "__pycache__") for name in names))
                archive.extractall(folder / "install")
            installed = folder / "install/soya-portrait-illustrator"
            validation = subprocess.run([sys.executable, "scripts/validate_skill.py", "."], cwd=installed, capture_output=True, text=True)
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            run = subprocess.run([sys.executable, "scripts/create_synthetic_demo.py", "--out", str(folder / "demo")], cwd=installed, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            self.assertTrue((folder / "demo/next-share/preview.html").is_file())


if __name__ == "__main__":
    unittest.main()
