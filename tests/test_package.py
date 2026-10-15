import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def invoke(self, path):
        return subprocess.run([sys.executable, str(ROOT / "scripts/package_skill.py"), "--out", str(path)], capture_output=True, text=True)

    def test_package_source_paths_and_filesystem_aliases_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "skill-source"
            (source / "scripts").mkdir(parents=True)
            script = source / "scripts/package_skill.py"
            shutil.copyfile(ROOT / "scripts/package_skill.py", script)
            outputs = [source / "skill.zip", source / "scripts/../skill.zip"]
            case_alias = source.with_name(source.name.upper())
            if case_alias.exists() and case_alias.samefile(source):
                outputs.append(case_alias / "skill.zip")
            for output in outputs:
                with self.subTest(output=output):
                    result = subprocess.run([sys.executable, str(script), "--out", str(output)], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("outside", result.stderr)
                    self.assertFalse(output.exists())

    def test_existing_checksum_is_unchanged_and_no_zip_created(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "skill.zip"
            checksum = output.with_suffix(".zip.sha256")
            checksum.write_bytes(b"existing checksum data")
            result = self.invoke(output)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertFalse(output.exists())
            self.assertEqual(checksum.read_bytes(), b"existing checksum data")

    def test_checksum_symlinks_never_modify_or_create_targets(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            for dangling in (False, True):
                with self.subTest(dangling=dangling):
                    output = folder / f"skill-{dangling}.zip"
                    target = folder / f"target-{dangling}"
                    if not dangling:
                        target.write_bytes(b"protected target")
                    checksum = output.with_suffix(".zip.sha256")
                    checksum.symlink_to(target)
                    result = self.invoke(output)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertFalse(output.exists())
                    self.assertTrue(checksum.is_symlink())
                    if dangling:
                        self.assertFalse(target.exists())
                    else:
                        self.assertEqual(target.read_bytes(), b"protected target")

    def test_zip_existing_file_and_symlinks_remain_unchanged(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            for kind in ("file", "symlink", "dangling"):
                with self.subTest(kind=kind):
                    output = folder / f"{kind}.zip"
                    target = folder / f"{kind}-target"
                    if kind == "file":
                        output.write_bytes(b"existing archive")
                    else:
                        if kind == "symlink":
                            target.write_bytes(b"existing target")
                        output.symlink_to(target)
                    result = self.invoke(output)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertFalse(output.with_suffix(".zip.sha256").exists())
                    if kind == "file":
                        self.assertEqual(output.read_bytes(), b"existing archive")
                    else:
                        self.assertTrue(output.is_symlink())
                        if kind == "symlink":
                            self.assertEqual(target.read_bytes(), b"existing target")
                        else:
                            self.assertFalse(target.exists())

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
