#!/usr/bin/env python3
"""
ImagenCN - Alibaba Cloud Bailian Text-to-Image Script

Generate images using Alibaba Cloud DashScope API with Qwen-Image and Wan Series models.
Default endpoint is China region.

Usage:
    python generate_image.py "prompt" [output_path]
    python generate_image.py --model wan2.7-image-pro "prompt" output.png
    python generate_image.py --size 2K "prompt" output.png
    python generate_image.py --model qwen-image-edit-max --image input.png "edit instruction" output.png

Environment variables:
    DASHSCOPE_API_KEY (required) - Alibaba Cloud Bailian API Key
    DASHSCOPE_MODEL (optional) - Default model (default: qwen-image-2.0-pro)
    DASHSCOPE_API_BASE (optional) - API endpoint, defaults to China region

API Endpoints:
    China (default): https://dashscope.aliyuncs.com/api/v1
    Singapore: https://dashscope-intl.aliyuncs.com/api/v1
    Virginia: https://dashscope-us.aliyuncs.com/api/v1

Models:
    Qwen-Image 2.0 family (latest, native 2K) - uses MultiModalConversation:
        - qwen-image-2.0-pro (default, flagship)
        - qwen-image-2.0-pro-2026-06-22 (latest snapshot, generation + editing fusion)
        - qwen-image-2.0
        - qwen-image-max, qwen-image-max-2025-12-30

    Qwen-Image edit family (image editing, requires --image) - uses MultiModalConversation:
        - qwen-image-edit-max, qwen-image-edit-max-2026-01-16
        - qwen-image-edit-plus

    Z-Image (lightweight, fast & low-cost) - uses MultiModalConversation:
        - z-image-turbo

    Qwen-Image legacy (text rendering) - uses ImageSynthesis:
        - qwen-image-plus, qwen-image-plus-2026-01-09
        - qwen-image

    Wan Series (photorealistic) - uses ImageGeneration:
        - wan2.7-image-pro (latest, supports up to 4K)
        - wan2.7-image
        - wan2.6-t2i
        - wan2.5-t2i-preview
        - wan2.2-t2i-flash, wan2.2-t2i-plus
        - wanx2.1-t2i-turbo, wanx2.1-t2i-plus, wanx2.0-t2i-turbo
"""

import argparse
import os
import sys
from pathlib import Path
from http import HTTPStatus

try:
    import requests
    from dashscope import ImageSynthesis, MultiModalConversation
    from dashscope.aigc.image_generation import ImageGeneration
    import dashscope
except ImportError:
    print("Error: Required packages not installed", file=sys.stderr)
    print("\nInstall with:", file=sys.stderr)
    print("  pip install dashscope requests", file=sys.stderr)
    sys.exit(1)


DEFAULT_MODEL = "qwen-image-2.0-pro"
DEFAULT_SIZE = "2048*2048"

# API Endpoints
API_ENDPOINTS = {
    "cn": "https://dashscope.aliyuncs.com/api/v1",
    "sg": "https://dashscope-intl.aliyuncs.com/api/v1",
    "us": "https://dashscope-us.aliyuncs.com/api/v1",
}
DEFAULT_API_BASE = API_ENDPOINTS["cn"]

# Models using ImageSynthesis (legacy Qwen text rendering, prompt parameter)
SYNTHESIS_MODELS = {"qwen-image-plus", "qwen-image-plus-2026-01-09", "qwen-image"}

# Models using ImageGeneration (Wan series, messages format)
GENERATION_MODELS = {
    "wan2.7-image-pro", "wan2.7-image",
    "wan2.6-t2i", "wan2.5-t2i-preview",
    "wan2.2-t2i-flash", "wan2.2-t2i-plus",
    "wanx2.1-t2i-turbo", "wanx2.1-t2i-plus", "wanx2.0-t2i-turbo",
}

# Models using MultiModalConversation (Qwen-Image 2.0 family, native 2K)
MULTIMODAL_MODELS = {
    "qwen-image-2.0-pro", "qwen-image-2.0-pro-2026-06-22",
    "qwen-image-2.0", "qwen-image-max", "qwen-image-max-2025-12-30",
}

# Z-Image models (lightweight, fast) - also use MultiModalConversation
ZIMAGE_MODELS = {"z-image-turbo"}

# Qwen-Image edit models (image editing, require --image) - MultiModalConversation
EDIT_MODELS = {
    "qwen-image-edit-max", "qwen-image-edit-max-2026-01-16",
    "qwen-image-edit-plus",
}

# Size presets for Qwen-Image 2.0 family (native up to 2048x2048)
QWEN2_SIZES = {
    "1:1": "2048*2048",
    "16:9": "2688*1536",
    "9:16": "1536*2688",
    "4:3": "2304*1728",
    "3:4": "1728*2304",
    "1K": "1024*1024",
    "2K": "2048*2048",
}

# Size presets for legacy Qwen-Image / qwen-image-plus
QWEN_SIZES = {
    "1:1": "1328*1328",
    "16:9": "1664*928",
    "9:16": "928*1664",
    "4:3": "1472*1104",
    "3:4": "1104*1472",
}

# Size presets for Z-Image (pixel area must stay within 512x512 to 2048x2048)
ZIMAGE_SIZES = {
    "1:1": "1024*1024",
    "16:9": "1280*720",
    "9:16": "720*1280",
    "2:3": "1024*1536",
    "3:2": "1536*1024",
    "1K": "1024*1024",
}

# Size presets for Wan series. Wan2.7 also accepts shorthand "1K"/"2K"/"4K".
WAN_SIZES = {
    "1:1": "1024*1024",
    "1:1-large": "1280*1280",
    "16:9": "1280*720",
    "9:16": "720*1280",
    "4:3": "1200*900",
    "3:4": "900*1200",
    "2:1": "1440*720",
    "1K": "1K",
    "2K": "2K",
    "4K": "4K",
}


def get_api_key():
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("Error: DASHSCOPE_API_KEY environment variable not set", file=sys.stderr)
        print("\nTo set it:", file=sys.stderr)
        print("  Windows (PowerShell): $env:DASHSCOPE_API_KEY = 'your-key'", file=sys.stderr)
        print("  Windows (CMD): set DASHSCOPE_API_KEY=your-key", file=sys.stderr)
        print("  macOS/Linux: export DASHSCOPE_API_KEY='your-key'", file=sys.stderr)
        print("\nGet API key at: https://bailian.console.aliyun.com/", file=sys.stderr)
        sys.exit(1)
    return api_key


def get_api_base():
    base = os.environ.get("DASHSCOPE_API_BASE", DEFAULT_API_BASE)
    if base in API_ENDPOINTS:
        return API_ENDPOINTS[base]
    return base


def resolve_size(size_input, model):
    if model in EDIT_MODELS:
        # No default: let the API match the input image dimensions
        if not size_input:
            return None
        return size_input.replace("x", "*")
    if model in MULTIMODAL_MODELS:
        sizes = QWEN2_SIZES
        default = "2048*2048"
    elif model in ZIMAGE_MODELS:
        sizes = ZIMAGE_SIZES
        default = "1024*1024"
    elif model in SYNTHESIS_MODELS:
        sizes = QWEN_SIZES
        default = "1328*1328"
    else:
        sizes = WAN_SIZES
        default = "1024*1024"
    if not size_input:
        return default
    if size_input in sizes:
        return sizes[size_input]
    if "*" in size_input or "x" in size_input:
        return size_input.replace("x", "*")
    return size_input


def create_output_dir(output_path):
    output_dir = output_path.parent
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)


def generate_with_synthesis(api_key, model, prompt, size, negative_prompt=None):
    """Generate image using ImageSynthesis (for qwen-image-plus)."""
    params = {
        "api_key": api_key,
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size,
        "prompt_extend": True,
        "watermark": False,
    }
    if negative_prompt:
        params["negative_prompt"] = negative_prompt
    return ImageSynthesis.call(**params)


def generate_with_generation(api_key, model, prompt, size, negative_prompt=None):
    """Generate image using ImageGeneration (for wan2.6-t2i, wan2.7-image, etc)."""
    messages = [{"role": "user", "content": [{"text": prompt}]}]
    params = {
        "api_key": api_key,
        "model": model,
        "messages": messages,
        "n": 1,
        "size": size,
        "prompt_extend": True,
        "watermark": False,
    }
    if negative_prompt:
        params["negative_prompt"] = negative_prompt
    return ImageGeneration.call(**params)


def generate_with_multimodal(api_key, model, prompt, size, negative_prompt=None, image=None):
    """Generate image using MultiModalConversation (qwen-image-2.0/edit family, z-image)."""
    content = []
    if image:
        content.append({"image": image})
    content.append({"text": prompt})
    messages = [{"role": "user", "content": content}]
    params = {
        "api_key": api_key,
        "model": model,
        "messages": messages,
        "n": 1,
        "prompt_extend": True,
        "watermark": False,
    }
    if size:
        params["size"] = size
    if negative_prompt:
        params["negative_prompt"] = negative_prompt
    return MultiModalConversation.call(**params)


def extract_image_url(rsp, model):
    """Extract image URL from response based on model type."""
    if model in SYNTHESIS_MODELS:
        if rsp.output and rsp.output.results:
            return rsp.output.results[0].url
    # ImageGeneration and MultiModalConversation share the choices/message format
    if hasattr(rsp, 'output') and rsp.output:
        choices = rsp.output.get('choices', [])
        if choices:
            content = choices[0].get('message', {}).get('content', [])
            for item in content:
                if 'image' in item:
                    return item['image']
    return None


def save_image(url, output_path):
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        output_path.write_bytes(response.content)
        return True
    except Exception as e:
        print(f"Error: Failed to download image: {e}", file=sys.stderr)
        return False


def get_file_size(path):
    size = path.stat().st_size
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def list_models():
    print("Available models:\n")
    print("Qwen-Image 2.0 family (native 2K) [MultiModalConversation API]:")
    for m in sorted(MULTIMODAL_MODELS):
        default = " (default)" if m == DEFAULT_MODEL else ""
        print(f"  - {m}{default}")
    print("\nQwen-Image edit family (image editing, requires --image) [MultiModalConversation API]:")
    for m in sorted(EDIT_MODELS):
        print(f"  - {m}")
    print("\nZ-Image (lightweight, fast & low-cost) [MultiModalConversation API]:")
    for m in sorted(ZIMAGE_MODELS):
        default = " (default)" if m == DEFAULT_MODEL else ""
        print(f"  - {m}{default}")
    print("\nQwen-Image legacy (text rendering) [ImageSynthesis API]:")
    for m in sorted(SYNTHESIS_MODELS):
        default = " (default)" if m == DEFAULT_MODEL else ""
        print(f"  - {m}{default}")
    print("\nWan Series (photorealistic) [ImageGeneration API]:")
    for m in sorted(GENERATION_MODELS):
        default = " (default)" if m == DEFAULT_MODEL else ""
        print(f"  - {m}{default}")
    print("\nSize presets:")
    print("  Qwen-Image 2.0:", ", ".join(QWEN2_SIZES.keys()))
    print("  Z-Image:", ", ".join(ZIMAGE_SIZES.keys()))
    print("  Qwen-Image legacy:", ", ".join(QWEN_SIZES.keys()))
    print("  Wan Series:", ", ".join(WAN_SIZES.keys()))
    print("\nAPI endpoints:")
    for region, url in API_ENDPOINTS.items():
        default = " (default)" if region == "cn" else ""
        print(f"  - {region}: {url}{default}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Alibaba Cloud Bailian API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "A cute cat"
  %(prog)s --model wan2.6-t2i "Mountain landscape photo" ./landscape.png
  %(prog)s --size 16:9 "Widescreen wallpaper" ./wallpaper.png
  %(prog)s --list-models
        """
    )
    parser.add_argument("prompt", nargs="?", help="Text description of the image")
    parser.add_argument("output", nargs="?", default="./generated-image.png",
                        help="Output file path (default: ./generated-image.png)")
    parser.add_argument("--model", "-m", help=f"Model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--size", "-s", help="Image size as ratio or pixels")
    parser.add_argument("--negative", "-n", help="Negative prompt")
    parser.add_argument("--image", "-i", help="Input image (path or URL) for editing models")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    args = parser.parse_args()

    if args.list_models:
        list_models()
        return

    if not args.prompt:
        parser.print_help()
        sys.exit(1)

    api_key = get_api_key()
    model = args.model or os.environ.get("DASHSCOPE_MODEL", DEFAULT_MODEL)
    size = resolve_size(args.size, model)
    output_path = Path(args.output)

    all_models = SYNTHESIS_MODELS | GENERATION_MODELS | MULTIMODAL_MODELS | ZIMAGE_MODELS | EDIT_MODELS
    if model not in all_models:
        print(f"Warning: Unknown model '{model}'. Using {DEFAULT_MODEL}", file=sys.stderr)
        model = DEFAULT_MODEL
        size = resolve_size(args.size, model)

    input_image = args.image
    if model in EDIT_MODELS and not input_image:
        print(f"Error: Model '{model}' is an editing model and requires --image", file=sys.stderr)
        sys.exit(1)
    if input_image and os.path.exists(input_image):
        input_image = f"file://{Path(input_image).resolve()}"

    create_output_dir(output_path)
    dashscope.base_http_api_url = get_api_base()

    if model in SYNTHESIS_MODELS:
        api_type = "ImageSynthesis"
    elif model in MULTIMODAL_MODELS or model in ZIMAGE_MODELS or model in EDIT_MODELS:
        api_type = "MultiModalConversation"
    else:
        api_type = "ImageGeneration"
    print(f"Generating image...")
    print(f"Prompt: \"{args.prompt}\"")
    print(f"Model: {model} ({api_type})")
    if input_image:
        print(f"Input image: {args.image}")
    print(f"Size: {size or 'auto (match input image)'}")
    print(f"Endpoint: {dashscope.base_http_api_url}")
    print(f"Output: {output_path}")
    print()

    try:
        if model in SYNTHESIS_MODELS:
            rsp = generate_with_synthesis(api_key, model, args.prompt, size, args.negative)
        elif model in MULTIMODAL_MODELS or model in ZIMAGE_MODELS or model in EDIT_MODELS:
            rsp = generate_with_multimodal(api_key, model, args.prompt, size, args.negative,
                                           image=input_image)
        else:
            rsp = generate_with_generation(api_key, model, args.prompt, size, args.negative)
    except Exception as e:
        print(f"Error: API call failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Check response status
    if hasattr(rsp, 'status_code') and rsp.status_code != HTTPStatus.OK:
        print(f"Error: API returned {rsp.status_code}", file=sys.stderr)
        if hasattr(rsp, 'code'):
            print(f"Code: {rsp.code}", file=sys.stderr)
        if hasattr(rsp, 'message'):
            print(f"Message: {rsp.message}", file=sys.stderr)
        sys.exit(1)

    # Extract and save image
    image_url = extract_image_url(rsp, model)
    if not image_url:
        print("Error: No image URL in response", file=sys.stderr)
        print(f"Response: {rsp}", file=sys.stderr)
        sys.exit(1)

    if not save_image(image_url, output_path):
        sys.exit(1)

    if output_path.exists() and output_path.stat().st_size > 0:
        file_size = get_file_size(output_path)
        print("Success! Image generated and saved.")
        print(f"File: {output_path}")
        print(f"Size: {file_size}")
    else:
        print(f"Error: Failed to save image to {output_path}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
