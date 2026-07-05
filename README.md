# Imagen-Qwen — AI Image Generation with Chinese Text Excellence

[中文文档](README_CN.md)

A Claude Code / OpenClaw skill for AI image generation using Alibaba Cloud Bailian API.

## Why This Skill?

| Feature | This Skill | Native Claude Code | Other Image Skills |
|---------|-----------|-------------------|-------------------|
| **Chinese text rendering** | ✓ Qwen-Image optimized | ✗ No image generation | Partial |
| **Photorealistic images** | ✓ Wan series multi-model | ✗ No image generation | Partial |
| **Multi-model selection** | ✓ 15+ models to choose from | ✗ N/A | Usually single model |
| **Size presets** | ✓ 7+ aspect ratios | ✗ N/A | Partial |
| **Negative prompts** | ✓ Fine-grained control | ✗ N/A | Partial |
| **CLI direct invocation** | ✓ Script ready to use | ✗ N/A | Requires custom code |
| **Multi-region API** | ✓ China/Singapore/Virginia | ✗ N/A | Usually single region |

**Key advantages:**
- **Best Chinese text** — Qwen-Image is one of the best models for rendering Chinese text on images
- **Realism + art** — Wan series covers everything from quick drafts to professional-grade output
- **Ready to use** — `pip install` two packages + one API key to get started

## Features

- **Qwen-Image 2.0**: Latest flagship, native 2K, professional typography rendering
- **Qwen-Image legacy**: Lighter Chinese/English text rendering models
- **Wan Series**: Photorealistic images and photography-grade visuals, Wan2.7 supports 4K
- **Z-Image**: Lightweight, fast and low-cost; high-fidelity portraits and product shots
- **Multiple size presets**: 1:1, 16:9, 9:16, 4:3, 3:4, plus 1K/2K/4K
- **Cross-platform**: Windows, macOS, Linux support
- **Multiple API regions**: China (default), Singapore, Virginia

## Install the Skill

**Claude Code (global):**
```bash
git clone https://github.com/Agents365-ai/imagen-qwen.git ~/.claude/skills/imagen-qwen
```

**Claude Code (project-specific):**
```bash
git clone https://github.com/Agents365-ai/imagen-qwen.git .claude/skills/imagen-qwen
```

**OpenClaw:**
```bash
git clone https://github.com/Agents365-ai/imagen-qwen.git skills/imagen-qwen
```

**SkillsMP:** Search `imagen-qwen` on [skillsmp.com](https://skillsmp.com) for one-click install.

## Requirements

### System Requirements

- Python 3.8+
- pip

### Install Dependencies

```bash
pip install dashscope requests
```

### API Key

Get your API key from [Alibaba Cloud Bailian Console](https://bailian.console.aliyun.com/)

```bash
export DASHSCOPE_API_KEY="your_api_key"
```

### Optional Environment Variables

```bash
# Set default model (default: qwen-image-2.0-pro)
export DASHSCOPE_MODEL="wan2.7-image-pro"

# Set API endpoint (default: cn)
export DASHSCOPE_API_BASE="cn"  # or "sg", "us", or full URL
```

## Quick Start

### Natural Language (Claude Code)

Just tell Claude what you want:

```
Generate an image of a cute orange cat
Create a poster with text "Happy New Year" in Chinese
Make a photorealistic 4K mountain sunset photo using wan2.7-image-pro
Generate a 16:9 landscape wallpaper
```

### Command Line

```bash
# Basic usage (default model: qwen-image-2.0-pro, native 2K)
python ~/.claude/skills/imagen-qwen/scripts/generate_image.py "A cute cat" output.png

# Photorealistic 4K with Wan2.7
python ~/.claude/skills/imagen-qwen/scripts/generate_image.py --model wan2.7-image-pro --size 4K "Mountain sunset" photo.png

# Custom size
python ~/.claude/skills/imagen-qwen/scripts/generate_image.py --size 16:9 "Wide landscape" landscape.png

# With negative prompt
python ~/.claude/skills/imagen-qwen/scripts/generate_image.py --negative "blurry" "High quality portrait" portrait.png

# List available models
python ~/.claude/skills/imagen-qwen/scripts/generate_image.py --list-models
```

## Models

| Model | Best For |
|-------|----------|
| `qwen-image-2.0-pro` | **Default**, latest flagship, native 2K, strongest typography and detail |
| `qwen-image-2.0-pro-2026-06-22` | Latest snapshot (Jun 2026), generation + editing fusion |
| `qwen-image-2.0` | Standard 2.0 tier, native 2K |
| `qwen-image-max` | Previous-gen flagship |
| `qwen-image-plus` | Distilled accelerated version |
| `qwen-image` | Base model |
| `wan2.7-image-pro` | Latest photorealistic, up to 4K output |
| `wan2.7-image` | Wan 2.7 standard, up to 2K |
| `wan2.6-t2i` | Wan 2.6, flexible sizing |
| `wan2.5-t2i-preview` | High quality art |
| `wan2.2-t2i-flash` | Fast generation |
| `wan2.2-t2i-plus` | Professional tier |
| `wanx2.1-t2i-turbo` | Fast execution |
| `wanx2.1-t2i-plus` | Professional tier |
| `wanx2.0-t2i-turbo` | Earlier generation |
| `z-image-turbo` | Lightweight, fast & low-cost; portraits and product images |

## Size Presets

**Qwen-Image 2.0 (native 2K):**
- `1:1` → 2048×2048 (default)
- `16:9` → 2688×1536
- `9:16` → 1536×2688
- `4:3` → 2304×1728
- `3:4` → 1728×2304
- `1K` → 1024×1024
- `2K` → 2048×2048

**Qwen-Image legacy:**
- `1:1` → 1328×1328
- `16:9` → 1664×928
- `9:16` → 928×1664
- `4:3` → 1472×1104
- `3:4` → 1104×1472

**Z-Image (pixel area 512×512 to 2048×2048):**
- `1:1` → 1024×1024 (default)
- `16:9` → 1280×720
- `9:16` → 720×1280
- `2:3` → 1024×1536
- `3:2` → 1536×1024

**Wan Series (Wan2.7 also accepts `1K`/`2K`/`4K`):**
- `1:1` → 1024×1024
- `1:1-large` → 1280×1280
- `16:9` → 1280×720
- `9:16` → 720×1280
- `4:3` → 1200×900
- `3:4` → 900×1200
- `2:1` → 1440×720

## API Endpoints

| Region | Alias | URL |
|--------|-------|-----|
| **China** (default) | `cn` | `https://dashscope.aliyuncs.com/api/v1` |
| Singapore | `sg` | `https://dashscope-intl.aliyuncs.com/api/v1` |
| Virginia | `us` | `https://dashscope-us.aliyuncs.com/api/v1` |

## License

MIT License

## Support

If this project helps you, consider supporting the author:

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/wechat-pay.png" width="180" alt="WeChat Pay">
      <br>
      <b>WeChat Pay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/alipay.png" width="180" alt="Alipay">
      <br>
      <b>Alipay</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/buymeacoffee.png" width="180" alt="Buy Me a Coffee">
      <br>
      <b>Buy Me a Coffee</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/awarding/award.gif" width="180" alt="Give a Reward">
      <br>
      <b>Give a Reward</b>
    </td>
  </tr>
</table>

## Author

**Agents365-ai**

- Bilibili: https://space.bilibili.com/441831884
- GitHub: https://github.com/Agents365-ai
