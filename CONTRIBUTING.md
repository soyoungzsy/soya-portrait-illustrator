# Contributing

Contributions are welcome when they improve likeness preservation, reduce unwanted identity drift, clarify consent boundaries, or make the Skill easier to use across image-editing providers.

## Before opening a pull request

1. Keep `SKILL.md` concise and route mode-specific detail to `references/`.
2. Keep instructions provider-neutral unless a provider-specific limitation is explicitly isolated and documented.
3. Run `python3 scripts/validate_skill.py .` from the repository root.
4. When changing `assets/presets.json` or `scripts/export_asset_pack.py`, run the exporter on synthetic masters and verify every manifest dimension plus cutout transparency.
5. Test changed visual instructions with images you are authorized to use.
6. Report observable outcomes, including failure cases; do not claim that a prompt is reliable based only on its wording.

## Photo and identity safety

- Never commit a real user’s photo or generated likeness.
- Do not paste private image links, personal prompt logs, API keys, or provider request IDs into issues.
- For reproducible examples, use a synthetic person, your own image with explicit publication intent, or a permissively licensed source whose attribution is recorded.
- Blur or remove unrelated bystanders and private background information before sharing an authorized test image.

## Good contributions

- A focused change with a clear before/after observation.
- A correction strategy that changes only the failed identity cue.
- A test matrix covering different lighting, hair, eyewear, age, or crop conditions without making sensitive-trait claims.
- Documentation that explains a genuine decision boundary rather than adding generic prompt adjectives.

## Avoid

- Prompts that beautify, slim, age-shift, or homogenize faces by default.
- Exact imitation of a named living artist.
- Real-person galleries without explicit, documented publication permission.
- Model rankings presented without repeatable tests and dates.
