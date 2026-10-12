# Soya Portrait Illustrator

[![Version](https://img.shields.io/badge/version-0.3.0-E76F51)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-264653)](LICENSE)

**Upload one photo, choose realistic hand-drawn or bean-eye anime style, and receive a reusable illustration system: avatars, phone wallpapers, social-post images, presentation layouts, and transparent character assets that still look like the same person.**

Soya Portrait Illustrator is an open-source Agent Skill for reference-image editing. Instead of regenerating the person for every format, it creates four likeness-approved masters and exports a consistent multi-size pack from them.

This public edition defaults to the complete asset pack when the requested quantity is ambiguous. A personalized local copy may use different defaults and is not part of this repository.

## Two styles

- **Realistic hand-drawn:** graphite or colored-pencil linework, restrained watercolor, paper texture, and an identity-preserving but aesthetically balanced smaller-head, roughly 4:6 upper-to-lower-body proportion.
- **Bean-eye anime:** small black bean eyes, minimal nose and mouth, black hand-drawn outlines, colored-pencil fill, and a cute flat two-dimensional silhouette without emphasized bust, waist, or hip curves.

Style and quantity are independent choices. When style is missing, the Skill asks the user to choose realistic hand-drawn or bean-eye anime. Both styles are produced only when explicitly requested.

The default identity target is approximately 80% recognizable with controlled light beautification, not photo-exact replication. When action is unspecified, the Skill selects a format-appropriate pose from its reusable pose library.

## Four masters

1. A square portrait for avatars and cards.
2. A tall composition with quiet clock and system-UI zones for wallpapers and vertical social posts.
3. A 16:9 composition with at least 40% negative space for presentation copy.
4. A transparent bust or figure for future layouts, stickers, posters, websites, and documents.

The skill never silently expands a headshot into an invented full body. A full-body cutout requires a sufficiently complete reference or explicit permission to infer missing clothing and anatomy.

## Default exports

The pack includes:

- 1024 and 512 square avatars, plus a circle-safe avatar.
- 1290×2796 iPhone-large, 1440×3120 Android-QHD, and 1080×2400 universal phone wallpapers.
- 1080×1080, 1080×1440, 1242×1660, and 1080×1920 social formats.
- 1920×1080 widescreen and 1600×1200 standard presentation images.
- A 2048 transparent character cutout, 1024 sticker, left-copy layout, right-copy layout, and 4:5 portrait card.
- A contact sheet and privacy-safe manifest.

These are durable project presets, not promises of permanent platform specifications. The system preserves high-resolution masters and ratio-aware safe areas so future sizes can be added without regenerating the person.

## Use cases

- **Avatar:** the circle-safe version protects hair, glasses, ears, and chin from platform cropping.
- **Phone wallpaper:** the subject stays clear of the clock, camera cutout, status area, and bottom controls.
- **WeChat Moments:** square and 3:4 variants support single images, grids, and portrait-led posts.
- **Xiaohongshu:** the high-resolution 3:4 version leaves room for a later headline while preserving a clean text-free master.
- **PowerPoint:** 16:9 and 4:3 sizes plus left/right character layouts support covers, profiles, quotes, sections, and closing slides.
- **Future formats:** the transparent cutout, sticker, and masters can be recomposed for websites, posters, long images, documents, and new platforms.

## Install

Copy the repository folder to:

```text
~/.codex/skills/soya-portrait-illustrator
```

`SKILL.md` must sit directly inside that folder. Restart or refresh Codex.

## Use

Attach an authorized photo and ask:

```text
Use $soya-portrait-illustrator to create a complete realistic hand-drawn asset pack from this photo. Preserve the face, expression, hairstyle, glasses, clothing colors, and pose. Export the avatar, phone wallpaper, social, presentation, cutout, sticker, and reusable layout presets.
```

## Exact-size export

```bash
python3 -m pip install -r requirements.txt
python3 scripts/export_asset_pack.py \
  --square master-square.png \
  --vertical master-vertical.png \
  --wide master-wide.png \
  --cutout master-cutout.png \
  --out portrait-asset-pack \
  --style realistic
```

The exporter reads `assets/presets.json`, creates every default size, and writes a contact sheet plus manifest.

## Privacy

Use only photos you own or are authorized to edit. Never submit identifiable user photos, generated likenesses, private image URLs, or personal prompt logs to issues or pull requests. Processing follows the terms of the image provider selected by the host environment; this repository does not claim local-only processing.

## Validate

```bash
python3 scripts/validate_skill.py .
```

Structural validation does not replace visual likeness testing with authorized reference photos.

## License

[MIT](LICENSE) © 2026 Soya
