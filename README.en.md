# Soya Portrait Illustrator · Personal IP Library

Version 0.4.0 · [中文](README.md) · [MIT](LICENSE)

Upload an authorized photo and say: **“Build my personal IP illustration library from this photo.”** The Skill checks the host's capabilities, asks only for missing purpose/topic/point information, obtains master approval, and delivers an avatar, editable-text sharing cover and transparent PPT illustration. Save the confirmed identity and palette, then reuse them for later topics.

## Requirements and installation

Install the complete `soya-portrait-illustrator/` folder into your host's Skills directory, with `SKILL.md` directly inside it; Codex commonly uses `~/.codex/skills/`. Reload Skills. Explicit invocation: `Use $soya-portrait-illustrator to build my personal IP illustration library from this photo.` No extra long prompt is required.

The host must inspect uploaded images, perform reference-image editing and save accessible output files. True transparent cutouts require alpha-capable output. This Skill includes no model, credits, API keys or background removal service. Newly paid calls and photo uploads require an agreed provider, data scope and cost. Short startup does not imply zero configuration in every environment.

Local helpers need Python (3.10+ recommended; tested with 3.9.6) and Pillow 10–11. A browser and appropriate system fonts are needed for previews. SVG text remains editable in SVG editors, but slide apps may flatten it. No PPTX or native PowerPoint text boxes are created.

## Reproducible offline demo

```bash
python3 -m venv ../soya-ip-venv
source ../soya-ip-venv/bin/activate
python3 -m pip install -r requirements.txt
python3 scripts/create_synthetic_demo.py --out ../synthetic-demo
```

Open `../synthetic-demo/first-share/preview.html`. This original geometric fixture and the fictional titles exercise first delivery and next-theme reuse without any model calls or real identity. They are not evidence of photo generation quality.

![Actual offline outputs from the synthetic fixture](examples/synthetic-showcase.svg)

## Workflow and outputs

Confirm a square master and a true alpha cutout. The agent runs `scripts/ip_library.py record` to save an immutable confirmed version, then `build` with an explicit version and JSON brief. See [commands, manifests and failures](references/personal-library.md).

- `avatar.png`: 1024², previewed at 48/96/192 pixels with circle cropping.
- `cover.svg`: 1920×1080, editable SVG title and point; `cover-background.png` is text-free.
- `ppt-cutout.png`: 1600² RGBA, previewed on light/dark/checkerboard surfaces.
- `preview.html`, `brief.json`, `kit-manifest.json`: local preview, text data, identity version, hashes, palette, dimensions and check results.

Text-only changes reuse the same masters. Palette and master edits create child versions. Unchanged master files retain their bytes. Regional generation may drift and still needs human review. Libraries and deliveries must stay outside the Skill source directory; original photos are not imported. Stored portraits and topic text remain private personal data even after metadata is removed.

New in 0.4.0: persistent identity/palette versions, reuse, narrow revisions, sharing kit, editable text, preview and failure handling. The four masters, 17 exports, two styles and approval rules already existed in 0.3.0; the legacy exporter remains available.

## Verification and packaging

```bash
python3 scripts/validate_skill.py .
python3 -m unittest discover -s tests -v
python3 scripts/release_audit.py --history
python3 scripts/package_skill.py --out ../soya-portrait-illustrator-0.4.0.zip
```

Packaging uses an explicit source allowlist and deterministic ZIP metadata. It never includes local photos, identity libraries, environments or `.git`. The release scan is heuristic and requires manual diff and provenance review. An [optional GitHub Actions template](references/github-actions.yml) validates and builds the ZIP. It is not enabled: the current GitHub OAuth login lacks `workflow` scope. An authorized maintainer may later copy it to `.github/workflows/validate.yml`. Local validation and packaging work without that scope.

No new real-person generation or likeness acceptance was performed for this upgrade. No OCR, face recognition, automatic publication, cloud synchronization, encryption or backup is included. One fixed cover layout is supported; text capacity and contrast checks cannot verify actual fonts or identity. See [validation notes](references/validation-notes.md), [privacy](PRIVACY.md) and the [entry preparation checklist](references/competition-checklist.md). The author's own case awaits her approved evidence; no external testimonials or time savings are claimed.

Only third-party Python dependency: official [Pillow](https://github.com/python-pillow/Pillow), distributed under [MIT-CMU](https://github.com/python-pillow/Pillow/blob/11.3.0/LICENSE). No fonts, models or third-party character assets are bundled. The original geometric demo is distributed under the project's MIT license.
