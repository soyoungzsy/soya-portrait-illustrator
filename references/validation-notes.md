# Validation notes

## v0.4.1 · boundary patch

The current official installation reference is [Build skills](https://learn.chatgpt.com/docs/build-skills), checked 2026-10-15: user scope is `~/.agents/skills`; project scope uses `.agents/skills`. The maintenance environment's existing `.codex/skills` catalog is compatibility evidence only. No user-global installation or target-host discovery/invocation was tested.

19 unittest cases passed on macOS / Python 3.9.6 / Pillow 11.3.0. Regression coverage adds source-directory/normalized-path/symlink aliases, all legacy export targets including contact sheet and manifest under overwrite, and preservation of existing ZIP/checksum files and regular/dangling link targets. The installable ZIP still runs the synthetic offline workflow after extraction. No real-person generation or full browser/font visual acceptance is claimed. Library recording is explicitly single-writer; concurrent initialization remains unsupported.


## v0.4.0 · local automated validation · 2026-10-15/16 UTC

Environment: macOS, Python 3.9.6, Pillow 11.3.0. To reproduce with the tested dependency, install `Pillow==11.3.0`; the existing requirements range remains Pillow 10–11.

- 13 unittest cases passed: legacy 17 exports, path protection, library reuse and byte stability, palette lineage, single-master revision, invalid alpha, missing confirmation, text overflow, master tampering, metadata removal, source-directory guard, low contrast and no-overwrite behavior.
- Package regression builds two ZIPs with identical SHA-256, extracts the Skill into a temporary install directory, validates it and runs the complete synthetic offline demo from that extracted package.
- Repository validator and Skill Creator frontmatter validator passed. The baseline required an absent CI file. An optional template now supplies validation and packaging, and the validator checks the template. Online CI is not activated because the existing GitHub OAuth login lacks workflow scope; GitHub explicitly rejected a workflow-file push.
- Heuristic scan covers tracked/unignored working files and every reachable Git commit/blob; manual diff review is still required. It does not prove absence of all private data or establish copyright consent.
- Synthetic demo: original Pillow-drawn geometric character, fictional Chinese title and point, one version used for first and next-theme deliveries. No model call, charge, photo upload or real identity. Avatar, text-free cover raster and alpha cutout were inspected as local images.
- Full browser preview and final font rendering were **not visually verified**: the browser policy rejected local `file:` navigation. The HTML/SVG files remain available for manual inspection. XML tests verify editable text and escaping; they do not certify rendering.
- No new real-person generation, likeness acceptance, installed-host photo workflow or contest submission was performed. The author case and continuous recording remain pending.

## Historical v0.3.0 maintainer record

The following record was already in the repository at the baseline. It was not independently reproduced for v0.4.0 and must not be presented as new acceptance evidence.

Last validated: 2026-10-10.

## Private visual validation

The workflow was exercised with a set of user-authorized private photos that are not distributed with this repository.

- Realistic hand-drawn square master: generated and checked for recognizable facial structure, hair color, cap, outfit, crop margin, and absence of text.
- Realistic tall master: generated with a quiet top clock area and consistent style.
- Realistic 16:9 master: generated with the subject on the right and usable copy space on the left.
- Transparent full-body master: generated with alpha; a low-opacity halo was observed and became the reason for adding the exporter’s default alpha-threshold normalization.
- Initial semi-realistic big-eye chibi master was rejected after user review because it did not match the intended anime mode.
- The accepted anime definition is now bean-eye hand-drawn comics: dot/bean eyes, minimal nose and mouth, black outlines, colored-pencil fill, flat 2D treatment, and 5–6-head-tall full-body proportions.
- User-approved preview boundary: approximately 80% recognizable identity, light facial beautification, and a relaxed asymmetric stance with separated hands.
- Final anime full-body boundary: cute, modest, non-sexualized A-line silhouette without exaggerated bust, waist, or hip curves.
- Default pack: exported to all 17 declared dimensions with a contact sheet and privacy-safe manifest.
- The first real export showed that cropping the 16:9 master into 4:3 clipped the subject; `ppt-standard` now composes from the transparent cutout and was revalidated.

The source photos and generated likenesses remain outside the public repository. This evidence establishes that the workflow can run end to end; it does not promise identical model output across providers or future model versions.

## Automated validation

`tests/test_export_asset_pack.py` verifies:

- All default manifest dimensions.
- Transparent output behavior and low-alpha halo removal.
- Contact-sheet and manifest creation.
- Rejection of preset paths that attempt to escape the selected output directory.
