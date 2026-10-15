# Privacy

Soya Portrait Illustrator is a prompt-and-workflow repository. It does not operate a server, collect analytics, receive photos, or store generated images on behalf of users.

## What may leave your device

When the Skill is used, the host application may send the reference photo, edit instructions, and generated output to the image-generation provider selected by the user or environment. That provider’s privacy, retention, moderation, and billing terms apply. This project does not claim local-only processing.

## User responsibilities

- Use only photos you own or are authorized to edit.
- Obtain appropriate consent before editing or publishing another person’s likeness.
- Do not use sensitive, confidential, intimate, medical, financial, or location-revealing images unless the chosen provider and context are appropriate.
- Do not publish a source photo or generated likeness without permission for that specific use.
- Remove unnecessary EXIF metadata before sharing images publicly.

## Contributor rules

Do not include any of the following in an issue, pull request, fixture, screenshot, or demo:

- Identifiable user photos or generated likenesses without explicit publication permission.
- Private image URLs, prompt logs containing personal data, or provider request IDs tied to a user.
- API keys, access tokens, or account information.

Use synthetic people, self-owned photos explicitly released for the project, or permissively licensed public images with recorded attribution.

The export manifest records only generic source roles such as `square` and `cutout`; it does not store input paths, input filenames, or subject names. Contributors should preserve this privacy boundary when extending the exporter.

## Deletion

This repository does not hold user photos, so it cannot delete data retained by a host application or model provider. Use the deletion and account controls offered by the service that processed the image.

## Local library in v0.4.0

Confirmed masters, identity aliases, palette versions and delivery briefs are private local data. Keep them outside the public Skill checkout. Original photos are not imported by the helper. Re-encoding removes image metadata, but the likeness remains personal data. No automatic upload, sync, encryption or backup is included. Never infer publication permission from permission to process a photo. The public demo uses only an original geometric fixture with no real identity.
