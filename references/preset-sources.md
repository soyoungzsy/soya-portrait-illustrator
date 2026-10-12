# Preset sources and maintenance boundary

Last reviewed: 2026-10-09.

The repository uses working export presets, not claims that social platforms will permanently require a specific pixel size. Ratios and safe-area behavior are more durable than platform UI details.

## Primary references

- [Apple Human Interface Guidelines — Layout](https://developer.apple.com/design/human-interface-guidelines/layout): lists current iPhone display point and pixel sizes, including 1290×2796 for several large-screen models. The project keeps that size as one iPhone-oriented wallpaper preset, not as a universal iPhone requirement.
- [Samsung Galaxy S26+ specifications](https://www.samsung.com/in/multistore/in_icai/feature.SM-S947BZKBINS/): lists a 3120×1440 main display. The project includes the portrait orientation, 1440×3120, as an Android QHD wallpaper preset.
- [Microsoft Support — Change the size of your PowerPoint slides](https://support.microsoft.com/en-us/powerpoint/change-the-size-of-your-powerpoint-slides): documents Standard 4:3 and Widescreen 16:9, with 16:9 as the default for new presentations. The project exports both ratios.

## Project conventions

- `1080×1440` and `1242×1660` are both 3:4 working canvases for portrait social content. They are intentionally labeled as project presets rather than official permanent Xiaohongshu requirements.
- `1080×1080` is a reusable square social canvas, not a promise about every WeChat Moments display mode.
- `1080×1920` is a general 9:16 vertical canvas for stories, video covers, and future layouts.
- Platform UI, compression, and preview cropping can change. Keep the four high-resolution masters and update `assets/presets.json` when a downstream destination changes.

Contributors should prefer current first-party documentation when changing a device or presentation preset. If a social platform has no stable public specification, document the dimension as a project convention rather than presenting it as official.
