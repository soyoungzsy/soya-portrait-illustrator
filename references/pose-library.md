# Reusable pose library

Choose pose independently from visual style. User-specified action always wins. When no action is specified, select the format default below instead of copying the pose from an identity or style reference.

## Default poses

| ID | Pose | Best use |
|---|---|---|
| `neutral-relaxed` | Three-quarter body angle; weight on one leg; other foot slightly forward and outward; shoulders open; one arm relaxed at the side; other arm gently bent with an open hand near the waist seam. Hands remain separate. | Default full-body cutout, general illustration, future layouts |
| `friendly-wave` | Small shoulder-height wave with relaxed fingers; other arm naturally lowered; body slightly turned. | Social posts, welcome cards, friendly profile content |
| `walking` | Natural mid-step with one foot forward; opposite arm swings gently; torso upright; gaze toward viewer or travel direction. | Phone wallpaper, posters, lifestyle social content |
| `thinking` | One hand lightly touching chin or cheek; other forearm relaxed across the waist; head tilted slightly, not exaggerated. | Reflection, strategy, idea, question scenes |
| `working` | Seated or standing naturally while writing on a notebook or using a laptop; shoulders relaxed; prop interaction physically plausible. | Work, AI building, planning, productivity scenes |
| `presenting` | Body faces the viewer at a slight angle; one open palm indicates the copy area; other arm relaxed. | PPT covers, explainers, left/right layout illustrations |
| `reading` | Holds one book or document at comfortable chest height; gaze lowered naturally; elbows not forced against the body. | Reading, learning, report, knowledge content |

## Format defaults

- **Avatar:** crop above the hands; shoulders turn slightly; head faces the viewer; use `neutral-relaxed` upper body.
- **Phone wallpaper:** prefer `walking`; use `neutral-relaxed` when a calmer mood is required.
- **Social portrait:** prefer `friendly-wave` or `walking` according to the requested mood.
- **PPT or copy-space layout:** use `presenting`, with the open palm directed toward the empty copy side.
- **Transparent cutout:** use `neutral-relaxed` unless a downstream scene requires another action.
- **Thinking/working/reading scenes:** use the matching action only when the requested topic supports it; do not add props merely for decoration.

## Hard exclusions

- No `clasped hands` in front of the abdomen.
- No `hands behind the back` as the generic default.
- No `pigeon-toed` or inward-turned feet.
- No stiff front-facing symmetrical stance.
- No mirrored arm positions, hidden hands without a crop reason, or fingers pinching imaginary objects.
- Do not copy a pose from a style reference unless the user explicitly requests that pose.

## Body balance

- Realistic full body: modestly small head, identity-preserving face, approximately 4:6 upper-to-lower-body balance, natural long legs.
- Bean-eye anime full body: around 5–6 heads tall, modest head size, approximately 4:6 upper-to-lower-body balance, with a cute simplified straight or A-line silhouette and no emphasized gender curves.
- Pose should create an easy S-curve or diagonal rhythm without distorting the spine, hips, knees, hands, or feet.
