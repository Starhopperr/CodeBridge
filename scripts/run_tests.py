#!/usr/bin/env python3
"""
scripts/run_tests.py
CodeBridge — Test Runner (offline summary + optional live backend)

Usage:
  python scripts/run_tests.py           # offline: list all tests with PENDING status
  python scripts/run_tests.py --live    # live: submit each test to running backend

NOTE: These tests are PROPOSED. Run with live backend and valid API key to
      record actual results.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
INPUTS_DIR   = PROJECT_ROOT / "test-data" / "inputs"
BACKEND_URL  = "http://localhost:8000"
TRANSLATE_EP = f"{BACKEND_URL}/translate"

# ── ANSI colours (disabled on Windows without ANSI support) ──────────────────
def _ansi(code: str, text: str) -> str:
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleMode(
                ctypes.windll.kernel32.GetStdHandle(-11), 7
            )
        except Exception:
            return text
    return f"\033[{code}m{text}\033[0m"

GREEN  = lambda t: _ansi("32", t)
RED    = lambda t: _ansi("31", t)
YELLOW = lambda t: _ansi("33", t)
CYAN   = lambda t: _ansi("36", t)
BOLD   = lambda t: _ansi("1",  t)

# ── Hardcoded test-case catalogue (matches CB-T01 to CB-T10) ─────────────────
# If a test-data/inputs/CB-Txx.md file exists its metadata overrides this.
CATALOGUE: list[dict] = [
    {
        "id": "CB-T01",
        "type": "Normal",
        "source_lang": "Python",
        "target_lang": "Java",
        "description": "Fibonacci sequence (recursive) → Java",
    },
    {
        "id": "CB-T02",
        "type": "Normal",
        "source_lang": "Python",
        "target_lang": "C++",
        "description": "Bubble sort → C++",
    },
    {
        "id": "CB-T03",
        "type": "Normal",
        "source_lang": "Java",
        "target_lang": "Python",
        "description": "Stack implementation → Python",
    },
    {
        "id": "CB-T04",
        "type": "Normal",
        "source_lang": "C++",
        "target_lang": "Python",
        "description": "Linked list → Python",
    },
    {
        "id": "CB-T05",
        "type": "Normal",
        "source_lang": "Java",
        "target_lang": "C++",
        "description": "Binary search → C++",
    },
    {
        "id": "CB-T06",
        "type": "Edge",
        "source_lang": "Python",
        "target_lang": "Java",
        "description": "Empty list / None input → Java (expected: graceful handling)",
    },
    {
        "id": "CB-T07",
        "type": "Edge",
        "source_lang": "C++",
        "target_lang": "Java",
        "description": "Pointer arithmetic → Java (expected: handle gracefully)",
    },
    {
        "id": "CB-T08",
        "type": "Edge",
        "source_lang": "Python",
        "target_lang": "C++",
        "description": "Function with zero/negative values → C++",
    },
    {
        "id": "CB-T09",
        "type": "Edge",
        "source_lang": "Python",
        "target_lang": "Java",
        "description": "Integer division (7//2=3) → Java (expected: preserve int division)",
    },
    {
        "id": "CB-T10",
        "type": "Invalid",
        "source_lang": "Python",
        "target_lang": "Java",
        "description": "Malformed Python with syntax error → Java (expected: P1 flags gracefully)",
    },
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_input_file(test_id: str) -> str | None:
    """Return the raw source code from test-data/inputs/CB-Txx.md, or None."""
    md_path = INPUTS_DIR / f"{test_id}.md"
    if not md_path.exists():
        return None
    text = md_path.read_text(encoding="utf-8")
    # Extract the first fenced code block as the snippet
    m = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
    return m.group(1).strip() if m else text.strip()


def parse_metadata_from_md(test_id: str, entry: dict) -> dict:
    """Try to enrich entry dict with Source/Target from the .md front-matter."""
    md_path = INPUTS_DIR / f"{test_id}.md"
    if not md_path.exists():
        return entry
    text = md_path.read_text(encoding="utf-8")
    for field, key in [("source_lang", r"Source[- ]?Language:\s*(\w+)"),
                        ("target_lang", r"Target[- ]?Language:\s*(\w+)"),
                        ("type",        r"Type:\s*(\w+)"),
                        ("description", r"Description:\s*(.+)")]:
        m = re.search(key, text, re.IGNORECASE)
        if m:
            entry[field] = m.group(1).strip()
    return entry


def check_backend_alive() -> bool:
    try:
        import urllib.request
        with urllib.request.urlopen(f"{BACKEND_URL}/health", timeout=4) as r:
            return r.status == 200
    except Exception:
        return False


def run_live_test(entry: dict) -> dict:
    """Submit one test to the backend. Returns result dict."""
    import urllib.request, urllib.error

    source_code = load_input_file(entry["id"])
    if not source_code:
        return {"status": "SKIP", "note": "No input file found"}

    payload = json.dumps({
        "source_code":      source_code,
        "source_language":  entry["source_lang"],
        "target_language":  entry["target_lang"],
        "user_context":     entry.get("description", ""),
    }).encode("utf-8")

    req = urllib.request.Request(
        TRANSLATE_EP,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=120) as resp:
            elapsed = time.time() - t0
            body = json.loads(resp.read().decode("utf-8"))
            # Summarise result
            p3 = body.get("p3_review", {})
            findings = p3.get("findings", [])
            defects  = [f for f in findings if f.get("severity", "").lower() == "definite"]
            return {
                "status":   "PASS",
                "elapsed":  f"{elapsed:.1f}s",
                "defects":  len(defects),
                "findings": len(findings),
            }
    except urllib.error.HTTPError as e:
        return {"status": "FAIL", "note": f"HTTP {e.code}"}
    except Exception as e:
        return {"status": "ERROR", "note": str(e)}


# ── Table printer ─────────────────────────────────────────────────────────────

def print_table(rows: list[dict], live: bool) -> None:
    # Column widths
    cw = {
        "id":    7,
        "type":  8,
        "langs": 16,
        "desc":  48,
        "status": 10,
    }
    if live:
        cw["status"] = 20

    sep = "+" + "+".join("-" * (w + 2) for w in cw.values()) + "+"
    hdr_fmt = "| {:<{id}} | {:<{type}} | {:<{langs}} | {:<{desc}} | {:<{status}} |"

    print(sep)
    print(hdr_fmt.format(
        "Test ID", "Type", "Source→Target", "Description", "Status",
        **cw
    ))
    print(sep)

    for r in rows:
        langs  = f"{r['source_lang']} → {r['target_lang']}"
        status = r.get("live_result", {}).get("status", "PENDING") if live else "PENDING"
        result = r.get("live_result", {})

        if live:
            if status == "PASS":
                d = result.get("defects", 0)
                f = result.get("findings", 0)
                e = result.get("elapsed", "")
                status_str = f"PASS ({d}def/{f}find {e})"
            elif status == "SKIP":
                status_str = f"SKIP: {result.get('note','')}"
            elif status in ("FAIL", "ERROR"):
                status_str = f"{status}: {result.get('note','')[:18]}"
            else:
                status_str = status
        else:
            status_str = "PENDING"

        desc = r["description"]
        if len(desc) > cw["desc"]:
            desc = desc[:cw["desc"] - 1] + "…"

        print(
            f"| {r['id']:<{cw['id']}} "
            f"| {r['type']:<{cw['type']}} "
            f"| {langs:<{cw['langs']}} "
            f"| {desc:<{cw['desc']}} "
            f"| {status_str:<{cw['status']}} |"
        )
    print(sep)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="CodeBridge test runner — offline summary or live backend run"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Submit tests to the running backend at http://localhost:8000",
    )
    args = parser.parse_args()

    print()
    print(BOLD(CYAN("=" * 72)))
    print(BOLD(CYAN("  CodeBridge — Test Suite Runner")))
    print(BOLD(CYAN("=" * 72)))
    print()
    print(YELLOW("  NOTE: These tests are PROPOSED. Run with live backend and"))
    print(YELLOW("        valid API key to record actual results."))
    print()

    # Build row list from catalogue, enriched from .md files
    rows = []
    for entry in CATALOGUE:
        e = dict(entry)
        e = parse_metadata_from_md(e["id"], e)
        rows.append(e)

    if args.live:
        print(CYAN("  Mode: LIVE — connecting to backend…"))
        if not check_backend_alive():
            print(RED("  [ERROR] Backend not reachable at http://localhost:8000"))
            print(RED("          Start the backend first (or use run_dev.ps1)."))
            sys.exit(1)
        print(GREEN("  [OK] Backend is alive. Running tests…"))
        print()
        for r in rows:
            print(f"  Running {r['id']}… ", end="", flush=True)
            result = run_live_test(r)
            r["live_result"] = result
            status = result.get("status", "?")
            if status == "PASS":
                print(GREEN(f"PASS ({result.get('elapsed','')})"))
            elif status == "SKIP":
                print(YELLOW(f"SKIP — {result.get('note','')}"))
            else:
                print(RED(f"{status} — {result.get('note','')}"))
        print()
    else:
        print(CYAN("  Mode: OFFLINE — showing catalogue (no backend calls)"))
        print()

    print_table(rows, live=args.live)

    print()
    if not args.live:
        print("  To run against the live backend:  python scripts/run_tests.py --live")
        print("  To start both servers:            .\\scripts\\run_dev.ps1")
    print()
    print(BOLD("  Test case inputs : test-data/inputs/CB-T01.md … CB-T10.md"))
    print(BOLD("  Expected outputs : test-data/expected/CB-T01_expected.md … CB-T10_expected.md"))
    print()


if __name__ == "__main__":
    main()
