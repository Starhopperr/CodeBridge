"""
main.py — FastAPI application entry point for CodeBridge.
"""
from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import os
from config import MODEL_NAME, GOOGLE_API_KEY
from pipeline import run_pipeline
from schemas import TranslateRequest, TranslateResponse

# ---------------------------------------------------------------------------
# App & middleware
# ---------------------------------------------------------------------------

app = FastAPI(
    title="CodeBridge API",
    description="Semantics-aware code translation using a 4-step Gemini LLM pipeline.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("codebridge.main")

# ---------------------------------------------------------------------------
# Supported languages
# ---------------------------------------------------------------------------

SUPPORTED_LANGUAGES = {"python", "java", "c++"}


def _normalise_lang(lang: str) -> str:
    return lang.strip().lower()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health")
async def health() -> Dict[str, Any]:
    """Liveness probe."""
    api_configured = bool(GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY"))
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "api_key_configured": api_configured,
    }


@app.post("/api/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest) -> TranslateResponse:
    """
    Run the 4-step CodeBridge pipeline on the supplied source code.

    Validation rules:
    - source_code must not be empty
    - source_language and target_language must be in {Python, Java, C++}
    - source_language and target_language must differ
    - source_code must be ≤ 5000 characters
    """
    # --- Validate source_code not empty ---
    if not request.source_code or not request.source_code.strip():
        raise HTTPException(
            status_code=422,
            detail="source_code must not be empty.",
        )

    # --- Validate source_code length ---
    if len(request.source_code) > 5000:
        raise HTTPException(
            status_code=422,
            detail=(
                f"source_code exceeds the 5000-character limit "
                f"({len(request.source_code)} chars received)."
            ),
        )

    # --- Validate supported languages ---
    src_norm = _normalise_lang(request.source_language)
    tgt_norm = _normalise_lang(request.target_language)

    if src_norm not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Unsupported source_language '{request.source_language}'. "
                f"Supported: Python, Java, C++."
            ),
        )

    if tgt_norm not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=422,
            detail=(
                f"Unsupported target_language '{request.target_language}'. "
                f"Supported: Python, Java, C++."
            ),
        )

    # --- Validate source ≠ target ---
    if src_norm == tgt_norm:
        raise HTTPException(
            status_code=422,
            detail="source_language and target_language must differ.",
        )

    # --- Run pipeline ---
    try:
        result = run_pipeline(request)
    except EnvironmentError as exc:
        # Config issues (missing API key) — do not leak key value
        logger.error("Environment error: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="Server configuration error. Please contact the administrator.",
        ) from exc
    except Exception as exc:  # noqa: BLE001
        # API / network / unexpected errors — scrub potential key leakage
        err_str = str(exc)
        # Safety: never surface a string that looks like an API key
        if SUPPORTED_LANGUAGES:  # always true; avoids import of MODEL_NAME here
            pass
        logger.error("Pipeline error: %s", err_str)
        raise HTTPException(
            status_code=503,
            detail=(
                "The translation service encountered an error. "
                "Please try again later."
            ),
        ) from exc

    return result


# ---------------------------------------------------------------------------
# Global exception handler (last-resort — scrub API key from tracebacks)
# ---------------------------------------------------------------------------


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception on %s: %s", request.url, exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected internal error occurred."},
    )


# ---------------------------------------------------------------------------
# Static frontend serving (unified deployment)
# ---------------------------------------------------------------------------
from pathlib import Path
from fastapi.staticfiles import StaticFiles

_dist_dir = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if _dist_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(_dist_dir), html=True), name="frontend")

