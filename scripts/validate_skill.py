#!/usr/bin/env python3
"""Validate the public repository without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SKILL_NAME = "soya-portrait-illustrator"
REQUIRED_FILES = (
    "SKILL.md",
    "README.md",
    "README.en.md",
    "LICENSE",
    "PRIVACY.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "agents/openai.yaml",
    "references/realistic-handdrawn.md",
    "references/anime-bean-eye.md",
    "references/asset-pack-presets.md",
    "references/composition-variants.md",
    "references/pose-library.md",
    "references/quality-check.md",
    "references/privacy-and-consent.md",
    "references/preset-sources.md",
    "references/validation-notes.md",
    "examples/requests.md",
    "assets/presets.json",
    "assets/portrait-illustrator-small.svg",
    "assets/portrait-illustrator.svg",
    "scripts/export_asset_pack.py",
    "tests/test_export_asset_pack.py",
    "tests/test_skill_contract.py",
    "references/github-actions.yml",
    "requirements.txt",
    "templates/share-brief.json",
    "scripts/ip_library.py",
    "scripts/create_synthetic_demo.py",
    "scripts/package_skill.py",
    "scripts/release_audit.py",
    "references/personal-library.md",
    "references/competition-checklist.md",
    "tests/test_ip_library.py",
    "tests/test_package.py",
    "examples/synthetic-showcase.svg",
)

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".py", ".txt"}
PRIVATE_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".avif"}
UNFINISHED_MARKERS = ("TODO", "FIXME", "TBD", "[MAIN SUBJECT]")
SAFE_SEGMENT = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"not valid UTF-8: {path}") from exc


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill = read_text(skill_path)
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, re.DOTALL)
        if not frontmatter:
            errors.append("SKILL.md has no valid YAML frontmatter block")
        else:
            header = frontmatter.group(1)
            name_match = re.search(r"^name:\s*([^\n]+)$", header, re.MULTILINE)
            desc_match = re.search(r"^description:\s*(.+)$", header, re.MULTILINE)
            if not name_match or name_match.group(1).strip(' "\'') != SKILL_NAME:
                errors.append(f"SKILL.md name must be {SKILL_NAME}")
            if not desc_match or len(desc_match.group(1).strip(' "\'')) < 40:
                errors.append("SKILL.md description is missing or not discriminating enough")

    yaml_path = root / "agents/openai.yaml"
    if yaml_path.is_file():
        yaml_text = read_text(yaml_path)
        short_match = re.search(r'^\s*short_description:\s*"([^"]+)"', yaml_text, re.MULTILINE)
        if not short_match:
            errors.append("openai.yaml is missing quoted short_description")
        elif not 25 <= len(short_match.group(1)) <= 64:
            errors.append("openai.yaml short_description must be 25-64 characters")
        if f"${SKILL_NAME}" not in yaml_text:
            errors.append(f"openai.yaml default_prompt must mention ${SKILL_NAME}")

    presets_path = root / "assets/presets.json"
    if presets_path.is_file():
        try:
            preset_data = json.loads(read_text(presets_path))
            presets = preset_data.get("presets", [])
            if not isinstance(presets, list) or not presets:
                errors.append("assets/presets.json must contain a non-empty presets list")
            else:
                ids = [preset.get("id") for preset in presets if isinstance(preset, dict)]
                if len(ids) != len(presets) or any(not value for value in ids):
                    errors.append("every export preset must have a non-empty id")
                if len(set(ids)) != len(ids):
                    errors.append("export preset ids must be unique")
                for preset in presets:
                    if not isinstance(preset, dict):
                        continue
                    preset_id = preset.get("id", "unknown")
                    if not isinstance(preset_id, str) or not SAFE_SEGMENT.fullmatch(preset_id):
                        errors.append(f"preset id is not a safe path segment: {preset_id!r}")
                    category = preset.get("category")
                    if not isinstance(category, str) or not SAFE_SEGMENT.fullmatch(category):
                        errors.append(f"preset {preset_id} has unsafe category: {category!r}")
                    for field in ("width", "height"):
                        value = preset.get(field)
                        if not isinstance(value, int) or value <= 0:
                            errors.append(f"preset {preset_id} has invalid {field}")
        except json.JSONDecodeError as exc:
            errors.append(f"assets/presets.json is invalid JSON: {exc}")

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if relative == Path("scripts/validate_skill.py"):
            continue
        if any(part.startswith(".") and part not in {".gitignore"} for part in relative.parts):
            continue
        if path.suffix.lower() in PRIVATE_IMAGE_SUFFIXES:
            errors.append(f"unexpected raster image; verify consent before committing: {relative}")
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"LICENSE", ".gitignore"}:
            text = read_text(path)
            for marker in UNFINISHED_MARKERS:
                if marker in text:
                    errors.append(f"unfinished marker {marker!r} in {relative}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK: {SKILL_NAME} repository structure and metadata are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
