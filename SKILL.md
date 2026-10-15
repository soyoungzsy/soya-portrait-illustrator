---
name: soya-portrait-illustrator
description: Build a reusable personal illustration library from authorized portrait masters. Prepare a sharing kit with avatar, editable title cover and transparent PPT illustration, save confirmed identity versions and palettes, and reuse them for later themes. Also supports the legacy four-master asset pack. Use for personal IP illustration workflows, not information graphics or automatic publishing.
---

# Soya Portrait Illustrator · Personal IP Library

用户上传照片后，只需说「按这张照片建立我的个人IP素材库」。主动检查宿主能力、补齐必要用途信息、确认人物并组织导出；不要让用户另外拼接长提示词或手动运行脚本。

Local Python helpers manage masters, versions, layout and checks. They do not generate images or guarantee likeness.

## Choose the scope

- A sharing session / personal IP library: avatar + sharing cover + transparent PPT illustration. Require only a square master and a transparent cutout.
- An explicit complete multi-size pack: use the existing four-master / 17-preset exporter. Read [asset-pack-presets](references/asset-pack-presets.md) and [composition rules](references/composition-variants.md).
- One requested image: deliver that image without expanding the scope.

## First sharing session

1. **Check host capabilities first.** Verify the available tool supports reference-image editing, can access the uploaded photo, can return a real alpha cutout, and can save outputs accessible to local Python. Check Python 3.9+ (3.10+ recommended) and Pillow with `python3 -c 'import PIL; print(PIL.__version__)'`. If capability is missing, explain the exact gap and prepare a brief; do not claim the full workflow ran. Ask before installing a missing dependency. The Skill bundles no model, API credentials, background removal service or generation entitlement. Before a newly paid call or photo upload, explain the data, provider and expected cost and obtain any missing authorization.
2. Obtain the authorized photo, intended use, topic/title and one point to express. Ask only for missing information. A normal, unretouched photo can be the reference: inspect visible face, hair, eyewear, outfit silhouette, layering, colors and accessories. Mirror reflections and dim light can obscure details; explain uncertainty rather than inventing them. Photos and local library files stay outside the public Skill source. Read [privacy and consent](references/privacy-and-consent.md) before processing a real person.
3. Ask realistic hand-drawn or bean-eye anime only if the choice is missing. Read the matching [realistic](references/realistic-handdrawn.md) or [anime](references/anime-bean-eye.md) reference. Inspect the photo before editing. Do not infer sensitive traits or hidden body details.
4. Generate text-free `square.png` and `cutout.png` through the available image-editing tool, using the original photo as reference in each new master call. Read [pose-library](references/pose-library.md) when changing actions. Preserve recognizable face, hairstyle, eyewear, clothing and accessories; no silent slimming, age shifts, skin-tone changes or sexualization. Any “80%” wording in style references is a qualitative preference, never a measured similarity guarantee.
5. Show the masters and obtain the user's confirmation before saving them as confirmed. Read [quality-check](references/quality-check.md). Confirm background, accent and text colors; use the default palette when the user has no preference. `--confirmed` records the agent's assertion of actual user approval; it does not obtain it.
6. Save and compose using [personal-library](references/personal-library.md). The agent runs these helpers; the user need not copy CLI commands. Copy `templates/share-brief.json` to a local work folder and fill the title and point. Use an alias rather than a legal name. Record only approved masters, never the original photo. New masters are re-encoded to remove metadata; unchanged stored masters are copied byte for byte.
7. Open `preview.html`: avatar at small circular sizes, cover with safe-area guide, cutout on light/dark/checkerboard backgrounds. Inspect title spelling, font rendering, portrait crop, stray generated lettering and alpha edges. Mechanical checks cannot assess likeness, read image lettering or certify background removal. Explain failed checks and correct their source before delivery.
8. Deliver `avatar.png`, editable `cover.svg` plus text-free `cover-background.png`, and `ppt-cutout.png`, alongside the preview and `kit-manifest.json`. The SVG contains editable text elements; it is not a PowerPoint text box. No PPTX is created. Export a raster cover only with an available renderer and report the format actually produced.

Use one writer per identity library; do not run `record` concurrently. Version-directory reservation is not a library-wide initialization lock.

## Reuse and local changes

- Ask which library/version only when it cannot be inferred. Reuse the explicit confirmed version for a new title/point; `build` does no generation and never modifies the library.
- Text-only change: edit the local brief and build into a new output directory. Avatar and cutout remain byte-identical for the same source version and environment.
- Palette-only change: `record --base v0001 --accent '#29A398' --confirmed` creates a child version; both masters retain their bytes. Use `--background` and `--text` as needed; low text/background contrast blocks a build.
- Pose, expression or clothing change: edit only the affected master through the image-editing tool. Provide the original photo and approved master as context where supported. Explicitly identify the allowed region and protected features, then inspect the result. Regional edits depend on the provider and may drift. Do not promise pixel preservation inside a regenerated image. After confirmation, record the changed role with `--base`; other master files are copied unchanged.
- Identity/style change: use a separate library. Versions are not overwritten. Builds verify master hashes and reject tampering, unknown schemas, invalid alpha and text overflow.

## Legacy full pack

The existing four-master and 17-size capability predates this library workflow. Follow [asset-pack-presets](references/asset-pack-presets.md) for square, vertical, wide and transparent masters. Keep at least 40% calm space in the wide scene, clock clearance in the vertical scene and circle clearance in the avatar. Confirm all four before running `scripts/export_asset_pack.py`; the exporter does not confirm likeness.

## Finish honestly

Report identity version, style/palette, delivered paths, machine checks, visual review performed and remaining issues. State whether a generation service was actually exercised. Never publish a real photo, likeness, private title or library without specific publication permission. This Skill does not register contests, submit entries, publish, or send messages automatically. See [competition checklist](references/competition-checklist.md) for a reviewable entry.
