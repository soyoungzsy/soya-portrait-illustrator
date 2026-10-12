# Realistic hand-drawn mode

Use this mode for “写实手绘”“人物速写”“彩铅肖像”“尽可能像本人” and ambiguous photo-to-illustration requests.

## Target look

- Recognizable at first glance, with natural human proportions.
- Visible hand-made linework: graphite or colored-pencil edges, restrained cross-hatching, and a light watercolor or gouache wash.
- Skin, hair, and fabric retain real tonal variation. Avoid airbrushed plastic skin.
- A quiet paper texture may be present, but it must not obscure eyes, mouth, or other likeness cues.
- The result should read as a carefully observed portrait drawing, not a photograph with a generic filter.
- For full-body assets, use slightly idealized editorial proportions without changing identity: a smaller head relative to the body, natural shoulders and waist, and approximately 4:6 upper-to-lower-body balance with longer legs.
- Preserve approximately 80% recognizable identity rather than exact photographic replication. Allow light beautification of facial balance, jawline smoothness, skin clarity, and expression while keeping age, overall face type, and personal character stable.

## Prompt structure

Replace every brace field with observations from the actual photo. Do not send braces or instructions as literal prompt text.

```text
Edit the supplied reference photo into a realistic hand-drawn portrait of the same person.

Identity anchor: preserve the exact subject count and approximately 80% recognizable identity through {general face shape}, {eyes and brows}, {nose and mouth cues}, {expression and gaze}, {hairline and hairstyle}, and {defining accessories}. Lightly beautify facial balance, skin clarity, and smile; do not reproduce exact photographic proportions. Preserve {clothing silhouette}, the selected pose from pose-library.md, and the requested crop/aspect ratio.

Visual treatment: refined graphite and colored-pencil linework with a restrained watercolor wash on lightly textured warm-white paper. Natural anatomy, believable facial planes, subtle line-weight variation, soft but accurate color, and a calm editorial portrait finish. Keep details concentrated around the face; simplify only secondary background details.

Full-body proportion when applicable: keep the face unchanged, reduce only the head-to-body scale, and use an aesthetically balanced approximately 4:6 upper-to-lower-body proportion with natural long legs. Do not distort shoulders, waist, hands, or feet.

Composition: {background instruction}. Preserve the source lighting direction and overall mood unless the user requested a change.

Do not beautify or redesign the person. No face swapping, generic model face, age shift, skin-tone shift, body reshaping, hairstyle replacement, altered expression, extra people, extra fingers or limbs, mismatched eyes, plastic 3D rendering, photorealistic camera finish, text, signature, logo, or watermark.
```

## Useful adjustments

- **More sketch-like:** reduce color coverage, expose construction lines sparingly, and keep the face fully resolved.
- **More polished:** add controlled colored-pencil layers and smoother watercolor transitions without erasing paper texture.
- **Cleaner background:** simplify it into two or three quiet tonal shapes while preserving the subject’s outline and original scene cues.
- **Avatar crop:** change to a centered head-and-shoulders crop only when requested; keep head shape, shoulders, and hair volume intact.

## Avoid

- “Perfect face,” “beautify,” “ideal proportions,” or similar instructions that fight resemblance.
- Heavy oil-paint impasto, glossy 3D character rendering, fashion-editorial retouching, or anime facial conventions.
- Over-rendering every background object; it competes with the face and encourages identity drift.
- A large head, compressed legs, or a 1:1 torso-to-leg split in full-body assets.
