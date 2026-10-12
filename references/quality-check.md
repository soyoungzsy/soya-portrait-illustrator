# Likeness and quality check

Compare the result with the source photo at similar on-screen size. Style quality cannot compensate for identity failure.

## Hard gates

Any item below is a failure:

- Wrong number of people or the wrong person emphasized.
- The result loses the intended person’s overall identity anchors and reads as an unrelated generic character. Exact photo-level likeness is not required.
- Hairstyle silhouette, hairline, eyewear, or another defining cue has disappeared or materially changed.
- Pose, expression, clothing silhouette, crop, or background changed without user authorization.
- Extra or missing limbs, obviously malformed hands, mismatched eyes, or broken facial anatomy.
- Unrequested text, signature, logo, or watermark.

## Scorecard

Give each dimension 0, 1, or 2 points:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Identity and beautification | Unrelated generic person | Recognizable but too literal or too generic | About 80% recognizable with controlled light beautification |
| Hair and accessories | Missing or redesigned | Mostly present | Distinctive cues preserved |
| Expression and pose | Changed | Close | Faithful |
| Requested style | Wrong mode | Mixed or generic | Clearly on target |
| Technical integrity | Visible defects | Minor defects | Clean |

Release at **8/10 or higher with no hard-gate failure**. The score is an internal decision aid; do not burden the user with it unless they ask for evaluation details.

## One-pass correction order

If correction is needed, fix the first applicable item and keep everything else stable:

1. Subject count and face identity.
2. Eyes, brows, mouth, and expression.
3. Hairline, hairstyle, eyewear, and accessories.
4. Anatomy and hands.
5. Style strength and background simplification.

Use a focused edit instruction such as “keep the existing composition and colors; correct only the eye spacing, brow angle, and hairline to match the reference.” Avoid rewriting the full prompt during a local correction because that invites drift elsewhere.

## Asset-pack derivative check

After the four masters pass, inspect the contact sheet and several full-size exports:

- Avatar: face and defining accessories remain legible at 128 px; circular crop does not cut hair or chin.
- Wallpaper: top 18–22% and bottom 8–12% contain no critical face, hand, or accessory detail.
- Social: no edge crop removes the head, shoulder, hand, or prop.
- Presentation: the designated copy side has calm negative space and the person does not cross common slide margins.
- Transparent cutout: edges are clean, holes inside glasses and between limbs remain transparent, and no source background survives.
- Layout variants: left and right compositions use the same approved cutout rather than regenerated people.
- Pose: hands remain separated unless interaction requires contact; stance matches the format default and avoids the hard exclusions in `pose-library.md`.
- Anime silhouette: cute and modest, with no unnecessary emphasis on bust, tiny waist, hips, cleavage, or sexualized posture.

Exact dimensions must match `assets/presets.json`. Pixel correctness does not override a failed likeness gate.
