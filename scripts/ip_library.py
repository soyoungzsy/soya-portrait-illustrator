#!/usr/bin/env python3
"""Offline, versioned identity masters and a three-use sharing kit. No model calls."""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import re
import shutil
import sys
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw

from export_asset_pack import contain, load_rgba, normalize_cutout_alpha

VERSION = "0.4.0"
ROOT = Path(__file__).resolve().parents[1]
SEGMENT = re.compile(r"[a-z0-9][a-z0-9-]{0,63}\Z")
REVISION = re.compile(r"v[0-9]{4}\Z")
COLORS = ("background", "accent", "text")
DEFAULT_PALETTE = {"background": "#FFF8EE", "accent": "#E76F51", "text": "#264653"}


def read_json(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("JSON must be an object")
    return data


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def outside_source(path):
    path = Path(path).resolve()
    if path == ROOT or ROOT in path.parents:
        raise ValueError("personal library and outputs must be outside the Skill source directory")
    return path


def palette_value(value):
    if not isinstance(value, str) or not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        raise ValueError("palette colors must be #RRGGBB")
    return value.upper()


def cutout_check(image):
    alpha = image.getchannel("A")
    if alpha.getextrema() != (0, 255):
        raise ValueError("cutout needs fully transparent background and visible opaque pixels")
    if any(alpha.getpixel(p) for p in ((0, 0), (image.width-1, 0), (0, image.height-1), (image.width-1, image.height-1))):
        raise ValueError("cutout corners must be transparent; painted checkerboards are not alpha")


def load_version(library, version):
    if not REVISION.fullmatch(version):
        raise ValueError("version must have form v0001")
    folder = library / "versions" / version
    if folder.is_symlink() or folder.resolve().parent != (library / "versions").resolve():
        raise ValueError("version directory escapes library")
    data = read_json(folder / "identity.json")
    if data.get("schema_version") != "1.0" or data.get("version") != version or data.get("confirmed") is not True:
        raise ValueError("unsupported or unconfirmed identity manifest")
    if not SEGMENT.fullmatch(data.get("identity_id", "")) or data.get("style") not in ("realistic", "anime", "custom"):
        raise ValueError("invalid identity metadata")
    if data.get("provenance") not in ("synthetic", "authorized-master"):
        raise ValueError("invalid provenance")
    for key in COLORS:
        palette_value(data["palette"][key])
    for role in ("square", "cutout"):
        item = data["masters"][role]
        path = folder / f"{role}.png"
        if item["file"] != path.name or path.is_symlink() or digest(path) != item["sha256"]:
            raise ValueError(f"master integrity failed: {role}; restore it or create a new confirmed version")
    return folder, data


def record(args):
    library = outside_source(args.library)
    if library.is_symlink() or (library / "versions").is_symlink():
        raise ValueError("library directories must not be symlinks")
    previous_folder, previous = load_version(library, args.base) if args.base else (None, None)
    if previous is None and (library / "versions").exists() and any((library / "versions").iterdir()):
        raise ValueError("library already has versions; use --base to preserve identity lineage")
    if previous is None and (not args.identity_id or not args.square or not args.cutout or not args.style):
        raise ValueError("first version requires --identity-id, --style, --square and --cutout")
    if previous is not None and any((args.identity_id, args.style, args.synthetic)):
        raise ValueError("revision inherits identity, style and provenance; create a separate library to change them")
    identity_id = previous["identity_id"] if previous else args.identity_id
    if not SEGMENT.fullmatch(identity_id):
        raise ValueError("identity-id must be a short lowercase alias, not a personal name or path")
    if not args.confirmed:
        raise ValueError("record only after user approval, then pass --confirmed")
    palette = dict(previous["palette"] if previous else DEFAULT_PALETTE)
    for key in COLORS:
        if getattr(args, key):
            palette[key] = palette_value(getattr(args, key))
    images = {}
    for role in ("square", "cutout"):
        source = getattr(args, role)
        if source:
            images[role] = load_rgba(source)
            if role == "square" and images[role].width != images[role].height:
                raise ValueError("square master must be 1:1")
            if role == "cutout":
                images[role] = normalize_cutout_alpha(images[role], 16)
                cutout_check(images[role])
    versions = library / "versions"
    versions.mkdir(parents=True, exist_ok=True)
    # A reservation directory prevents two writers from allocating the same version.
    for index in range(1, 10000):
        version = f"v{index:04d}"
        target = versions / version
        try:
            target.mkdir()
            break
        except FileExistsError:
            continue
    else:
        raise ValueError("version limit reached")
    try:
        masters = {}
        for role in ("square", "cutout"):
            path = target / f"{role}.png"
            if role in images:
                # New image without EXIF, PNG text, ICC, or original file paths.
                clean = Image.new("RGBA", images[role].size)
                clean.paste(images[role])
                clean.save(path)
            else:
                shutil.copyfile(previous_folder / f"{role}.png", path)
            with Image.open(path) as image:
                masters[role] = {"file": path.name, "sha256": digest(path), "size": list(image.size)}
        data = {"schema_version": "1.0", "project_version": VERSION, "identity_id": identity_id,
                "version": version, "parent_version": args.base, "confirmed": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "style": previous["style"] if previous else args.style,
                "provenance": previous["provenance"] if previous else ("synthetic" if args.synthetic else "authorized-master"),
                "palette": palette, "masters": masters,
                "changed": [role for role in ("square", "cutout") if role in images] +
                           [key for key in COLORS if getattr(args, key)]}
        write_json(target / "identity.json", data)
    except Exception:
        shutil.rmtree(target)
        raise
    print(f"Recorded {version}; unchanged masters preserved byte for byte")


def lines(value, width, max_lines):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("title and point must be non-empty text")
    if any(unicodedata.category(char).startswith("C") for char in value):
        raise ValueError("text must not contain control or hidden formatting characters")
    result, line, used = [], "", 0
    for char in value.strip():
        units = 1 if unicodedata.east_asian_width(char) in ("W", "F") else 0.62
        if used + units > width:
            result.append(line)
            line, used = "", 0
        line += char
        used += units
    result.append(line)
    if len(result) > max_lines:
        raise ValueError(f"text exceeds safe text area ({max_lines} lines); shorten it, never silently truncate")
    return result


def svg_text(text_lines, x, y, font_size, color):
    spans = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else font_size * 1.3:g}">{html.escape(line)}</tspan>' for i, line in enumerate(text_lines))
    return f'<text x="{x}" y="{y}" font-size="{font_size}" fill="{color}" font-family="system-ui, sans-serif">{spans}</text>'


def preview_document(title, point):
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sharing kit preview</title><style>
body{{font:16px system-ui,sans-serif;background:#f1f0ec;color:#263e48;margin:0;padding:32px;max-width:1120px}}
h1{{font-size:32px}}section{{margin:32px 0;background:white;padding:24px;border-radius:16px}}img{{max-width:100%}}
.avatars{{display:flex;gap:30px;align-items:center}}.avatars img{{border-radius:50%}}.cover{{position:relative}}
.guide{{position:absolute;inset:7.1% 4%;border:2px dashed #ce4f26;pointer-events:none}}
.surfaces{{display:flex;gap:16px;flex-wrap:wrap}}.surface{{width:29%;min-width:180px;border:1px solid #bbb}}
.surface img{{width:100%;display:block}}.dark{{background:#172732}}.checker{{background:conic-gradient(#ddd 25%,white 0 50%,#ddd 0 75%,white 0) 0 0/24px 24px}}
p{{line-height:1.6}}a{{color:#8a351d}}</style>
<h1>{html.escape(title)}</h1><p>{html.escape(point)}</p><p>Offline layout preview · synthetic demo only when provenance says synthetic. Dashed line: safe area.</p>
<section><h2>Avatar · actual circle crops</h2><div class="avatars"><img src="avatar.png" width="48" height="48" alt="48 pixel avatar"><img src="avatar.png" width="96" height="96" alt="96 pixel avatar"><img src="avatar.png" width="192" height="192" alt="192 pixel avatar"></div><p>Check face, hair and accessories at small sizes. Circle cropping still needs human review.</p></section>
<section><h2>Sharing cover · 1920 × 1080</h2><div class="cover"><img src="cover.svg" alt="Sharing cover"><div class="guide"></div></div><p><a href="cover.svg">Editable SVG text</a> · edit title and point in brief.json, then rebuild into a new output folder. Verify fonts and line wrapping on the target device.</p></section>
<section><h2>PPT illustration · light / dark / alpha checkerboard</h2><div class="surfaces"><div class="surface"><img src="ppt-cutout.png" alt="Light background"></div><div class="surface dark"><img src="ppt-cutout.png" alt="Dark background"></div><div class="surface checker"><img src="ppt-cutout.png" alt="Alpha checkerboard"></div></div><p>Insert ppt-cutout.png into PowerPoint. Check edge halos, missing details and solid background residue.</p></section>
<p>See kit-manifest.json for hashes and machine checks. Identity, stray lettering in masters and visual quality require human review; no model or OCR was run.</p></html>'''


def build(args):
    library, output = outside_source(args.library), outside_source(args.out)
    if output.exists():
        raise ValueError("output already exists; select a new folder to preserve previous deliveries")
    if library == output or library in output.parents or output in library.parents:
        raise ValueError("delivery and identity library must be separate directories")
    folder, identity = load_version(library, args.version)
    brief = read_json(args.brief)
    if brief.get("schema_version") != "1.0":
        raise ValueError("unsupported brief schema_version")
    title_lines = lines(brief.get("title"), 10, 3)
    point_lines = lines(brief.get("point"), 17, 4)
    palette = identity["palette"]
    def luminance(color):
        values = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
        values = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in values]
        return sum(v * w for v, w in zip(values, (0.2126, 0.7152, 0.0722)))
    low, high = sorted((luminance(palette["text"]), luminance(palette["background"])))
    if (high + 0.05) / (low + 0.05) < 4.5:
        raise ValueError("text/background contrast below 4.5:1; record a version with a clearer palette")
    square, cutout = load_rgba(folder / "square.png"), load_rgba(folder / "cutout.png")
    cutout_check(cutout)
    # Render in a sibling temporary directory; failed jobs never look complete.
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".ip-kit-", dir=output.parent))
    try:
        avatar = square.resize((1024, 1024), Image.Resampling.LANCZOS)
        avatar.save(stage / "avatar.png")
        ppt = contain(cutout, (1600, 1600), scale=0.88)
        ppt.save(stage / "ppt-cutout.png")
        cutout_check(ppt)
        background = Image.new("RGBA", (1920, 1080), palette["background"])
        draw = ImageDraw.Draw(background)
        draw.rounded_rectangle((80, 80, 180, 94), radius=7, fill=palette["accent"])
        person = contain(cutout, (800, 900), scale=0.94)
        background.alpha_composite(person, (1040, 90))
        background.save(stage / "cover-background.png")
        encoded = base64.b64encode((stage / "cover-background.png").read_bytes()).decode()
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">'
               f'<image width="1920" height="1080" href="data:image/png;base64,{encoded}"/>' +
               svg_text(title_lines, 120, 290, 80, palette["text"]) +
               svg_text(point_lines, 120, 700, 44, palette["text"]) + '</svg>')
        (stage / "cover.svg").write_text(svg, encoding="utf-8")
        write_json(stage / "brief.json", {"schema_version": "1.0", "title": brief["title"], "point": brief["point"]})
        (stage / "preview.html").write_text(preview_document(brief["title"], brief["point"]), encoding="utf-8")
        files = [{"file": name, "sha256": digest(stage / name)} for name in
                 ("avatar.png", "cover.svg", "cover-background.png", "ppt-cutout.png", "brief.json", "preview.html")]
        manifest = {"schema_version": "1.0", "project_version": VERSION,
                    "identity_id": identity["identity_id"], "identity_version": args.version,
                    "provenance": identity["provenance"], "master_hashes": identity["masters"],
                    "palette": palette, "outputs": files,
                    "layout": {"cover_size": [1920, 1080], "safe_rect": [80, 80, 1840, 1000],
                               "title_rect": [120, 180, 940, 530], "point_rect": [120, 640, 940, 910],
                               "person_rect": [1040, 90, 1840, 990]},
                    "checks": {"master_hashes": "passed", "ppt_alpha": "passed", "text_capacity": "passed",
                               "dimensions": {"avatar.png": [1024, 1024], "ppt-cutout.png": [1600, 1600], "cover-background.png": [1920, 1080]},
                               "visual_review": "required: circle crop, font rendering, likeness, stray text and alpha edges",
                               "generation": "external; not performed by this script", "ocr": "not performed"}}
        write_json(stage / "kit-manifest.json", manifest)
        stage.rename(output)
    except Exception:
        shutil.rmtree(stage)
        raise
    print(f"Created three-use kit: {output / 'preview.html'}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    rec = sub.add_parser("record", help="Create an immutable confirmed version, optionally based on an earlier version")
    rec.add_argument("--library", type=Path, required=True)
    rec.add_argument("--base")
    rec.add_argument("--identity-id")
    rec.add_argument("--style", choices=("realistic", "anime", "custom"))
    rec.add_argument("--square", type=Path)
    rec.add_argument("--cutout", type=Path)
    rec.add_argument("--confirmed", action="store_true")
    rec.add_argument("--synthetic", action="store_true", help="Only when masters are synthetic and contain no real identity")
    for key in COLORS:
        rec.add_argument(f"--{key}")
    kit = sub.add_parser("build", help="Reuse one explicit identity version for avatar, editable cover and PPT cutout")
    kit.add_argument("--library", type=Path, required=True)
    kit.add_argument("--version", required=True)
    kit.add_argument("--brief", type=Path, required=True)
    kit.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        (record if args.command == "record" else build)(args)
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
