# Soya Portrait Illustrator

[![Version](https://img.shields.io/badge/version-0.3.0-E76F51)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-264653)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Codex-Agent%20Skill-2A9D8F)](https://agentskills.io/)

**上传一张照片，选择写实手绘或豆豆眼动漫风格，生成一套仍然像本人的人物素材：头像、手机屏保、朋友圈、小红书、PPT，以及以后还没想好版式的透明插画。**

Soya Portrait Illustrator 是一个可安装到 Codex 的开源 Agent Skill。它不把任务理解成“给照片套滤镜”，而是先生成一组高相似度母版，再把母版稳定地适配成多种尺寸和版式。这样，同一个人在头像里、屏保里、社交内容里和 PPT 里仍然是同一个人。

这是面向公开用户的素材包版本：上传照片后，需求未指定数量时默认生成整套素材包。SOYA 本地使用的“模糊需求默认单张”是独立的私人 Skill，不属于本仓库。

[English README](README.en.md)

## 一张照片，为什么要做成一套素材

一张好看的插画通常只能解决一次需求：裁成头像时脸太小，放进手机屏保时被时间挡住，放到 PPT 时没有留文字空间，发小红书时又要重新构图。每次重新生图，不仅成本高，还容易出现人物变脸、发型漂移、衣服和配饰不一致。

这个项目采用“**母版 → 确认相似度 → 自动导出**”的方式：

1. 用原照片生成方形、竖版、横版、透明人物四张母版。
2. 先检查脸型、五官关系、神态、发型、眼镜、服装和姿态是否仍像本人。
3. 再从已确认的母版导出一整套精确尺寸，不让每个尺寸都重新发明一个人。

## 两种可选人物风格

| 风格 | 视觉语言 | 更适合 |
|---|---|---|
| 写实手绘 | 铅笔/彩铅线稿、轻水彩、纸张纹理；不改脸，优化为小头、上身与下身约 4:6 的自然修长比例 | 纪念肖像、质感头像、手机屏保、人物型 PPT、个人品牌内容 |
| 豆豆眼动漫 | 小黑豆眼、极简鼻嘴、黑色手绘线、彩铅填色、平面二维漫画感；全身约 5–6 头身，用可爱简化轮廓，不强调胸腰胯等女性曲线 | 社交头像、贴纸、小红书、朋友圈、文档/网页插画和个人 IP |

“生成一张还是整套素材”与“选择哪种风格”是两个独立选项。未指定风格时会先询问选择**写实手绘**还是**豆豆眼动漫**；只有明确说“两种都要”时，才生成两套同结构素材包。

人物默认保留约 80% 辨识度，并允许轻度美化，不追求照片级复刻。没有指定动作时，项目会按头像、屏保、社交图、PPT 和透明人物分别调用通用动作库，避免双手交叠、双手背后、内八或僵直站姿。

## 默认会得到什么

### 1. 四张可长期复用的母版

| 母版 | 比例 | 用途 | 构图规则 |
|---|---:|---|---|
| 方形人物母版 | 1:1 | 头像、方形社交图、人物卡片 | 脸和发型进入圆形安全区，四周保留裁切空间 |
| 竖版场景母版 | 约 9:19.5 | 手机屏保、竖版社交内容 | 顶部给时间和状态栏留白，人物不贴边 |
| 横版场景母版 | 16:9 | PPT、封面、横版内容 | 至少 40% 安静留白，可继续排标题和正文 |
| 透明人物母版 | 透明 PNG | 未来版式、贴纸、左/右人物排版 | 默认只做参考图真实可见的身体范围 |

透明母版不会凭空把一张大头照补成“可信全身照”。原图没有下半身时，默认输出胸像或半身；只有用户明确接受推断时才生成全身。

### 2. 自动导出的默认素材包

| 类别 | 文件 | 像素 | 典型用途 |
|---|---|---:|---|
| 头像 | `avatar-square-1024.png` | 1024×1024 | 微信、小红书、社交账号、个人资料页 |
| 头像 | `avatar-circle-safe-1024.png` | 1024×1024 | 会被平台裁成圆形的头像 |
| 头像 | `avatar-small-512.png` | 512×512 | App、通讯录、轻量网页头像 |
| 手机屏保 | `phone-wallpaper-ios-large.png` | 1290×2796 | 大屏 iPhone 竖版屏保预设 |
| 手机屏保 | `phone-wallpaper-android-qhd.png` | 1440×3120 | 高分辨率 Android 竖版屏保预设 |
| 手机屏保 | `phone-wallpaper-universal.png` | 1080×2400 | 适合多数手机继续裁切的通用版 |
| 朋友圈 | `moments-square.png` | 1080×1080 | 单图、九宫格基础素材 |
| 社交竖图 | `social-portrait.png` | 1080×1440 | 朋友圈、小红书和通用 3:4 竖图 |
| 小红书 | `xiaohongshu-portrait.png` | 1242×1660 | 3:4 高分辨率封面或正文首图 |
| Story/竖屏 | `social-story.png` | 1080×1920 | 9:16 竖屏内容、视频封面、未来竖版版式 |
| PPT | `ppt-wide.png` | 1920×1080 | 16:9 演示文稿、线上分享 |
| PPT | `ppt-standard.png` | 1600×1200 | 4:3 演示、旧模板或特定会议室 |
| 插画素材 | `character-cutout.png` | 2048×2048 | 透明人物、海报、文档、网页继续排版 |
| 插画素材 | `character-sticker.png` | 1024×1024 | 白边贴纸、社交内容、装饰元素 |
| 未来版式 | `layout-person-left.png` | 1920×1080 | 人物在左，右侧留标题/正文空间 |
| 未来版式 | `layout-person-right.png` | 1920×1080 | 人物在右，左侧留标题/正文空间 |
| 未来版式 | `portrait-card-4x5.png` | 1600×2000 | 人物海报、卡片、后续平台适配 |

这些是项目的**稳定工作预设**，不是对平台永久官方规格的承诺。平台会改版，真正稳定的是比例、构图安全区和保留高分辨率母版。尺寸依据与维护边界见 [references/preset-sources.md](references/preset-sources.md)。

导出后还会生成：

- `contact-sheet.jpg`：一眼查看整套素材。
- `pack-manifest.json`：记录风格、尺寸、来源母版和文件列表，不记录人物姓名或绝对路径。

## 具体使用场景

### 做头像

普通方图在微信、小红书或其他平台里常被再次裁成圆形。项目同时输出普通方形头像和圆形安全区头像，避免头发、耳朵、眼镜或下巴被平台裁掉。512 与 1024 两档也兼顾轻量使用和高清存档。

### 做手机屏保

屏保不是把一张竖图拉长。顶部的时间、灵动岛/开孔、状态栏，底部的快捷操作都可能挡住主体。竖版母版会预留安静区域，再导出 iPhone 大屏、Android QHD 和通用 20:9 三档；换设备时优先裁切背景，不裁人物脸和关键动作。

### 发朋友圈

方图适合单图和九宫格，3:4 竖图更适合完整展示人物。项目不默认往图里写文案，因为文字会限制二次使用；你可以把同一张素材拿去配不同朋友圈内容，也可以之后再在安全留白区排字。

### 发小红书

默认提供 3:4 高分辨率竖图，人物不会占满顶部，便于后续加标题。它也保留无字版，避免 AI 生图文字错误，并让一张人物素材能复用于封面、正文首图和系列内容。

### 做 PPT

项目同时提供 16:9 和 4:3 两档，并额外生成“人物在左 / 人物在右”两种 16:9 版式。人物和文字不抢位置，适合个人介绍、案例页、章节页、演讲封面、人物观点和结束页。PowerPoint 当前仍以 16:9 为默认，同时保留 4:3 标准尺寸，因此两档都留着更稳妥。

### 适配未来还不知道的版式

真正有长期价值的是透明人物母版。它可以继续放进网页、海报、长图、文档、视频封面或新平台尺寸。项目还提供白边贴纸、4:5 人物卡和左右留白版式，先覆盖高频组合，同时避免为每个未来场景重新生成人物。

## 安装

下载或克隆本项目，把整个文件夹复制到：

```text
~/.codex/skills/soya-portrait-illustrator
```

目录中应直接看到 `SKILL.md`。重启或刷新 Codex 后即可被自动发现。

## 使用

上传一张有权使用的人物照片，然后说：

```text
用 $soya-portrait-illustrator 把这张照片做成一整套写实手绘素材。保留脸型、眼神、发型、眼镜、衣服配色和姿态，输出头像、手机屏保、朋友圈、小红书、PPT 和透明人物素材。
```

或生成豆豆眼动漫版：

```text
Use $soya-portrait-illustrator to create a complete bean-eye anime asset pack from this photo. Use small black bean eyes, a minimal nose and mouth, black hand-drawn outlines, colored-pencil fill, and flat 2D comic treatment while keeping the person recognizable.
```

只想做一张也可以：

```text
用 $soya-portrait-illustrator 只做一张 16:9 的写实手绘 PPT 封面，人物在右，左侧留文字空间。
```

更多示例见 [examples/requests.md](examples/requests.md)。

## 自动导出精确尺寸

生图工具主要负责人物和场景，精确像素由脚本完成，避免为了改尺寸反复重画人物。

```bash
python3 -m pip install -r requirements.txt
python3 scripts/export_asset_pack.py \
  --square master-square.png \
  --vertical master-vertical.png \
  --wide master-wide.png \
  --cutout master-cutout.png \
  --out portrait-asset-pack \
  --style realistic
```

脚本使用 `assets/presets.json`，会生成全部默认尺寸、联系表和 manifest。可以通过修改 JSON 增加未来平台，不必改 Skill 主流程。

透明人物生成常见的低透明度光晕会在导出时自动清理；默认阈值为 16，可通过 `--alpha-threshold` 调整。自定义预设的 `id` 与 `category` 只允许小写字母、数字和连字符，所有输出都必须留在用户指定的 `--out` 目录内。

## 项目结构

```text
SKILL.md                             入口、风格路由、母版与素材包工作流
agents/openai.yaml                  Skill 界面名称、图标和默认调用语
references/realistic-handdrawn.md   写实手绘风格与提示词骨架
references/anime-bean-eye.md        豆豆眼动漫风格与提示词骨架
references/asset-pack-presets.md    默认尺寸、来源母版与安全区
references/composition-variants.md  头像/屏保/社交/PPT 的构图规则
references/pose-library.md          通用动作、版式默认动作和禁用姿态
references/quality-check.md         相似度硬门槛与修正顺序
references/privacy-and-consent.md   照片授权、隐私与公开分享边界
references/preset-sources.md        尺寸依据与非官方预设声明
references/validation-notes.md      不公开真人素材的端到端验证记录
assets/presets.json                 可扩展的机器可读导出清单
scripts/export_asset_pack.py        从四张母版生成精确尺寸素材包
scripts/validate_skill.py           无第三方依赖的仓库检查脚本
tests/test_export_asset_pack.py      尺寸、透明通道和路径安全回归测试
tests/test_skill_contract.py         风格、美化边界和动作库契约测试
requirements.txt                    导出脚本唯一依赖：Pillow
examples/requests.md                中英文调用示例
PRIVACY.md                          面向使用者的隐私说明
CONTRIBUTING.md                     贡献规范
SECURITY.md                         漏洞报告和照片安全边界
CHANGELOG.md                        版本变更记录
LICENSE                             MIT 许可证
```

## 能力与边界

- 需要运行环境具备参考图编辑能力；仅有文生图时，无法可靠保留人物相似度。
- 本项目不捆绑模型或图像服务，也不包含 API Key、模型权重或真人示例图。
- 图片会按你选择的生成服务处理；项目本身不搭服务器、不收集图片，也不宣称本地处理。
- 自动导出脚本只做裁切、缩放、透明合成、贴纸描边和版式摆放，不会凭算法修复一张已经“不像本人”的母版。

## 隐私

只处理你本人拥有或已获授权的照片。不要把用户照片、生成的人物肖像、私有图片链接或含个人信息的提示词提交到 Issue 或 Pull Request。公开分享前应确认授权并移除不必要的 EXIF 信息。完整说明见 [PRIVACY.md](PRIVACY.md)。

## 验证

```bash
python3 scripts/validate_skill.py .
```

结构检查不等于视觉效果通过。人物相似度仍需用有授权的照片在真实图像编辑环境中复验。

本仓库的公开验证记录见 [references/validation-notes.md](references/validation-notes.md)。真人照片和生成的人物肖像不会作为测试样例提交到仓库。

## License

[MIT](LICENSE) © 2026 Soya
