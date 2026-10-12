---
name: soya-portrait-illustrator
description: Turn an uploaded human photo into a reusable illustration asset pack in either realistic hand-drawn or bean-eye anime style, including avatars, phone wallpapers, social-post images, presentation layouts, transparent cutouts, and future-ready composition variants. Use for photo-to-illustration and multi-size portrait asset requests; do not use for text-only character invention or information graphics.
---

# Soya Portrait Illustrator

Turn one authorized reference photo into a coherent family of illustrations that still looks like the same person across formats. Treat likeness as the invariant and format as the variable.

## Choose the deliverable

- If the user asks for “一套素材”“全套”“多尺寸”“头像 + 屏保 + 社交图”“asset pack”, create the **default asset pack** below.
- If the user asks for one specific image, create only that image; do not force the full pack.
- In this public GitHub edition, if the request is ambiguous but clearly about turning a photo into an illustration, default to the complete realistic hand-drawn asset pack. Create only one image when the user explicitly narrows the request to one image or one format.

## Choose a style separately from quantity

- **Realistic hand-drawn** applies when the user says “写实”“写实手绘”“彩铅肖像”“像本人”. Read [references/realistic-handdrawn.md](references/realistic-handdrawn.md). For full-body outputs, keep the face unchanged while using a smaller head and approximately 4:6 upper-to-lower-body balance.
- **Bean-eye anime** applies when the user says “动漫”“豆豆眼”“漫画人物”“anime”. Read [references/anime-bean-eye.md](references/anime-bean-eye.md). This means dot/bean eyes, minimal nose and mouth, black hand-drawn outlines, colored-pencil fill, and flat 2D comic treatment—not large glossy anime eyes or semi-realistic chibi.
- If style is not specified, ask one concise question: “选择写实手绘，还是豆豆眼动漫风格？” Do not infer style from the requested quantity or format.
- If the user explicitly asks for both styles, create two sibling packs with the same file structure. Otherwise, keep the pack in one visual system.

## Default asset pack

Create four approved masters before exporting sizes:

1. `master-square.png` — 1:1 head-and-shoulders or half-body portrait; face and hair inside the central circle-safe area.
2. `master-vertical.png` — tall scene for wallpapers and vertical social posts; leave quiet space around the top clock area and avoid putting the face against the screen edge.
3. `master-wide.png` — 16:9 scene for presentations; preserve at least 40% calm negative space for future copy.
4. `master-cutout.png` — transparent-background bust or figure for reusable layouts. Create a full body only when the reference shows enough of the body or the user explicitly accepts inferred clothing and anatomy.

Read [references/asset-pack-presets.md](references/asset-pack-presets.md) for the exact exports and [references/composition-variants.md](references/composition-variants.md) for safe-area behavior.

Read [references/pose-library.md](references/pose-library.md) before generating a full-body or scene master. If the user gives no action, use the format default from that file; never copy an awkward pose from a photo or style reference by default.

## Workflow

1. **Require an accessible reference photo.** If none is available, ask the user to upload one. If several people appear and the intended subject is unclear, ask which person to draw.
2. **Inspect before editing.** Note subject count, crop, pose, expression, face proportions, hairstyle, visible clothing, defining accessories, lighting, and background. Do not infer sensitive traits.
3. **Set identity priorities.** Preserve, in order: subject count; roughly 80% recognizable identity; hairline and hairstyle; eyewear or defining accessories; clothing silhouette and color; requested action; crop; background. Permit light facial beautification instead of exact photographic reproduction.
4. **Generate masters through reference-image editing.** Include the original photo in every master-generation call. Do not create the later masters only from an earlier generated image; repeated generation from generation compounds identity drift.
5. **Use one style system.** Keep linework, palette, paper or brush texture, facial treatment, and clothing interpretation consistent across all masters.
6. **Approve the masters.** Read [references/quality-check.md](references/quality-check.md). If identity fails, correct the master before creating derivatives.
7. **Export exact sizes.** When local execution is available, run:

   ```bash
   python3 <skill-directory>/scripts/export_asset_pack.py \
     --square /absolute/path/to/master-square.png \
     --vertical /absolute/path/to/master-vertical.png \
     --wide /absolute/path/to/master-wide.png \
     --cutout /absolute/path/to/master-cutout.png \
     --out /absolute/path/to/portrait-asset-pack \
     --style realistic
   ```

   Resolve `<skill-directory>` from the loaded Skill path. If Pillow is missing, report the exact install command from `<skill-directory>/requirements.txt` and ask before installing it. The exporter reads its own `assets/presets.json`, removes low-alpha cutout halos by default, creates exact pixel sizes, adds left/right reusable layouts, and writes a contact sheet plus manifest.
8. **Validate derivatives.** Check that no crop cuts the head, chin, hands, or defining accessory; the face is clear at avatar size; the clock area is quiet on wallpapers; and PPT/social variants retain intended negative space.
9. **Deliver the folder and contact sheet.** Keep source photos outside the public repository and preserve all original files.

If exact local exporting is unavailable, generate the requested aspect ratios directly, state that pixel-perfect export was not run, and do not claim exact dimensions.

## Shared constraints

- Favor recognizable identity over fashionable stylization.
- Never silently beautify, slim, age-shift, change skin tone, redesign facial structure, replace hair, or change gender presentation.
- Keep the number of people, limbs, visible objects, and major accessories stable.
- Do not place decorative text, signatures, logos, or watermarks into reusable masters.
- Keep hands separated in the default pose; avoid clasped hands, hands behind the back, pigeon-toed feet, or stiff symmetrical standing.
- Do not copy a named living artist’s exact style. Translate style into general visual traits.
- Read [references/privacy-and-consent.md](references/privacy-and-consent.md) before using a photo or generated likeness in any public artifact.

## Output note

Report the base style, the four masters created, the number of exports, the output folder, and any intentionally omitted asset. Keep explanations concise; the contact sheet is the primary overview.
