#!/usr/bin/env python3
"""Build a deterministic installable Skill ZIP from an explicit source allowlist."""
import argparse
import hashlib
import os
import zipfile
from contextlib import ExitStack
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "soya-portrait-illustrator"
TOP = ("SOURCES.md", "MAINTENANCE.md", "OPEN_SOURCE_REVIEW.md", "VERSION", "SKILL.md", "README.md", "README.en.md", "LICENSE", "PRIVACY.md", "SECURITY.md", "CONTRIBUTING.md", "CHANGELOG.md", "requirements.txt")
# Additions to the public package require intentional review here.
FILES = TOP + (
    "references/github-actions.yml",
    "agents/openai.yaml", "assets/presets.json", "assets/portrait-illustrator-small.svg", "assets/portrait-illustrator.svg",
    "templates/share-brief.json", "scripts/ip_library.py", "scripts/export_asset_pack.py", "scripts/package_skill.py",
    "scripts/create_synthetic_demo.py", "scripts/validate_skill.py", "scripts/release_audit.py",
    "examples/requests.md", "examples/synthetic-showcase.svg",
    "references/anime-bean-eye.md", "references/asset-pack-presets.md", "references/composition-variants.md",
    "references/pose-library.md", "references/preset-sources.md", "references/privacy-and-consent.md",
    "references/quality-check.md", "references/realistic-handdrawn.md", "references/validation-notes.md",
    "references/personal-library.md", "references/competition-checklist.md",
    "tests/test_export_asset_pack.py", "tests/test_skill_contract.py", "tests/test_ip_library.py", "tests/test_package.py",
)


def package(out):
    out = Path(os.path.abspath(out))
    resolved = out.resolve()
    for candidate in (out, *out.parents, resolved, *resolved.parents):
        if candidate.resolve() == ROOT or (candidate.exists() and candidate.samefile(ROOT)):
            raise ValueError("write release packages outside the source directory")
    sidecar = out.with_suffix(out.suffix + ".sha256")
    for path in (out, sidecar):
        if path.exists() or path.is_symlink():
            raise ValueError(f"package or checksum path already exists: {path.name}")
    for name in FILES:
        path = ROOT / name
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"missing or symlinked package source: {name}")
    out.parent.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        with ExitStack() as stack:
            # O_EXCL creation via x modes rejects even dangling leaf symlinks
            # and protects both paths if another writer wins after preflight.
            archive_file = stack.enter_context(out.open("x+b"))
            created.append((out, os.fstat(archive_file.fileno())))
            checksum_file = stack.enter_context(sidecar.open("xb"))
            created.append((sidecar, os.fstat(checksum_file.fileno())))
            with zipfile.ZipFile(archive_file, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for name in sorted(FILES):
                    info = zipfile.ZipInfo(f"{NAME}/{name}", date_time=(2026, 10, 15, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    info.external_attr = 0o100644 << 16
                    archive.writestr(info, (ROOT / name).read_bytes())
            archive_file.seek(0)
            checksum = hashlib.sha256(archive_file.read()).hexdigest()
            checksum_file.write(f"{checksum}  {out.name}\n".encode())
    except Exception:
        for path, original_stat in reversed(created):
            try:
                current = path.lstat()
                if (current.st_dev, current.st_ino) == (original_stat.st_dev, original_stat.st_ino):
                    path.unlink()
            except FileNotFoundError:
                pass
        raise
    print(f"{checksum}  {out.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    try:
        package(parser.parse_args().out)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")
