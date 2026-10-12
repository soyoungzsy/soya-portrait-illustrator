# Validation notes

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
