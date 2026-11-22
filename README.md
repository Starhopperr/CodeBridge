# CodeBridge

**CodeBridge — Semantics-Aware Code Translation and Verification.**
A prompt-engineering workflow (SCSE4041, Problem Pool C7) that translates code snippets between Python, Java and C++ while making assumptions, language differences and semantic mismatches inspectable.

---

## Table of Contents

1. [Project Summary](#project-summary)
2. [Supported Languages & Constructs](#supported-languages--constructs)
3. [Architecture](#architecture)
4. [Prerequisites](#prerequisites)
5. [Setup & Installation](#setup--installation)
6. [Environment Variables](#environment-variables)
7. [Running the Application](#running-the-application)
8. [Running Tests](#running-tests)
9. [Experiment Reproduction](#experiment-reproduction)
10. [Team](#team)
11. [Limitations](#limitations)
12. [Responsible Use](#responsible-use)

---

## Project Summary

CodeBridge is a full-stack web application and prompt-engineering research prototype that uses a **4-stage LLM pipeline** to translate self-contained code snippets between Python, Java, and C++. Each stage is a structured prompt that produces inspectable JSON output, allowing developers and researchers to see exactly what assumptions were made, what semantic differences exist, and what tests are proposed.

This project was developed for **SCSE4041 — Problem Pool C7**.

---

## Supported Languages & Constructs

**Supported translation pairs:**

| Source Language | Target Language |
|----------------|----------------|
| Python         | Java           |
| Python         | C++            |
| Java           | Python         |
| Java           | C++            |
| C++            | Python         |
| C++            | Java           |

**Supported constructs:**
- Self-contained snippets with **no external library dependencies**
- Standard data structures (arrays, lists, maps, sets)
- Control flow (loops, conditionals, recursion)
- Basic I/O via `stdin`/`stdout`
- Simple classes and functions
- Common algorithms (sorting, searching, math)

**Unsupported constructs** (flagged by P1 Analysis):
- External library imports (e.g., `numpy`, `pandas`, `javax.*`, Boost)
- GUI code (Tkinter, Swing, Qt, etc.)
- File I/O beyond `stdin`/`stdout`
- Complex OOP hierarchies (deep inheritance, multiple interface implementation)
- Reflection, metaprogramming, or runtime code generation
- Threading / async / concurrent primitives
- Platform-specific system calls

---

## Architecture

**4-prompt pipeline:**

```
P1 Source Analysis → P2 Constrained Translation → P3 Semantic Review → P4 Test Generation
```

| Stage | Role | Output |
|-------|------|--------|
| **P1** | Static source analysis | Program summary, functions, data structures, edge cases, assumptions |
| **P2** | Constrained translation | Translated code with inline assumption notes |
| **P3** | Independent semantic review | Findings: definite defects, risks, open questions |
| **P4** | Test generation | Proposed test cases (normal, boundary, edge, error) |

**Stack:**

- **Frontend:** React + Vite + TypeScript
- **Backend:** Python FastAPI
- **LLM Model:** Gemini (configurable via environment variable)
- **Communication:** REST API (JSON)

```
┌─────────────────────┐         ┌──────────────────────────────────────┐
│  React + Vite + TS  │  REST   │  FastAPI Backend                     │
│  (localhost:5173)   │◄───────►│  (localhost:8000)                    │
│                     │         │                                      │
│  - Code input form  │         │  POST /translate                     │
│  - P1-P4 results    │         │  ├── P1: Source Analysis             │
│  - Findings display │         │  ├── P2: Constrained Translation     │
│  - Test cases table │         │  ├── P3: Semantic Review             │
└─────────────────────┘         │  └── P4: Test Generation             │
                                │                     │                │
                                │              Gemini API              │
                                └──────────────────────────────────────┘
```

---

## Prerequisites

| Requirement | Minimum Version | Notes |
|-------------|----------------|-------|
| Python | 3.10+ | For the FastAPI backend |
| Node.js | 18+ | For the React frontend |
| npm | 9+ | Installed with Node.js |
| Gemini API Key | — | Obtain from [Google AI Studio](https://aistudio.google.com/) |

---

## Setup & Installation

```bash
# 1. Clone or download the project
git clone <repository-url>
cd CodeBridge

# ── Backend ──────────────────────────────────────────────
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

pip install -r requirements.txt

copy .env.example .env        # Windows
# cp .env.example .env        # macOS / Linux
# Then open .env and set your GOOGLE_API_KEY

uvicorn main:app --reload
# Backend now running at http://localhost:8000

# ── Frontend (open a new terminal) ───────────────────────
cd frontend
npm install
npm run dev
# Frontend now running at http://localhost:5173
```

> **Tip:** Use `scripts/run_dev.ps1` on Windows to launch both servers automatically.

---

## Environment Variables

Create `backend/.env` by copying `backend/.env.example`:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | ✅ Yes | — | Your Gemini API key. **Never commit this.** |
| `MODEL_NAME` | ❌ No | `gemini-1.5-flash` | Gemini model to use (e.g. `gemini-1.5-pro`) |

> **Warning:** `GOOGLE_API_KEY` is listed in `.gitignore` and `.env` is excluded from version control. Running `scripts/check_secrets.ps1` will scan your tracked files and alert if the key was accidentally committed.

---

## Running the Application

### Quick Start (Windows)

```powershell
# From the project root:
.\scripts\run_dev.ps1
```

This script:
1. Verifies `backend/.env` exists
2. Launches the backend in a new PowerShell window
3. Waits 3 seconds for the backend to start
4. Launches the frontend in another new PowerShell window
5. Prints the URLs

### Manual Start

```bash
# Terminal 1 — Backend
cd backend
.venv\Scripts\activate
uvicorn main:app --reload

# Terminal 2 — Frontend
cd frontend
npm run dev
```

**Access the app:** Open [http://localhost:5173](http://localhost:5173) in your browser.

**API docs:** [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI auto-generated by FastAPI)

---

## Running Tests

### Offline / Proposed mode (no API key needed)

```bash
python scripts/run_tests.py
```

Lists all 10 test cases with their type and translation direction. Status is `PENDING` until run against a live backend.

### Live mode (requires running backend + valid API key)

```bash
python scripts/run_tests.py --live
```

Submits each test case to the backend at `http://localhost:8000/translate` and records the pipeline response.

### Secret scanning

```powershell
.\scripts\check_secrets.ps1
```

Scans all git-tracked files for accidentally committed API key patterns. Prints `PASS` or `FAIL`.

---

## Experiment Reproduction

To reproduce the results reported in the project documentation:

1. Set up the backend with a valid `GOOGLE_API_KEY` (see [Setup](#setup--installation))
2. Start both servers
3. Run the test suite in live mode:
   ```bash
   python scripts/run_tests.py --live
   ```
4. Inspect raw outputs in `test-data/inputs/` and `test-data/expected/`
5. Cross-reference with `docs/BUILD_LOG.md` and `docs/MILESTONE_STATUS.md`

> Run `scripts/run_tests.py` against the live backend for offline test-data inspection.

---

## Team

> **[TO BE PROVIDED]**

---

## Limitations

| Limitation | Detail |
|-----------|--------|
| No guaranteed semantic equivalence | The pipeline proposes a translation; correctness is not formally verified. |
| No arbitrary code execution | No code is executed at any stage — all analysis is static and LLM-based. |
| Input size limit | Maximum **5000 characters** per snippet. |
| Language scope | Python, Java, and C++ **only**. No other languages. |
| No external dependencies | Snippets must be self-contained. External imports are flagged, not translated. |
| LLM variability | Results may differ across API calls due to model temperature and version changes. |

---

## Responsible Use

> **Treat submitted code as untrusted.** Do not submit proprietary or personal data without consent. Test results are proposed, not verified execution.

- **Do not submit** code containing credentials, secrets, or personally identifiable information.
- **Do not submit** proprietary algorithms or trade secrets without appropriate authorization.
- **Understand** that all outputs are **proposed** translations — they have not been compiled, executed, or formally verified.
- **Review** all P3 findings and P4 test cases before using any translated code in production.
- The backend does not store submitted code beyond the duration of a single API request.

---

*CodeBridge — SCSE4041 Problem Pool C7 | Milestone 2*
