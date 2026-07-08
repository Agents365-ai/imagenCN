# ImagenCN Model Reference

> Data source: [`models.json`](models.json) · Updated: 2026-07-08

## Quick Reference

| Use Case | Model | Platform |
|----------|-------|----------|
| Default / general | `qwen-image-2.0-pro` | DashScope |
| Photorealistic photos | `wan2.7-image-pro` | DashScope |
| Edit an image | `qwen-image-edit-max` | DashScope |
| Cheap & fast | `z-image-turbo` | DashScope |
| Photo + text combo | `doubao-seedream-5-0-260128` | Volcano Ark |
| Complex Chinese composition | `hy-image-v3.0` | Hunyuan |
| Chinese text in images | `cogview-4` | Zhipu |
| Ultra-cheap volume gen | `step-image-edit-2` | StepFun |

## Summary

| Platform | Models | Price Range | Max Res | Env Var |
|----------|--------|-------------|---------|---------|
| **DashScope** | 21 | ¥0.02–0.20 | 1K–4K | `DASHSCOPE_API_KEY` |
| **Volcano Ark** | 3 | ¥0.15–0.22 | 3K–4K | `ARK_API_KEY` |
| **Hunyuan** | 1 | ¥0.20 | 2K | `HUNYUAN_API_KEY` |
| **Zhipu** | 3 | ¥0.06–0.08 | 2K | `ZHIPUAI_API_KEY` |
| **StepFun** | 2 | ¥0.02–0.10 | 1K | `STEP_API_KEY` |

---

## Alibaba Cloud Bailian (DashScope) — 21 models

API: Native SDK (`dashscope`) · Endpoint: `https://dashscope.aliyuncs.com/api/v1` · Regions: cn, sg, us

| Model | Category | API | Price | Max Res | Notes |
|-------|----------|-----|-------|---------|-------|
| `qwen-image-2.0-pro` ★ | Qwen-Image 2.0 | MultiModalConversation | ¥0.12 | 2048×2048 | Default flagship, strongest typography |
| `qwen-image-2.0-pro-2026-06-22` | Qwen-Image 2.0 | MultiModalConversation | ¥0.12 | 2048×2048 | Latest snapshot, generation+editing fusion |
| `qwen-image-2.0` | Qwen-Image 2.0 | MultiModalConversation | ¥0.10 | 2048×2048 | Standard 2.0 tier |
| `qwen-image-max` | Qwen-Image 2.0 | MultiModalConversation | ¥0.10 | 2048×2048 | Previous-gen flagship |
| `qwen-image-max-2025-12-30` | Qwen-Image 2.0 | MultiModalConversation | ¥0.10 | 2048×2048 | Snapshot, improved realism |
| `qwen-image-edit-max` | Editing | MultiModalConversation | ¥0.12 | auto | Flagship editing, needs `--image` |
| `qwen-image-edit-max-2026-01-16` | Editing | MultiModalConversation | ¥0.12 | auto | Latest editing snapshot |
| `qwen-image-edit-plus` | Editing | MultiModalConversation | ¥0.06 | auto | Fast low-cost editing |
| `qwen-image-plus` | Legacy | ImageSynthesis | ¥0.04 | 1328×1328 | Distilled accelerated |
| `qwen-image-plus-2026-01-09` | Legacy | ImageSynthesis | ¥0.04 | 1328×1328 | Snapshot, fast high-quality |
| `qwen-image` | Legacy | ImageSynthesis | ¥0.04 | 1328×1328 | Base model |
| `z-image-turbo` | Z-Image | MultiModalConversation | ¥0.02 | 2048×2048 | Ultra-fast, cheapest |
| `wan2.7-image-pro` | Wan Series | ImageGeneration | ¥0.20 | 4K | Latest photorealistic, unified architecture |
| `wan2.7-image` | Wan Series | ImageGeneration | ¥0.12 | 2K | Wan 2.7 standard |
| `wan2.6-t2i` | Wan Series | ImageGeneration | ¥0.10 | 2K | Flexible sizing |
| `wan2.5-t2i-preview` | Wan Series | ImageGeneration | ¥0.10 | 768×2700 | High quality art |
| `wan2.2-t2i-flash` | Wan Series | ImageGeneration | ¥0.06 | 2K | Speed-optimized |
| `wan2.2-t2i-plus` | Wan Series | ImageGeneration | ¥0.10 | 2K | Professional tier |
| `wanx2.1-t2i-turbo` | Wan Series | ImageGeneration | ¥0.06 | 2K | Fast execution |
| `wanx2.1-t2i-plus` | Wan Series | ImageGeneration | ¥0.10 | 2K | Professional tier |
| `wanx2.0-t2i-turbo` | Wan Series | ImageGeneration | ¥0.06 | 2K | Earlier generation |

★ = default model

---

## ByteDance Volcano Ark — 3 models

API: OpenAI-compatible REST · Endpoint: `https://ark.cn-beijing.volces.com/api/v3/images/generations`

| Model | Category | Price | Max Res | Notes |
|-------|----------|-------|---------|-------|
| `doubao-seedream-5-0-260128` ★ | Seedream | ¥0.22 | 3K | Latest, PNG/JPEG, best text rendering |
| `doubao-seedream-4-5-251128` | Seedream | ¥0.22 | 4K | Seedream 4.5 |
| `doubao-seedream-4-0-250828` | Seedream | ¥0.15 | 4K | Budget-friendly 4K |

---

## Tencent Hunyuan — 1 model

API: OpenAI-compatible REST · Endpoint: `https://tokenhub.tencentmaas.com/v1/images/generations`

| Model | Category | Price | Max Res | Notes |
|-------|----------|-------|---------|-------|
| `hy-image-v3.0` ★ | Hunyuan | ¥0.20 | 2048×2048 | Flagship, 8K-char Chinese prompts |

---

## Zhipu / BigModel — 3 models

API: OpenAI-compatible REST · Endpoint: `https://api.z.ai/api/paas/v4/images/generations`

| Model | Category | Price | Max Res | Notes |
|-------|----------|-------|---------|-------|
| `cogview-4` ★ | CogView | ¥0.06 | 2048×2048 | Native Chinese text rendering |
| `cogview-4-250304` | CogView | ¥0.06 | 2048×2048 | Fixed snapshot, reproducible |
| `glm-image` | GLM | ¥0.08 | 2048×2048 | Hybrid autoregressive/diffusion |

---

## StepFun (阶跃星辰) — 2 models

API: OpenAI-compatible REST · Endpoint: `https://api.stepfun.com/v1/images/generations`

| Model | Category | Price | Max Res | Notes |
|-------|----------|-------|---------|-------|
| `step-2x-large` ★ | Step-2X | ¥0.10 | 1024×1024 | High quality, balanced |
| `step-image-edit-2` | Step-Edit | ¥0.02 | 1024×1024 | Ultra-cheap, negative prompts |

---

## How to Update

Edit [`docs/models.json`](models.json), then:

```bash
# After updating models.json, re-sync HTML (edit models.html DATA block)
# The markdown table can be regenerated from JSON if a build script is added
```

Long-term: a simple Node/Python script can regenerate both `models.html` and `models.md`
from `models.json`. For now, they are maintained manually in sync with the JSON source.
