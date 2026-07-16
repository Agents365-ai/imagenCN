"""Unit tests for imagenCN providers — exceptions, size resolution,
generation, error formatting, backward-compatible exports.

Run with: python -m pytest tests/ -v
"""

import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# Allow imports from the scripts package (repo_root/skills/imagenCN/scripts)
_repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_repo_root / "skills" / "imagenCN" / "scripts"))

from providers.base import (
    OpenAICompatibleProvider, ConfigError, APIError, IOError_, ImageGenError,
    safe_request, safe_json,
)


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------

class TestExceptions:
    def test_config_error(self):
        e = ConfigError("missing key")
        assert isinstance(e, ImageGenError)
        assert e.exit_code == 2

    def test_api_error(self):
        e = APIError("api fail")
        assert isinstance(e, ImageGenError)
        assert e.exit_code == 3

    def test_io_error(self):
        e = IOError_("write fail")
        assert isinstance(e, ImageGenError)
        assert e.exit_code == 4


# ---------------------------------------------------------------------------
# Size resolution
# ---------------------------------------------------------------------------

class TestSizeResolution:
    def test_ark_default(self):
        from volcano_ark import resolve_ark_size
        assert resolve_ark_size(None) == "2048x2048"

    def test_ark_preset(self):
        from volcano_ark import resolve_ark_size
        assert resolve_ark_size("16:9") == "2848x1600"

    def test_ark_custom_star_separator(self):
        from volcano_ark import resolve_ark_size
        assert resolve_ark_size("1024*768") == "1024x768"

    def test_hunyuan_colon_format(self):
        from hunyuan import resolve_hunyuan_size
        assert resolve_hunyuan_size(None) == "1024:1024"
        assert resolve_hunyuan_size("16:9") == "1920:1080"
        assert resolve_hunyuan_size("1024*768") == "1024:768"

    def test_zhipu_default(self):
        from zhipu import resolve_zhipu_size
        assert resolve_zhipu_size(None) == "1024x1024"

    def test_stepfun_default(self):
        from stepfun import resolve_stepfun_size
        assert resolve_stepfun_size(None) == "1024x1024"

    def test_gemini_named_and_ratio(self):
        from gemini import resolve_gemini_size
        assert resolve_gemini_size(None) == "1K"
        assert resolve_gemini_size("2K") == "2K"
        assert resolve_gemini_size("16:9") == "16:9"


# ---------------------------------------------------------------------------
# Model sets
# ---------------------------------------------------------------------------

class TestModelSets:
    def test_ark_models(self):
        from volcano_ark import ARK_MODELS
        assert "doubao-seedream-5-0-260128" in ARK_MODELS
        assert len(ARK_MODELS) == 3

    def test_hunyuan_models(self):
        from hunyuan import HUNYUAN_MODELS
        assert "hy-image-v3.0" in HUNYUAN_MODELS

    def test_zhipu_models(self):
        from zhipu import ZHIPU_MODELS
        assert "cogview-4" in ZHIPU_MODELS
        assert "glm-image" in ZHIPU_MODELS

    def test_stepfun_models(self):
        from stepfun import STEPFUN_MODELS
        assert "step-2x-large" in STEPFUN_MODELS

    def test_gemini_models(self):
        from gemini import GEMINI_MODELS
        assert "gemini-3-pro-image-preview" in GEMINI_MODELS


# ---------------------------------------------------------------------------
# API key handling
# ---------------------------------------------------------------------------

class TestApiKey:
    def test_missing_key_raises_config_error(self):
        p = OpenAICompatibleProvider()
        p.env_var = "NONEXISTENT_KEY_12345"
        with pytest.raises(ConfigError, match="NONEXISTENT_KEY_12345"):
            p.get_api_key()

    def test_existing_key_returns_value(self):
        p = OpenAICompatibleProvider()
        p.env_var = "TEST_KEY"
        os.environ["TEST_KEY"] = "test-value-123"
        try:
            assert p.get_api_key() == "test-value-123"
        finally:
            del os.environ["TEST_KEY"]

    def test_gemini_missing_key_raises_config_error(self):
        from gemini import get_gemini_api_key
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("GEMINI_API_KEY", None)
            with pytest.raises(ConfigError, match="GEMINI_API_KEY"):
                get_gemini_api_key()


# ---------------------------------------------------------------------------
# Generation (mocked HTTP)
# ---------------------------------------------------------------------------

class TestGeneration:
    def test_generate_success(self):
        p = OpenAICompatibleProvider()
        p.name = "Test"
        p.api_base = "https://test.example.com/v1/images/generations"
        mock_rsp = MagicMock()
        mock_rsp.status_code = 200
        mock_rsp.json.return_value = {"data": [{"url": "https://cdn.example.com/img.png"}]}

        with patch("providers.base.requests") as mock_requests:
            mock_requests.request.return_value = mock_rsp
            url = p.generate("key123", "model-x", "a cat", "1024x1024")
            assert url == "https://cdn.example.com/img.png"

    def test_generate_http_error_raises_api_error(self):
        p = OpenAICompatibleProvider()
        p.name = "Test"
        p.api_base = "https://test.example.com/v1/images/generations"
        mock_rsp = MagicMock()
        mock_rsp.status_code = 401
        mock_rsp.text = "Unauthorized"

        with patch("providers.base.requests") as mock_requests:
            mock_requests.request.return_value = mock_rsp
            with pytest.raises(APIError):
                p.generate("bad-key", "model-x", "a cat", "1024x1024")

    def test_generate_malformed_response_raises(self):
        p = OpenAICompatibleProvider()
        p.name = "Test"
        p.api_base = "https://test.example.com/v1/images/generations"
        mock_rsp = MagicMock()
        mock_rsp.status_code = 200
        mock_rsp.json.return_value = {"data": []}  # no url

        with patch("providers.base.requests") as mock_requests:
            mock_requests.request.return_value = mock_rsp
            with pytest.raises(APIError):
                p.generate("key", "model-x", "a cat", "1024x1024")

    def test_gemini_generate_returns_decoded_bytes(self):
        import base64
        from gemini import generate_with_gemini
        mock_rsp = MagicMock()
        mock_rsp.status_code = 200
        mock_rsp.json.return_value = {"candidates": [{"content": {"parts": [
            {"inlineData": {"data": base64.b64encode(b"png-bytes").decode()}}
        ]}}]}

        with patch("providers.base.requests") as mock_requests:
            mock_requests.request.return_value = mock_rsp
            out = generate_with_gemini("key", "gemini-3-pro-image-preview",
                                       "a cat", "1K")
            assert out == b"png-bytes"

    def test_gemini_generate_no_image_raises(self):
        from gemini import generate_with_gemini
        mock_rsp = MagicMock()
        mock_rsp.status_code = 200
        mock_rsp.json.return_value = {"candidates": [{"content": {"parts": [
            {"text": "blocked"}
        ]}}]}

        with patch("providers.base.requests") as mock_requests:
            mock_requests.request.return_value = mock_rsp
            with pytest.raises(APIError, match="no image data"):
                generate_with_gemini("key", "gemini-3-pro-image-preview",
                                     "a cat", "1K")


# ---------------------------------------------------------------------------
# Request-body wiring (wrapper kwargs → tweak_body → POST body)
# ---------------------------------------------------------------------------

def _capture_body(call):
    """Run a generate_with_* call against mocked HTTP; return the POSTed body."""
    mock_rsp = MagicMock()
    mock_rsp.status_code = 200
    mock_rsp.json.return_value = {"data": [{"url": "https://cdn.example.com/i.png"}]}
    with patch("providers.base.requests") as mock_requests:
        mock_requests.request.return_value = mock_rsp
        call()
        return mock_requests.request.call_args.kwargs["json"]


class TestBodyWiring:
    def test_ark_guidance_and_watermark(self):
        from volcano_ark import generate_with_ark
        body = _capture_body(lambda: generate_with_ark(
            "k", "doubao-seedream-5-0-260128", "a cat", "2048x2048",
            guidance_scale=7.5, no_watermark=True))
        assert body["guidance_scale"] == 7.5
        assert body["watermark"] is False

    def test_ark_watermark_defaults_true(self):
        from volcano_ark import generate_with_ark
        body = _capture_body(lambda: generate_with_ark(
            "k", "doubao-seedream-5-0-260128", "a cat", "2048x2048"))
        assert body["watermark"] is True

    def test_hunyuan_revise_and_logo(self):
        from hunyuan import generate_with_hunyuan
        body = _capture_body(lambda: generate_with_hunyuan(
            "k", "hy-image-v3.0", "a cat", "1024:1024", revise=1, logo=0))
        assert body["revise"] == 1
        assert body["logo_add"] == 0

    def test_stepfun_negative_prompt(self):
        from stepfun import generate_with_stepfun
        body = _capture_body(lambda: generate_with_stepfun(
            "k", "step-2x-large", "a cat", "1024x1024", negative="blurry"))
        assert body["negative_prompt"] == "blurry"


# ---------------------------------------------------------------------------
# Dispatcher error routing (missing key → AUTH_ERROR / exit 2)
# ---------------------------------------------------------------------------

class TestDispatcherAuthError:
    def test_missing_key_exits_2_with_auth_error(self, tmp_path):
        import json
        import subprocess
        script = _repo_root / "skills" / "imagenCN" / "scripts" / "generate_image.py"
        env = {k: v for k, v in os.environ.items() if k != "STEP_API_KEY"}
        proc = subprocess.run(
            [sys.executable, str(script), "a cat", str(tmp_path / "o.png"),
             "--platform", "stepfun", "--format", "json"],
            capture_output=True, text=True, env=env)
        assert proc.returncode == 2, proc.stdout + proc.stderr
        envelope = json.loads(proc.stdout)
        assert envelope["ok"] is False
        assert envelope["error"]["code"] == "AUTH_ERROR"
        assert envelope["error"]["retryable"] is False


# ---------------------------------------------------------------------------
# Backward-compatible exports
# ---------------------------------------------------------------------------

class TestBackwardCompat:
    def test_ark_module_exports(self):
        from volcano_ark import (get_ark_api_key, resolve_ark_size,
                                 generate_with_ark, ARK_MODELS, ARK_SIZES)
        assert callable(get_ark_api_key)
        assert callable(resolve_ark_size)
        assert callable(generate_with_ark)
        assert isinstance(ARK_MODELS, set)
        assert isinstance(ARK_SIZES, dict)

    def test_hunyuan_module_exports(self):
        from hunyuan import (get_hunyuan_api_key, resolve_hunyuan_size,
                             generate_with_hunyuan, HUNYUAN_MODELS, HUNYUAN_SIZES)
        assert callable(get_hunyuan_api_key)
        assert callable(resolve_hunyuan_size)
        assert callable(generate_with_hunyuan)
        assert isinstance(HUNYUAN_MODELS, set)
        assert isinstance(HUNYUAN_SIZES, dict)

    def test_zhipu_module_exports(self):
        from zhipu import (get_zhipu_api_key, resolve_zhipu_size,
                           generate_with_zhipu, ZHIPU_MODELS, ZHIPU_SIZES)
        assert callable(get_zhipu_api_key)
        assert callable(resolve_zhipu_size)
        assert callable(generate_with_zhipu)
        assert isinstance(ZHIPU_MODELS, set)
        assert isinstance(ZHIPU_SIZES, dict)

    def test_stepfun_module_exports(self):
        from stepfun import (get_stepfun_api_key, resolve_stepfun_size,
                             generate_with_stepfun, STEPFUN_MODELS, STEPFUN_SIZES)
        assert callable(get_stepfun_api_key)
        assert callable(resolve_stepfun_size)
        assert callable(generate_with_stepfun)
        assert isinstance(STEPFUN_MODELS, set)
        assert isinstance(STEPFUN_SIZES, dict)

    def test_gemini_module_exports(self):
        from gemini import (get_gemini_api_key, resolve_gemini_size,
                            generate_with_gemini, save_gemini_image,
                            GEMINI_MODELS, GEMINI_SIZES)
        assert callable(get_gemini_api_key)
        assert callable(resolve_gemini_size)
        assert callable(generate_with_gemini)
        assert callable(save_gemini_image)
        assert isinstance(GEMINI_MODELS, set)
        assert isinstance(GEMINI_SIZES, dict)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

class TestHttpHelpers:
    def test_safe_json_valid(self):
        mock = MagicMock()
        mock.json.return_value = {"ok": True}
        assert safe_json(mock) == {"ok": True}

    def test_safe_json_invalid(self):
        mock = MagicMock()
        mock.headers = {"content-type": "text/html"}
        mock.text = "<html>error</html>"
        mock.status_code = 502
        mock.json.side_effect = ValueError
        with pytest.raises(APIError, match="non-JSON"):
            safe_json(mock)
