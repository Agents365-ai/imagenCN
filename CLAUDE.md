# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Language

All code, comments, and documentation must be in English.

## Git Commits

Do NOT add "Co-Authored-By: Claude" to commit messages.

## What This Is

A Claude Code skill for AI image generation using Alibaba Cloud Bailian (阿里云百炼) API.

## Models

- **Qwen-Image (通义千问)**: Best for Chinese/English text rendering on images
- **Wan Series (通义万相)**: Best for photorealistic images and photography

## Key Command

```bash
# Basic usage
python scripts/generate_image.py "prompt" output.png

# With model and size
python scripts/generate_image.py --model wan2.6-t2i --size 16:9 "prompt" output.png

# List models
python scripts/generate_image.py --list-models
```

## Environment Variables

```bash
export DASHSCOPE_API_KEY="your_api_key"  # Required
export DASHSCOPE_MODEL="qwen-image-plus"  # Optional default model
export DASHSCOPE_API_BASE="cn"            # Optional: cn, sg, us
```

## Project Structure

```
imagenCN/
├── SKILL.md              # Main documentation
├── scripts/
│   └── generate_image.py # Image generation script
└── CLAUDE.md             # This file
```
