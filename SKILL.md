---
name: imagenCN
description: Use when generating images with Alibaba Cloud Bailian API, especially for Chinese text rendering or photorealistic images
author: Agents365-ai
created: 2024-12-01
updated: 2026-07-05
homepage: https://github.com/Agents365-ai/imagenCN
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["DASHSCOPE_API_KEY"]},"primaryEnv":"DASHSCOPE_API_KEY","emoji":"🎨"}}
---

# ImagenCN - Alibaba Cloud Bailian Text-to-Image Skill

## Overview

Generate images using Alibaba Cloud Bailian API. **Default endpoint is China region**.

Supports five model families:
- **Qwen-Image 2.0** (latest, native 2K): Flagship general-purpose generator with strong text rendering
- **Qwen-Image Edit**: Instruction-based image editing (requires an input image)
- **Qwen-Image legacy**: Lighter Chinese/English text rendering models
- **Wan Series**: Photorealistic images and photography-grade visuals (Wan2.7 supports up to 4K)
- **Z-Image**: Lightweight, fast and low-cost; strong at high-fidelity portraits and product shots

**Cross-platform support**: Windows, macOS, Linux

## When to Use This Skill

Automatically activate this skill when:
- User requests image generation with Chinese text or calligraphy
- Need photorealistic images or photography-style visuals
- Creating commercial posters, illustrations, or digital art
- User explicitly requests Alibaba Cloud / Bailian / Qwen / Wan models
- Any task where AI-generated image with strong Chinese support would be helpful

## Workflow

1. Pick a model based on the request (see Model Selection Guide below). Default to `qwen-image-2.0-pro` if unsure.
2. Pick a size: native 2K for the Qwen-Image 2.0 family, `1K`/`2K`/`4K` for Wan2.7, or an aspect-ratio preset (`16:9`, `1:1`, etc.).
3. Run `scripts/generate_image.py` with the prompt and output path.
4. If the output path was implicit, save into the user's current working directory.

## Models

### Qwen-Image 2.0 family - Latest Flagship (MultiModalConversation API)

| Model | Description |
|-------|-------------|
| `qwen-image-2.0-pro` | **Default**. Latest flagship, native 2K, strongest typography and detail |
| `qwen-image-2.0-pro-2026-06-22` | Latest snapshot (Jun 2026): generation + editing fusion, better text rendering and prompt adherence |
| `qwen-image-2.0` | Standard 2.0 tier, native 2K |
| `qwen-image-max` | Previous-gen flagship (Dec 2025) |
| `qwen-image-max-2025-12-30` | qwen-image-max snapshot: improved realism, fewer AI artifacts |

### Qwen-Image Edit family - Image Editing (MultiModalConversation API)

Editing models require an input image via `--image` (local path or URL). Omit `--size` to match the input image dimensions.

| Model | Description |
|-------|-------------|
| `qwen-image-edit-max` | Flagship editing model, strongest instruction following |
| `qwen-image-edit-max-2026-01-16` | Latest max snapshot (Jan 2026) |
| `qwen-image-edit-plus` | Faster, lower-cost editing |

### Qwen-Image legacy (ImageSynthesis API)

| Model | Description |
|-------|-------------|
| `qwen-image-plus` | Distilled accelerated version of qwen-image-max |
| `qwen-image-plus-2026-01-09` | qwen-image-plus snapshot (Jan 2026): faster high-quality generation |
| `qwen-image` | Base model |

### Wan Series - Photorealistic Generation (ImageGeneration API)

| Model | Description |
|-------|-------------|
| `wan2.7-image-pro` | **Latest**. Up to 4K output, unified architecture (T2I + edit + multi-image) |
| `wan2.7-image` | Wan 2.7 standard, up to 2K |
| `wan2.6-t2i` | Wan 2.6, flexible sizing |
| `wan2.5-t2i-preview` | High quality, up to 768x2700 |
| `wan2.2-t2i-flash` | Speed-optimized |
| `wan2.2-t2i-plus` | Professional tier |
| `wanx2.1-t2i-turbo` | Fast execution |
| `wanx2.1-t2i-plus` | Professional tier |
| `wanx2.0-t2i-turbo` | Earlier generation |

### Z-Image - Lightweight & Fast (MultiModalConversation API)

| Model | Description |
|-------|-------------|
| `z-image-turbo` | Fast, low-cost generation; bilingual (CN/EN) text rendering, high-fidelity portraits and product images. Pixel area 512x512 to 2048x2048 |

## Usage

### Basic Usage

```bash
# Default model (qwen-image-2.0-pro, native 2K output)
python ~/.claude/skills/imagenCN/scripts/generate_image.py "A cute cat" output.png

# Photorealistic with Wan model (Wan2.7 supports 4K)
python ~/.claude/skills/imagenCN/scripts/generate_image.py --model wan2.7-image-pro --size 4K "Realistic photo of mountains at sunset" photo.png

# Edit an existing image (requires --image; local path or URL)
python ~/.claude/skills/imagenCN/scripts/generate_image.py --model qwen-image-edit-max --image input.png "Change the background to a beach at sunset" edited.png
```

### Size Options

```bash
# Use ratio preset
python ~/.claude/skills/imagenCN/scripts/generate_image.py --size 16:9 "Wide landscape" landscape.png

# Use exact dimensions
python ~/.claude/skills/imagenCN/scripts/generate_image.py --size 1280*720 "Custom size" custom.png
```

### Size Presets

**Qwen-Image 2.0 (native 2K):**
- `1:1` -> 2048x2048 (default)
- `16:9` -> 2688x1536
- `9:16` -> 1536x2688
- `4:3` -> 2304x1728
- `3:4` -> 1728x2304
- `1K` -> 1024x1024
- `2K` -> 2048x2048

**Qwen-Image legacy:**
- `1:1` -> 1328x1328
- `16:9` -> 1664x928
- `9:16` -> 928x1664
- `4:3` -> 1472x1104
- `3:4` -> 1104x1472

**Z-Image (pixel area 512x512 to 2048x2048):**
- `1:1` -> 1024x1024 (default)
- `16:9` -> 1280x720
- `9:16` -> 720x1280
- `2:3` -> 1024x1536
- `3:2` -> 1536x1024
- `1K` -> 1024x1024

**Wan Series (Wan2.7 also accepts `1K`/`2K`/`4K`):**
- `1:1` -> 1024x1024
- `1:1-large` -> 1280x1280
- `16:9` -> 1280x720
- `9:16` -> 720x1280
- `4:3` -> 1200x900
- `3:4` -> 900x1200
- `2:1` -> 1440x720

### Advanced Options

```bash
# With negative prompt
python ~/.claude/skills/imagenCN/scripts/generate_image.py --negative "blurry, low quality" "High quality portrait" portrait.png

# List all models
python ~/.claude/skills/imagenCN/scripts/generate_image.py --list-models
```

## Requirements

```bash
pip install dashscope requests
```

## Environment Variables

```bash
# Required - Alibaba Cloud Bailian API Key
export DASHSCOPE_API_KEY="your_api_key"

# Optional - Set default model
export DASHSCOPE_MODEL="wan2.7-image-pro"

# Optional - Set API endpoint (default: China)
export DASHSCOPE_API_BASE="cn"  # or full URL
```

Get API Key: https://bailian.console.aliyun.com/

## API Endpoints

| Region | Alias | URL |
|--------|-------|-----|
| **China** (default) | `cn` | `https://dashscope.aliyuncs.com/api/v1` |
| Singapore | `sg` | `https://dashscope-intl.aliyuncs.com/api/v1` |
| Virginia | `us` | `https://dashscope-us.aliyuncs.com/api/v1` |

```bash
# Switch to Singapore endpoint
export DASHSCOPE_API_BASE="sg"

# Or use full URL
export DASHSCOPE_API_BASE="https://dashscope-intl.aliyuncs.com/api/v1"
```

## Model Selection Guide

| Use Case | Recommended Model |
|----------|-------------------|
| General high-quality (default) | `qwen-image-2.0-pro` |
| Chinese text/calligraphy | `qwen-image-2.0-pro` |
| English text on images | `qwen-image-2.0-pro` |
| Posters with typography | `qwen-image-2.0-pro` |
| Photorealistic photos (4K) | `wan2.7-image-pro` |
| Photorealistic photos (2K) | `wan2.7-image` |
| Portrait photography | `wan2.7-image-pro` |
| Image editing (best quality) | `qwen-image-edit-max` |
| Image editing (fast, low-cost) | `qwen-image-edit-plus` |
| Fast, low-cost generation | `z-image-turbo` |
| High-fidelity portraits / product shots (fast) | `z-image-turbo` |
| Fast photorealistic (Wan) | `wan2.2-t2i-flash` |
| Lower-cost text rendering | `qwen-image-plus` |

## Comparison with Imagen (Gemini)

| Feature | ImagenCN (Bailian) | Imagen (Gemini) |
|---------|-------------------|-----------------|
| Chinese text rendering | Excellent | Good |
| English text rendering | Excellent | Good |
| Photorealistic images | Excellent | Good |
| Speed | Medium | Fast |
| Model variety | 15+ models | 3 models |
| Max resolution | 4K (Wan2.7-Pro) | 2K |

## Examples

### Chinese New Year Poster
```bash
python ~/.claude/skills/imagenCN/scripts/generate_image.py \
  "A beautiful Chinese New Year poster with red background, golden text, fireworks and firecrackers" \
  new_year_poster.png
```

### Photorealistic Landscape (4K)
```bash
python ~/.claude/skills/imagenCN/scripts/generate_image.py \
  --model wan2.7-image-pro \
  --size 4K \
  "Breathtaking sunset over mountain range, golden hour, professional photography" \
  landscape.png
```

### Product Shot
```bash
python ~/.claude/skills/imagenCN/scripts/generate_image.py \
  --model wan2.7-image \
  --size 2K \
  "Professional product photography of a coffee cup on marble surface, studio lighting" \
  product.png
```
