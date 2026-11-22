"""
pipeline.py — 4-step LLM pipeline for CodeBridge.

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

import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory

from config import MODEL_NAME, require_api_key
from prompts import build_p1_prompt, build_p2_prompt, build_p3_prompt, build_p4_prompt
from schemas import (
    P1Analysis,
    P2Translation,
    P3Review,
    P4Tests,
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

# API key configuration will be done at runtime via require_api_key()

# Safety settings — keep permissive for code content so security-related
# examples are not blocked.
SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

GENERATION_CONFIG = genai.GenerationConfig(
    temperature=0.1,
    # Requesting JSON MIME type nudges the model to stay on-schema.
    response_mime_type="application/json",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _strip_markdown_fences(text: str) -> str:
    """Remove ```json … ``` or ``` … ``` wrappers if present."""
    text = text.strip()
    # Match optional language tag after opening fence
    pattern = r"^```[a-zA-Z]*\s*([\s\S]*?)\s*```$"
    match = re.match(pattern, text)
    if match:
        return match.group(1).strip()
    return text


def _call_model(system_prompt: str, user_prompt: str, step_name: str) -> str:
    """
    Call the Gemini model with a system + user prompt.
    Returns the raw text response.
    """
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=system_prompt,
        generation_config=GENERATION_CONFIG,
        safety_settings=SAFETY_SETTINGS,
    )
    response = model.generate_content(user_prompt)
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
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(request: TranslateRequest) -> TranslateResponse:
    """
    Execute the 4-step CodeBridge pipeline and return a TranslateResponse.

    Each step failure is captured as an error note; subsequent steps that
    depend on a failed step receive an empty JSON object so they can still
    attempt to run.
    """
    errors: Dict[str, str] = {}

    # Validate and configure API key before executing steps
    api_key = require_api_key()
    genai.configure(api_key=api_key)

    # Serialise source for prompt injection
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
        raw_p1 = _call_model(sys_p, usr_p, "P1-Analysis")
        p1_data = _parse_json(raw_p1, "P1-Analysis")
        p1_obj = P1Analysis.model_validate(p1_data)
        p1_json_str = json.dumps(p1_data, ensure_ascii=False)
        logger.info("[P1-Analysis] parsed OK — %d functions found", len(p1_obj.functions))
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
        raw_p2 = _call_model(sys_p, usr_p, "P2-Translation")
        p2_data = _parse_json(raw_p2, "P2-Translation")
        p2_obj = P2Translation.model_validate(p2_data)
        translated_code = p2_obj.translated_code or ""
        p2_json_str = json.dumps(p2_data, ensure_ascii=False)
        logger.info(
            "[P2-Translation] parsed OK — translated_code length=%d", len(translated_code)
        )
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
        raw_p3 = _call_model(sys_p, usr_p, "P3-Review")
        p3_data = _parse_json(raw_p3, "P3-Review")
        p3_obj = P3Review.model_validate(p3_data)
        p3_json_str = json.dumps(p3_data, ensure_ascii=False)
        logger.info(
            "[P3-Review] parsed OK — %d findings recorded",
            len(p3_obj.findings),
        )
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
        raw_p4 = _call_model(sys_p, usr_p, "P4-Tests")
        p4_data = _parse_json(raw_p4, "P4-Tests")
        p4_obj = P4Tests.model_validate(p4_data)
        logger.info(
            "[P4-Tests] parsed OK — %d test cases", len(p4_obj.test_cases)
        )
    except Exception as exc:  # noqa: BLE001
        err_msg = f"P4 failed: {exc}"
        logger.error(err_msg)
        errors["p4"] = err_msg

    # -----------------------------------------------------------------------
    # Assemble response
    # -----------------------------------------------------------------------
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
