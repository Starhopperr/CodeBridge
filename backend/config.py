"""
config.py — Load environment configuration for CodeBridge backend.
"""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# Search for .env in current directory (backend/) or project root (..)
backend_dir = Path(__file__).resolve().parent
root_dir = backend_dir.parent

env_loaded = False
for env_path in [backend_dir / ".env", root_dir / ".env"]:
    if env_path.is_file():
        load_dotenv(dotenv_path=env_path)
        env_loaded = True
        break

if not env_loaded:
    load_dotenv()

GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
MODEL_NAME: str = os.getenv("MODEL_NAME", "gemini-1.5-flash")


def is_api_key_configured() -> bool:
    """Check if a real Gemini API key is configured."""
    key = os.getenv("GOOGLE_API_KEY") or GOOGLE_API_KEY
    if not key or not key.strip() or "your_gemini_api_key" in key or key == "your_key_here":
        return False
    return True


def require_api_key() -> str:
    """Validate that GOOGLE_API_KEY is present; raise EnvironmentError if missing."""
    if not is_api_key_configured():
        raise EnvironmentError(
            "GOOGLE_API_KEY is not configured. "
            "Please copy .env.example to .env and configure your Gemini API key."
        )
    return (os.getenv("GOOGLE_API_KEY") or GOOGLE_API_KEY).strip()
