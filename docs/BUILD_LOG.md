# BUILD_LOG.md — CodeBridge

A chronological record of build activities, changes, and findings.

---

## 2026-11-22 — Initial Scaffold

| Field | Detail |
|---|---|
| **Owner** | Antigravity (AI assistant) |
| **Session** | Swarm build — full project scaffold |

### Files Changed / Created

**Backend (`backend/`):**
- `requirements.txt` — Python dependencies
- `config.py` — API key and model config from `.env`
- `schemas.py` — Pydantic v2 models for all pipeline stages
- `prompts.py` — Prompt builder functions for P1–P4
- `pipeline.py` — 4-step LLM pipeline (`run_pipeline`)
- `main.py` — FastAPI app with CORS and `/translate` endpoint
- `.env.example` — Template for environment variables

**Frontend (`frontend/`):**
- `package.json` — Project metadata and npm scripts
- `vite.config.ts` — Vite + React configuration with API proxy
- `tsconfig.json` — TypeScript compiler options
- `index.html` — HTML entry point
- `src/main.tsx` — React root
- `src/App.tsx` — Main application component (editor, selectors, results)
- `src/api.ts` — API client for `/translate`
- `src/types.ts` — TypeScript interfaces matching backend schemas
- `src/components/` — UI components (CodeEditor, LanguageSelector, ResultsPanel, etc.)

**Docs (`docs/`):**
- `PROJECT_FACTS.md`
- `MILESTONE_STATUS.md`
- `BUILD_LOG.md` ← this file
- `M1_PROPOSAL.md`
- `M1_RUBRIC_AUDIT.md`
- `M2_FORM_VALUES.md`
- `VIVA_PREPARATION.md`

**Research (`research/`):**
- `COMPARABLE_TOOLS.md`

**Prompt Library:**
- `prompts/v1/p1_v1.md`, `p2_v1.md`
- `prompts/v2/p1_v2.md`, `p2_v2.md`, `p3_v2.md`, `p4_v2.md`
- `prompts/v3/p1_v3.md`, `p2_v3.md`, `p3_v3.md`, `p4_v3.md`
- `prompts/final/p1_final.md`, `p2_final.md`, `p3_final.md`, `p4_final.md`

**Test Data:**
- `test-data/inputs/CB-T01.md` through `CB-T10.md` (10 input files)
- `test-data/expected/CB-T01_expected.md` through `CB-T10_expected.md` (10 expected files)

### Work Completed
- Full directory structure established
- Backend FastAPI application implemented with 4-prompt pipeline
- React + Vite + TypeScript frontend with code editor, language selectors, and results display
- Prompt library created: 3 version families (V1 baseline, V2 constrained, V3/final chained)
- 10 test input cases authored (CB-T01 through CB-T10, covering normal, edge, and invalid scenarios)
- 10 expected result descriptions authored (pre-defined before model execution)
- All documentation files created

### Tests Executed

> [!WARNING]
> **None yet.** End-to-end tests are pending a valid `GOOGLE_API_KEY`.

### Results

- Pending first run. All files are structurally complete.

### Known Issues

| Issue | Severity | Notes |
|---|---|---|
| `GOOGLE_API_KEY` not set | **Blocker** | App will not function until key is added to `backend/.env` |
| npm packages not installed | Medium | Run `npm install` in `frontend/` before starting dev server |
| No actual model outputs recorded | Medium | Test suite results are pre-defined expected only; actual outputs pending |

### Next Actions

1. Team member adds `GOOGLE_API_KEY=...` to `backend/.env`
2. Start backend: `cd backend && uvicorn main:app --reload`
3. Start frontend: `cd frontend && npm install && npm run dev`
4. Run CB-T01 through CB-T10 manually via the UI
5. Record actual model outputs in `test-data/outputs/` (create directory)
6. Compare outputs to `test-data/expected/` and log findings here
7. Record demonstration reel (2–5 min)
8. Complete M2 submission form (see `docs/M2_FORM_VALUES.md`)

---

_Log entries should be appended below as work continues._
