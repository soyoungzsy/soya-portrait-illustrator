# Local identity library protocol · schema 1.0

These commands are helpers for the agent. The user's entry point is an uploaded photo and one short instruction. Paths below are examples; keep personal libraries and deliveries outside the Skill checkout. Original photos are never imported by these helpers. Confirm consent before any external image-editing service.

## First record and sharing kit

After the user approves the two generated masters:

```bash
python3 scripts/ip_library.py record \
  --library ../my-ip-library --identity-id my-character --style anime \
  --square ../work/square.png --cutout ../work/cutout.png --confirmed
python3 scripts/ip_library.py build \
  --library ../my-ip-library --version v0001 \
  --brief ../work/share-brief.json --out ../deliveries/first-share
```

Use `--synthetic` only for invented fixtures with no real identity. It is a provenance declaration, not anonymization. `--confirmed` must follow real user approval. The synthetic demo may confirm its own test fixture; that is not a real-person acceptance test.

The brief is an object with `schema_version: "1.0"`, `title`, and `point`. Unknown fields are discarded; do not add personal data. There is one fixed 1920×1080 cover layout: left editable text, right character. The conservative text budget is three title lines and four point lines. Capacity is estimated from Unicode character widths; actual font metrics and cropping need visual inspection. Long text fails instead of truncating. No OCR is performed.

## State and versioning

```text
my-ip-library/
  versions/
    v0001/
      identity.json
      square.png
      cutout.png
    v0002/ ...
```

`identity.json` contains `schema_version`, `project_version`, `identity_id`, `version`, `parent_version`, `confirmed`, `created_at`, `style`, `provenance`, `palette` (`background`, `accent`, `text`), `masters` and `changed`. Each master has a relative file name, SHA-256 and pixel size. Master paths are fixed by role and never trusted from JSON. Builds check the schema, confirmation and hashes before writing. This manifest is not cryptographically signed; a person who edits both image and manifest can defeat integrity checks.

Only one writer may record into a library at a time. There is no library-wide lock: version-directory reservation only avoids allocating the same directory and does not make concurrent first initialization safe. Do not launch concurrent `record` calls.

Versions are immutable through the CLI. There is no mutable “latest” pointer: explicitly pass a version. Save a new version for every confirmed revision; old deliveries remain reproducible in the same Pillow environment. Cross-version Pillow encoding may differ. Libraries contain personal likenesses and are private local data even when EXIF is removed. No cloud sync, encryption or backup is included; use the user's approved local backup practice.

## Next theme and narrow corrections

Change only the brief and run `build` with the same version and a new output path. No model call is needed.

```bash
# Change palette only; both approved master files remain byte-identical.
python3 scripts/ip_library.py record --library ../my-ip-library \
  --base v0001 --accent '#29A398' --confirmed
# Store a newly approved expression in the square master only.
python3 scripts/ip_library.py record --library ../my-ip-library \
  --base v0002 --square ../work/revised-square.png --confirmed
```

Do not regenerate all masters to correct a title or color. For a real visual edit, protect hair, face, outfit and accessories except the explicitly requested feature. Provider-supported masks may help but cannot guarantee preserved pixels within a regenerated master. Keep rejected attempts outside the version library. Record a short local reason for any rejected edit if useful; do not publish private prompt logs.

## Deliverables and checks

- `avatar.png`: 1024², viewed as circles at 48/96/192 pixels.
- `cover.svg`: self-contained 1920×1080 image with real `<text>` / `<tspan>` elements. Text is editable in an SVG editor. Imported SVG may be flattened by slide applications; it does not promise native PowerPoint text editing. `cover-background.png` has no title/point layer.
- `ppt-cutout.png`: 1600² true RGBA; insert into PowerPoint. No PPTX file is generated.
- `preview.html`: local only, relative assets, no external resources or scripts.
- `brief.json`: editable text data; it may contain private topic text, so treat the delivery as private.
- `kit-manifest.json`: explicit identity version, master and output hashes, dimensions, palette, layout rectangles, check status and pending visual review. No absolute source paths or raw photo metadata.

Source alpha needs fully transparent background, opaque visible pixels and transparent corners. Alpha validity cannot detect a painted checkerboard inside the subject region or guarantee edge quality. Safe areas are project layout presets, not platform specifications. Contrast is checked at a minimum ratio of 4.5:1. Geometry checks do not detect face/hair cropping. Inspect the actual preview.

## Failure handling

| Failure | Recovery |
|---|---|
| Missing reference-image editing / unknown cost | Explain the missing host capability or provider/cost choice; stop dependent generation. |
| User rejects likeness / clothing drift | Re-edit only the affected master; do not save it as confirmed. |
| Fully opaque/empty cutout / opaque corners | Request a true alpha output or use an authorized removal tool; do not rename a JPEG to PNG. |
| Master hash mismatch | Restore the approved file from local backup or save a newly reviewed version. |
| Text capacity / low contrast | Shorten the brief or record a readable palette. No silent truncation. |
| Existing delivery | Choose a new output folder; no overwrite flag exists. |
| Missing font / stray generated letters / halos | Visually inspect and correct; script cannot certify these. |

Failed builds stage temporary files and clean them up. They return code 2 and print `error:`; they do not produce a completed delivery folder. An abruptly terminated process may leave a hidden `.ip-kit-*` temporary directory, which can be removed after checking no build is running.
