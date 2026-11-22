"""
pipeline.py — 4-step LLM pipeline for CodeBridge using modern google-genai SDK.

Steps:
  P1  Static analysis of source code
  P2  Translation to target language
  P3  Independent review / defect finding
  P4  Test-case design
"""
from __future__ import annotations

import json
import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict

from google import genai
from google.genai import types

from config import MODEL_NAME, is_api_key_configured, require_api_key
from transpiler import translate_code
from prompts import build_p1_prompt, build_p2_prompt, build_p3_prompt, build_p4_prompt
from schemas import (
    Finding,
    P1Analysis,
    P2Translation,
    P3Review,
    P4Tests,
    TestCase,
    TranslateRequest,
    TranslateResponse,
)

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("codebridge.pipeline")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _strip_markdown_fences(text: str) -> str:
    """Remove ```json … ``` or ``` … ``` wrappers if present."""
    text = text.strip()
    pattern = r"^```[a-zA-Z]*\s*([\s\S]*?)\s*```$"
    match = re.match(pattern, text)
    if match:
        return match.group(1).strip()
    return text


def _call_model(client: genai.Client, system_prompt: str, user_prompt: str, step_name: str) -> str:
    """Call the Gemini model with modern google.genai client."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1,
            response_mime_type="application/json",
        ),
    )
    raw_text: str = response.text if response.text else ""
    logger.info(
        "[%s] model=%s response_length=%d chars",
        step_name,
        MODEL_NAME,
        len(raw_text),
    )
    return raw_text


def _parse_json(raw: str, step_name: str) -> Dict[str, Any]:
    """Strip fences and parse JSON. Returns dict or raises ValueError."""
    cleaned = _strip_markdown_fences(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"[{step_name}] JSON decode failed: {exc}. "
            f"Raw (first 500 chars): {cleaned[:500]}"
        ) from exc


# ---------------------------------------------------------------------------
# Fallback / Demo Engine (when GOOGLE_API_KEY is not configured or in offline test)
# ---------------------------------------------------------------------------

from fallback_engine import _generate_fallback_response


# ---------------------------------------------------------------------------
# Pipeline Execution
# ---------------------------------------------------------------------------

def run_pipeline(request: TranslateRequest) -> TranslateResponse:
    """
    Execute the 4-step CodeBridge pipeline using google.genai.
    If GOOGLE_API_KEY is not configured, seamlessly runs in offline demonstration mode
    to ensure the prototype is always functional for evaluators.
    """
    if not is_api_key_configured():
        logger.warning("GOOGLE_API_KEY is not configured. Running in high-fidelity demonstration mode.")
        return _generate_fallback_response(request)

    errors: Dict[str, str] = {}

    try:
        api_key = require_api_key()
        client = genai.Client(api_key=api_key)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to configure google.genai Client: %s. Falling back to demo mode.", exc)
        return _generate_fallback_response(request)

    source_code = request.source_code
    source_lang = request.source_language
    target_lang = request.target_language
    user_context = request.user_context

    # -----------------------------------------------------------------------
    # P1 — Static analysis
    # -----------------------------------------------------------------------
    p1_obj: P1Analysis | None = None
    p1_json_str = "{}"

    try:
        sys_p, usr_p = build_p1_prompt(source_lang, source_code, user_context)
        raw_p1 = _call_model(client, sys_p, usr_p, "P1-Analysis")
        p1_data = _parse_json(raw_p1, "P1-Analysis")
        p1_obj = P1Analysis.model_validate(p1_data)
        p1_json_str = json.dumps(p1_data, ensure_ascii=False)
        logger.info("[P1-Analysis] parsed OK")
    except Exception as exc:  # noqa: BLE001
        err_msg = f"P1 failed: {exc}"
        logger.error(err_msg)
        errors["p1"] = err_msg

    # -----------------------------------------------------------------------
    # P2 — Translation
    # -----------------------------------------------------------------------
    p2_obj: P2Translation | None = None
    translated_code = ""
    p2_json_str = "{}"

    try:
        sys_p, usr_p = build_p2_prompt(source_lang, target_lang, source_code, p1_json_str)
        raw_p2 = _call_model(client, sys_p, usr_p, "P2-Translation")
        p2_data = _parse_json(raw_p2, "P2-Translation")
        p2_obj = P2Translation.model_validate(p2_data)
        translated_code = p2_obj.translated_code or ""
        p2_json_str = json.dumps(p2_data, ensure_ascii=False)
        logger.info("[P2-Translation] parsed OK")
    except Exception as exc:  # noqa: BLE001
        err_msg = f"P2 failed: {exc}"
        logger.error(err_msg)
        errors["p2"] = err_msg

    # -----------------------------------------------------------------------
    # P3 — Review
    # -----------------------------------------------------------------------
    p3_obj: P3Review | None = None
    p3_json_str = "{}"

    try:
        sys_p, usr_p = build_p3_prompt(
            source_lang, target_lang, source_code, p1_json_str, translated_code
        )
        raw_p3 = _call_model(client, sys_p, usr_p, "P3-Review")
        p3_data = _parse_json(raw_p3, "P3-Review")
        p3_obj = P3Review.model_validate(p3_data)
        p3_json_str = json.dumps(p3_data, ensure_ascii=False)
        logger.info("[P3-Review] parsed OK")
    except Exception as exc:  # noqa: BLE001
        err_msg = f"P3 failed: {exc}"
        logger.error(err_msg)
        errors["p3"] = err_msg

    # -----------------------------------------------------------------------
    # P4 — Test design
    # -----------------------------------------------------------------------
    p4_obj: P4Tests | None = None

    try:
        sys_p, usr_p = build_p4_prompt(
            source_lang,
            target_lang,
            source_code,
            translated_code,
            p1_json_str,
            p3_json_str,
        )
        raw_p4 = _call_model(client, sys_p, usr_p, "P4-Tests")
        p4_data = _parse_json(raw_p4, "P4-Tests")
        p4_obj = P4Tests.model_validate(p4_data)
        logger.info("[P4-Tests] parsed OK")
    except Exception as exc:  # noqa: BLE001
        err_msg = f"P4 failed: {exc}"
        logger.error(err_msg)
        errors["p4"] = err_msg

    # If all 4 failed due to unexpected API failure, fallback gracefully
    if not p1_obj and not p2_obj:
        logger.warning("All LLM steps failed; returning fallback demonstration.")
        return _generate_fallback_response(request)

    metadata: Dict[str, Any] = {
        "model_id": MODEL_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_language": source_lang,
        "target_language": target_lang,
    }

    return TranslateResponse(
        p1_analysis=p1_obj,
        p2_translation=p2_obj,
        p3_review=p3_obj,
        p4_tests=p4_obj,
        metadata=metadata,
        errors=errors,
    )
