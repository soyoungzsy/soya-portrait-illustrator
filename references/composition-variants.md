# Composition variants

Use these rules while generating masters and reviewing exports.

## Avatar

- Keep the full hair silhouette, ears or earrings, glasses, and chin inside the central 78% of the square.
- Do not place the face exactly against the top edge.
- Test at 128 px on screen. The expression and main identity cue should still read.
- The circle-safe export adds margin; it does not draw a visible circle.

## Phone wallpaper

- Keep the top 18–22% visually quiet for time, camera cutout, and status information.
- Keep the bottom 8–12% free of important hands, text, or accessories.
- Put the eyes below the top UI zone, not behind the clock.
- Extend simple background shapes when adapting between nearby phone ratios. Do not stretch the face or body.

## WeChat Moments and general social

- Use the square export for grids and the 3:4 export for portrait-led single posts.
- Keep reusable masters text-free. Add captions later in a layout tool.
- Avoid placing the face within 5% of any edge because feed previews may crop differently.

## Xiaohongshu

- Use the 3:4 portrait export as the main working format.
- Preserve roughly 12–18% quiet space at the top when a later cover title is likely.
- Keep the text-free illustration as the source of truth. AI-generated Chinese text is not part of this Skill.

## Presentation

- Prefer 16:9 for current decks; retain 4:3 for legacy and venue-specific templates.
- For a person-left layout, keep the right 45–55% calm. Reverse this for person-right.
- Do not put the face beneath the title area or close to common slide margins.
- Use the transparent cutout for slide systems that already have a background.

## Future-ready illustration assets

- `character-cutout`: transparent, no baked-in frame, no text, no watermark.
- `character-sticker`: clean white contour around the cutout; suitable for casual content.
- `portrait-card-4x5`: balanced poster-like crop with enough breathing room for future captions.
- Left/right layouts should use minimal abstract accents rather than platform-specific branding.

## When to omit an asset

- Omit a full-body cutout when the source does not show enough body and the user did not authorize inference.
- Omit a wallpaper when the photo is too tightly cropped to create a safe tall composition without inventing major scene content; offer a plain or softly textured background instead.
- Omit text-bearing variants unless the user supplies the exact copy and asks for it.
