# Asset-pack presets

The default pack turns four likeness-approved masters into exact-size derivatives. Dimensions are working presets chosen for practical reuse; platform requirements may change.

## Required masters

| Role | Suggested ratio | What it must contain |
|---|---:|---|
| `square` | 1:1 | Recognizable head-and-shoulders or half-body portrait with crop margin |
| `vertical` | about 9:19.5 | Tall scene with quiet top and bottom UI zones |
| `wide` | 16:9 | Landscape scene with at least 40% negative space |
| `cutout` | transparent | Bust, half-body, or full body matching what the source can support |

Every master must be generated from the original photo, not only from another generated master.

## Default exports

| ID | Size | Source | Operation | Use |
|---|---:|---|---|---|
| `avatar-square-1024` | 1024×1024 | square | cover | High-resolution profile image |
| `avatar-circle-safe-1024` | 1024×1024 | square | circle-safe inset | Circular platform crops |
| `avatar-small-512` | 512×512 | square | cover | Lightweight app/contact avatar |
| `phone-wallpaper-ios-large` | 1290×2796 | vertical | cover | Large iPhone working preset |
| `phone-wallpaper-android-qhd` | 1440×3120 | vertical | cover | QHD Android working preset |
| `phone-wallpaper-universal` | 1080×2400 | vertical | cover | General 20:9 phone crop |
| `moments-square` | 1080×1080 | square | cover | Moments single image or grid source |
| `social-portrait` | 1080×1440 | vertical | cover | General 3:4 social portrait |
| `xiaohongshu-portrait` | 1242×1660 | vertical | cover | High-resolution 3:4 working preset |
| `social-story` | 1080×1920 | vertical | cover | 9:16 vertical content |
| `ppt-wide` | 1920×1080 | wide | cover | 16:9 presentation or video frame |
| `ppt-standard` | 1600×1200 | cutout | compose right | 4:3 presentation without cropping the person |
| `character-cutout` | 2048×2048 | cutout | contain on transparency | Reusable person asset |
| `character-sticker` | 1024×1024 | cutout | white outline | Sticker and social decoration |
| `layout-person-left` | 1920×1080 | cutout | compose left | Copy area on the right |
| `layout-person-right` | 1920×1080 | cutout | compose right | Copy area on the left |
| `portrait-card-4x5` | 1600×2000 | vertical | cover | Poster, card, and future social use |

The machine-readable source is [../assets/presets.json](../assets/presets.json). Modify that file to add or retire sizes without duplicating the list inside the exporter.

## Export policy

- Preserve the original master files alongside the pack.
- The exporter sets alpha values below 16 to transparent by default so low-opacity generation halos do not expand cutout bounds; use `--alpha-threshold 0` only when that behavior is intentionally disabled.
- Export lossless PNG by default. Convert copies to JPEG or WebP only for a known downstream limit.
- Do not upscale a visibly soft face and call it high resolution. Pixel size and facial detail are different qualities.
- Do not include crop guides in final images. Use separate guide overlays if a downstream workflow needs them.
- Keep filenames free of the person’s real name unless the user explicitly wants it.
