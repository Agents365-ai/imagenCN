# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Language

All code, comments, and documentation must be in English (README_CN.md is the sole exception — it is the Chinese companion to README.md).

## Git Commits

Do NOT add "Co-Authored-By: Claude" to commit messages.

## What This Is

A Claude Code skill for AI image generation using five Chinese T2I platforms:
- Alibaba Cloud Bailian (阿里云百炼) — DashScope API
- ByteDance Volcano Ark (火山方舟) — Seedream models
- Tencent Hunyuan (腾讯混元) — Hunyuan Image 3.0
- Zhipu / BigModel (智谱) — CogView-4, GLM-Image
- StepFun (阶跃星辰) — Step-2X, Step-Image-Edit-2

## Models

- **Qwen-Image (通义千问)**: Best for Chinese/English text rendering on images (DashScope)
- **Wan Series (通义万相)**: Best for photorealistic images and photography (DashScope)
- **Z-Image**: Lightweight, fast & low-cost (DashScope)
- **Seedream (豆包)**: Photo + text combo, up to 4K (Volcano Ark)
- **Hunyuan Image (混元生图)**: Complex Chinese composition, 8K-char prompts (Tencent Hunyuan)
- **CogView-4 (智谱)**: Native Chinese text in images (Zhipu)
- **Step-2X (阶跃星辰)**: Ultra-cheap volume generation (StepFun)

## Key Command

```bash
# Basic usage (from repo root)
python skills/imagenCN/scripts/generate_image.py "prompt" output.png

# With model and size (DashScope)
python skills/imagenCN/scripts/generate_image.py --model wan2.7-image-pro --size 16:9 "prompt" output.png

# Volcano Ark (ByteDance) — requires ARK_API_KEY
python skills/imagenCN/scripts/generate_image.py --platform ark "prompt" output.png

# Tencent Hunyuan — requires HUNYUAN_API_KEY
python skills/imagenCN/scripts/generate_image.py --platform hunyuan "prompt" output.png

# Zhipu / BigModel — requires ZHIPUAI_API_KEY
python skills/imagenCN/scripts/generate_image.py --platform zhipu "prompt" output.png

# StepFun — requires STEP_API_KEY
python skills/imagenCN/scripts/generate_image.py --platform stepfun "prompt" output.png

# List models (all 5 platforms)
python skills/imagenCN/scripts/generate_image.py --list-models
```

## Advanced Options

```bash
# Disable automatic prompt extension (DashScope only)
python skills/imagenCN/scripts/generate_image.py --no-extend "prompt" output.png

# Set random seed for reproducibility
python skills/imagenCN/scripts/generate_image.py --seed 42 "prompt" output.png

# Guidance scale (Volcano Ark only)
python skills/imagenCN/scripts/generate_image.py --platform ark --guidance-scale 7.5 "prompt" output.png

# Auto-enhance prompt (Tencent Hunyuan only)
python skills/imagenCN/scripts/generate_image.py --platform hunyuan --revise 0 "prompt" output.png

# Add AI logo (Tencent Hunyuan only)
python skills/imagenCN/scripts/generate_image.py --platform hunyuan --logo 1 "prompt" output.png

# Disable watermark (Volcano Ark only)
python skills/imagenCN/scripts/generate_image.py --platform ark --no-watermark "prompt" output.png

# Dry run (preview without generating)
python skills/imagenCN/scripts/generate_image.py --dry-run "prompt"
```

## Environment Variables

```bash
export DASHSCOPE_API_KEY="your_api_key"   # Required (DashScope)
export DASHSCOPE_MODEL="qwen-image-2.0-pro"  # Optional default model (DashScope)
export DASHSCOPE_API_BASE="cn"            # Optional: cn, sg, us (DashScope)

export ARK_API_KEY="your_api_key"         # Required (Volcano Ark)
export ARK_MODEL="doubao-seedream-5-0-260128"  # Optional default model (Ark)

export HUNYUAN_API_KEY="your_api_key"     # Required (Tencent Hunyuan)
export HUNYUAN_MODEL="hy-image-v3.0"      # Optional default model (Hunyuan)

export ZHIPUAI_API_KEY="your_api_key"     # Required (Zhipu)
export ZHIPUAI_MODEL="cogview-4"          # Optional default model (Zhipu)

export STEP_API_KEY="your_api_key"        # Required (StepFun)
export STEP_MODEL="step-2x-large"         # Optional default model (StepFun)
```

## Project Structure

```
imagenCN/
├── SKILL.md              # Main documentation (in skills/imagenCN/)
├── README.md             # English README
├── README_CN.md          # Chinese README
├── CLAUDE.md             # This file
├── assets/               # Workflow diagrams
└── skills/
    └── imagenCN/
        ├── SKILL.md
        └── scripts/
            ├── generate_image.py   # Main entry point
            ├── volcano_ark.py      # Volcano Ark platform module
            ├── hunyuan.py          # Tencent Hunyuan platform module
            ├── zhipu.py            # Zhipu platform module
            └── stepfun.py          # StepFun platform module
```
