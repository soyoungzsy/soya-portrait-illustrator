# Anime bean-eye mode

Use this mode for “动漫风格”“豆豆眼”“漫画人物”“anime”. The required look is a flat hand-drawn comic illustration, not a semi-realistic big-eye render and not a glossy 3D character.

## Target look

- Small solid-black vertical oval or bean-shaped eyes. No iris gradients, glassy highlights, eyelashes rendered like a beauty portrait, or oversized anime eyes.
- A minimal nose drawn as one short hook, dot, or tiny line; a simple curved mouth; optional restrained pencil blush.
- Clean black hand-drawn contours with slight line-weight variation and visible colored-pencil or crayon fill texture.
- Warm off-white paper or genuine transparency; flat two-dimensional treatment with little or no cel-shading.
- Preserve the subject’s face outline, eyebrow angle, eye spacing, hairstyle silhouette, hair color, cap, clothing colors, and expression so the character remains person-specific.
- Target approximately 80% recognizable identity; lightly beautified facial balance is intentional: use a smoother face outline, cleaner jawline, clearer skin, and friendlier smile, but do not reproduce exact photographic facial proportions.
- For full-body assets, use an elegant illustrated proportion around 5–6 heads tall, a modest head size, and roughly 4:6 upper-to-lower-body balance. Do not use the previous 2.5–3.5-head chibi proportion.
- Use a cute, modest, non-sexualized silhouette. Simplify the torso and clothing into soft straight or A-line shapes; no exaggerated bust, waist, or hip curves, cleavage, pin-up posture, or fashion-model hourglass treatment.

## Style anchor

When a bean-eye reference image is supplied, label it as **style reference only**. Use the user’s photos as the identity source. Do not copy the reference image’s pets, robot, notebook, coffee cup, books, pose, or scene unless the user explicitly asks for them.

## Prompt structure

Replace every brace field with observations from the actual photo. Do not send braces or instructions as literal prompt text.

```text
Edit the supplied person photo into a recognizable bean-eye hand-drawn anime illustration of the same person.

Identity anchor: preserve about 80% recognizable identity through {general face outline}, {eyebrow angle}, {eye spacing}, {hairline and hairstyle silhouette}, {hair color}, {expression}, {cap or defining accessory}, and {clothing colors and silhouette}. The user photos define identity; the supplied comic image defines style only. Lightly beautify facial balance and do not reproduce exact photographic facial proportions.

Anime treatment: small solid-black bean-shaped eyes, minimal single-line nose, simple curved mouth, subtle pencil blush, clean black hand-drawn outlines, visible colored-pencil fill texture, warm off-white paper, flat two-dimensional comic finish. For full body, use a modest head size, 5–6-head-tall illustrated proportion, approximately 4:6 upper-to-lower-body balance, and a cute simplified A-line silhouette without emphasized gender curves.

Composition and pose: {format-specific composition and pose selected from pose-library.md}. Keep the person recognizable without realistic facial rendering.

No glossy oversized eyes, no iris gradients, no realistic eyelashes, no semi-photorealistic face, no 3D doll render, no generic V-shaped anime face, no 2.5-head chibi body, no exaggerated chest/waist/hips, no cleavage, no pin-up pose, no copied props or pets from the style reference, no extra people, no text, signature, logo, or watermark.
```

## Useful adjustments

- **Avatar:** retain the bean eyes and simplified face, but keep the real hair silhouette and cap fully inside the circular safe area.
- **Wallpaper:** use a 5–6-head-tall figure with long, clean leg lines; keep the top UI zone quiet.
- **Presentation:** place the figure left or right with restrained pencil accents and large empty copy space.
- **Transparent cutout:** keep only the character, with clean black outline and genuine transparent background.

## Avoid

- Turning bean eyes into large luminous anime eyes.
- Keeping a realistic nose and mouth while cartoonizing only the eyes.
- Copying the reference composition or its dog, cat, robot, stationery, books, or drink.
- Making the head dominate half the body height.
- Emphasizing breasts, a tiny waist, hips, or other sexualized feminine features instead of the cute character style.
