#!/usr/bin/env python3
"""Export an exact-size portrait illustration pack from four approved masters."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont, ImageOps


RESAMPLE = Image.Resampling.LANCZOS
VALID_SOURCES = {"square", "vertical", "wide", "cutout"}
VALID_OPERATIONS = {
    "cover",
    "circle_safe",
    "contain_transparent",
    "sticker",
    "compose_left",
    "compose_right",
}
SAFE_SEGMENT = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Create avatar, wallpaper, social, presentation, and reusable portrait assets."
    )
    parser.add_argument("--square", required=True, type=Path, help="Approved 1:1 portrait master")
    parser.add_argument("--vertical", required=True, type=Path, help="Approved tall portrait master")
    parser.add_argument("--wide", required=True, type=Path, help="Approved 16:9 portrait master")
    parser.add_argument("--cutout", required=True, type=Path, help="Approved transparent person cutout")
    parser.add_argument("--out", required=True, type=Path, help="New output directory")
    parser.add_argument(
        "--presets",
        type=Path,
        default=root / "assets" / "presets.json",
        help="Machine-readable preset file",
    )
    parser.add_argument(
        "--style",
        choices=("realistic", "anime", "custom"),
        default="realistic",
        help="Style label stored in the manifest",
    )
    parser.add_argument("--background", default="#FFF8EE", help="Solid layout background color")
    parser.add_argument("--accent", default="#E76F51", help="Abstract layout accent color")
    parser.add_argument("--focus-x", type=float, default=0.5, help="Horizontal crop focus from 0 to 1")
    parser.add_argument("--focus-y", type=float, default=0.42, help="Vertical crop focus from 0 to 1")
    parser.add_argument(
        "--alpha-threshold",
        type=int,
        default=16,
        help="Set cutout alpha values below this 0-255 threshold to fully transparent",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting files inside an existing non-empty output directory",
    )
    return parser.parse_args()


def load_rgba(path: Path) -> Image.Image:
    if not path.is_file():
        raise ValueError(f"input does not exist: {path}")
    with Image.open(path) as image:
        return ImageOps.exif_transpose(image).convert("RGBA")


def validate_cutout(image: Image.Image) -> None:
    alpha = image.getchannel("A")
    minimum, maximum = alpha.getextrema()
    if minimum == maximum == 255:
        raise ValueError("--cutout must contain transparency; received a fully opaque image")


def normalize_cutout_alpha(image: Image.Image, threshold: int) -> Image.Image:
    if not 0 <= threshold <= 255:
        raise ValueError("--alpha-threshold must be between 0 and 255")
    if threshold == 0:
        return image
    normalized = image.copy()
    alpha = normalized.getchannel("A").point(lambda value: 0 if value < threshold else value)
    normalized.putalpha(alpha)
    return normalized


def rgba_color(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    red, green, blue = ImageColor.getrgb(value)
    return red, green, blue, alpha


def cover(image: Image.Image, size: tuple[int, int], focus: tuple[float, float]) -> Image.Image:
    return ImageOps.fit(image, size, method=RESAMPLE, centering=focus)


def trim_transparency(image: Image.Image) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if not bbox:
        raise ValueError("transparent master has no visible pixels")
    return image.crop(bbox)


def contain(
    image: Image.Image,
    size: tuple[int, int],
    *,
    scale: float = 0.9,
    background: tuple[int, int, int, int] = (0, 0, 0, 0),
) -> Image.Image:
    canvas = Image.new("RGBA", size, background)
    source = trim_transparency(image)
    max_size = (max(1, int(size[0] * scale)), max(1, int(size[1] * scale)))
    source.thumbnail(max_size, RESAMPLE)
    x = (size[0] - source.width) // 2
    y = (size[1] - source.height) // 2
    canvas.alpha_composite(source, (x, y))
    return canvas


def circle_safe(
    image: Image.Image,
    size: tuple[int, int],
    focus: tuple[float, float],
) -> Image.Image:
    background = cover(image, size, focus).filter(ImageFilter.GaussianBlur(max(12, size[0] // 28)))
    inset_size = (int(size[0] * 0.84), int(size[1] * 0.84))
    foreground = cover(image, inset_size, focus)
    x = (size[0] - foreground.width) // 2
    y = (size[1] - foreground.height) // 2
    background.alpha_composite(foreground, (x, y))
    return background


def sticker(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    foreground = contain(image, size, scale=0.76)
    alpha = foreground.getchannel("A")
    radius = max(7, (min(size) // 64) | 1)
    outline_mask = alpha.filter(ImageFilter.MaxFilter(radius))
    shadow_mask = outline_mask.filter(ImageFilter.GaussianBlur(max(2, min(size) // 160)))

    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    shadow = Image.new("RGBA", size, (38, 70, 83, 72))
    shadow_offset = max(4, min(size) // 128)
    shifted_shadow = Image.new("L", size, 0)
    shifted_shadow.paste(shadow_mask, (shadow_offset, shadow_offset))
    canvas.alpha_composite(Image.composite(shadow, Image.new("RGBA", size), shifted_shadow))

    outline = Image.new("RGBA", size, (255, 255, 255, 255))
    canvas.alpha_composite(Image.composite(outline, Image.new("RGBA", size), outline_mask))
    canvas.alpha_composite(foreground)
    return canvas


def compose_layout(
    image: Image.Image,
    size: tuple[int, int],
    *,
    side: str,
    background: tuple[int, int, int, int],
    accent: tuple[int, int, int, int],
) -> Image.Image:
    canvas = Image.new("RGBA", size, background)
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    circle_size = int(min(size) * 0.64)
    circle_y = int(size[1] * 0.17)
    if side == "left":
        circle_x = int(size[0] * 0.03)
    else:
        circle_x = size[0] - circle_size - int(size[0] * 0.03)
    draw.ellipse(
        (circle_x, circle_y, circle_x + circle_size, circle_y + circle_size),
        fill=(accent[0], accent[1], accent[2], 42),
        outline=(accent[0], accent[1], accent[2], 120),
        width=max(3, size[0] // 420),
    )
    canvas.alpha_composite(overlay)

    source = trim_transparency(image)
    source.thumbnail((int(size[0] * 0.47), int(size[1] * 0.9)), RESAMPLE)
    margin = int(size[0] * 0.035)
    x = margin if side == "left" else size[0] - source.width - margin
    y = size[1] - source.height
    canvas.alpha_composite(source, (x, y))
    return canvas


def load_presets(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"preset file does not exist: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    presets = data.get("presets")
    if not isinstance(presets, list) or not presets:
        raise ValueError("preset file must contain a non-empty presets list")

    seen: set[str] = set()
    for preset in presets:
        preset_id = preset.get("id")
        if not isinstance(preset_id, str) or not preset_id:
            raise ValueError("every preset needs a non-empty string id")
        if not SAFE_SEGMENT.fullmatch(preset_id):
            raise ValueError(f"preset id must use lowercase letters, digits, and hyphens: {preset_id!r}")
        if preset_id in seen:
            raise ValueError(f"duplicate preset id: {preset_id}")
        seen.add(preset_id)
        category = preset.get("category")
        if not isinstance(category, str) or not SAFE_SEGMENT.fullmatch(category):
            raise ValueError(
                f"category for {preset_id} must be one safe lowercase path segment: {category!r}"
            )
        if preset.get("source") not in VALID_SOURCES:
            raise ValueError(f"invalid source for {preset_id}: {preset.get('source')}")
        if preset.get("operation") not in VALID_OPERATIONS:
            raise ValueError(f"invalid operation for {preset_id}: {preset.get('operation')}")
        if not isinstance(preset.get("width"), int) or preset["width"] <= 0:
            raise ValueError(f"invalid width for {preset_id}")
        if not isinstance(preset.get("height"), int) or preset["height"] <= 0:
            raise ValueError(f"invalid height for {preset_id}")
    return data


def render_preset(
    preset: dict[str, Any],
    sources: dict[str, Image.Image],
    focus: tuple[float, float],
    background: tuple[int, int, int, int],
    accent: tuple[int, int, int, int],
) -> Image.Image:
    image = sources[preset["source"]]
    size = (preset["width"], preset["height"])
    operation = preset["operation"]

    if operation == "cover":
        return cover(image, size, focus)
    if operation == "circle_safe":
        return circle_safe(image, size, focus)
    if operation == "contain_transparent":
        return contain(image, size, scale=0.92)
    if operation == "sticker":
        return sticker(image, size)
    if operation == "compose_left":
        return compose_layout(image, size, side="left", background=background, accent=accent)
    if operation == "compose_right":
        return compose_layout(image, size, side="right", background=background, accent=accent)
    raise ValueError(f"unsupported operation: {operation}")


def make_contact_sheet(items: list[tuple[str, Image.Image]], path: Path) -> None:
    columns = 4
    cell_width = 340
    cell_height = 250
    rows = math.ceil(len(items) / columns)
    sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), (247, 244, 238))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for index, (label, image) in enumerate(items):
        column = index % columns
        row = index // columns
        x = column * cell_width
        y = row * cell_height
        preview = image.convert("RGBA")
        preview.thumbnail((cell_width - 28, cell_height - 48), RESAMPLE)
        preview_bg = Image.new("RGBA", preview.size, (255, 255, 255, 255))
        preview_bg.alpha_composite(preview)
        px = x + (cell_width - preview.width) // 2
        py = y + 12 + (cell_height - 48 - preview.height) // 2
        sheet.paste(preview_bg.convert("RGB"), (px, py))
        draw.text((x + 12, y + cell_height - 28), label, fill=(38, 70, 83), font=font)

    sheet.save(path, quality=92, optimize=True)


def main() -> int:
    args = parse_args()
    if not 0 <= args.focus_x <= 1 or not 0 <= args.focus_y <= 1:
        print("error: --focus-x and --focus-y must be between 0 and 1", file=sys.stderr)
        return 2
    if not 0 <= args.alpha_threshold <= 255:
        print("error: --alpha-threshold must be between 0 and 255", file=sys.stderr)
        return 2

    output = args.out.resolve()
    if output.exists() and any(output.iterdir()) and not args.overwrite:
        print(f"error: output directory is not empty: {output}; use --overwrite to proceed", file=sys.stderr)
        return 2
    output.mkdir(parents=True, exist_ok=True)

    try:
        sources = {
            "square": load_rgba(args.square),
            "vertical": load_rgba(args.vertical),
            "wide": load_rgba(args.wide),
            "cutout": load_rgba(args.cutout),
        }
        validate_cutout(sources["cutout"])
        sources["cutout"] = normalize_cutout_alpha(sources["cutout"], args.alpha_threshold)
        preset_data = load_presets(args.presets)
        background = rgba_color(args.background)
        accent = rgba_color(args.accent)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    manifest_outputs: list[dict[str, Any]] = []
    contact_items: list[tuple[str, Image.Image]] = []
    focus = (args.focus_x, args.focus_y)

    for preset in preset_data["presets"]:
        rendered = render_preset(preset, sources, focus, background, accent)
        category_dir = output / preset["category"]
        category_dir.mkdir(parents=True, exist_ok=True)
        relative = Path(preset["category"]) / f"{preset['id']}.png"
        target = (output / relative).resolve()
        try:
            target.relative_to(output)
        except ValueError as exc:
            raise ValueError(f"preset output escapes the selected output directory: {relative}") from exc
        rendered.save(target, optimize=True)
        contact_items.append((preset["id"], rendered.copy()))
        manifest_outputs.append(
            {
                "id": preset["id"],
                "category": preset["category"],
                "file": relative.as_posix(),
                "width": preset["width"],
                "height": preset["height"],
                "source": preset["source"],
                "operation": preset["operation"],
            }
        )

    make_contact_sheet(contact_items, output / "contact-sheet.jpg")
    manifest = {
        "schema_version": "1.0",
        "project_version": preset_data.get("project_version", "unknown"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "style": args.style,
        "sources": ["square", "vertical", "wide", "cutout"],
        "outputs": manifest_outputs,
    }
    (output / "pack-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Created {len(manifest_outputs)} assets in {output}")
    print(f"Contact sheet: {output / 'contact-sheet.jpg'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
