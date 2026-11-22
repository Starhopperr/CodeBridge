# MILESTONE_STATUS.md — CodeBridge

## M1 — Proposal

**Status: ✅ COMPLETED**

> [!NOTE]
> The original M1 deadline has passed. The proposal is preserved as `docs/M1_PROPOSAL.md` for reference and viva preparation.

**Deliverables Completed:**
- [x] Project proposal document (`docs/M1_PROPOSAL.md`)
- [x] Problem statement and user identification
- [x] Initial prompt workflow design (P1→P2→P3→P4)
- [x] Existing solutions survey (see `research/COMPARABLE_TOOLS.md`)
- [x] Technology stack proposed

---

## M2 — Prototype

**Status: 🔄 IN PROGRESS**
**Deadline: 22 November 2026, 11:59 PM**

### What is Working

| Module | Status | Notes |
|---|---|---|
| Project directory structure | ✅ Done | Full scaffold created |
| FastAPI backend (`backend/`) | ✅ Done | `main.py`, `pipeline.py`, `schemas.py`, `prompts.py`, `config.py` |
| React + Vite + TypeScript frontend (`frontend/`) | ✅ Done | Editor, language selectors, results panels, export |
| Prompt library v1 (baseline) | ✅ Done | `prompts/v1/p1_v1.md`, `p2_v1.md` |
| Prompt library v2 (constrained) | ✅ Done | `prompts/v2/p1_v2.md` through `p4_v2.md` |
| Prompt library v3 / final (chained) | ✅ Done | `prompts/v3/` and `prompts/final/` |
| Test-data inputs | ✅ Done | CB-T01 through CB-T10 |
| Test-data expected | ✅ Done | CB-T01_expected through CB-T10_expected |
| Documentation | ✅ Done | PROJECT_FACTS, BUILD_LOG, VIVA_PREPARATION, etc. |
| Comparable tools research | ✅ Done | `research/COMPARABLE_TOOLS.md` |

### What is Pending

| Item | Blocker | Action Required |
|---|---|---|
| End-to-end API test | Needs `GOOGLE_API_KEY` in `backend/.env` | Team to add API key |
| Live prototype demo | Needs `npm install` + `uvicorn` running | Start both servers locally |
| Test suite execution | Needs live API connection | Run after key is added |
| M2 form submission | Form link not yet opened | Complete form at `docs/M2_FORM_VALUES.md` |
| Repository URL | Not yet shared | Add to `PROJECT_FACTS.md` |
| Reel / demo video | Not yet recorded | Record 2–5 min demo |
| Team member details | Placeholder only | Fill `[TO BE PROVIDED]` fields |

### How to Start the Prototype Locally

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env  # then add your GOOGLE_API_KEY
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

---

## M3 — Final Submission

**Status: ⏳ NOT STARTED**
**Deadline: 1 December 2026**

**Expected Deliverables (to be confirmed):**
- [ ] Polished, fully tested prototype
- [ ] Final prompt library with iteration evidence
- [ ] Completed test suite with actual model outputs
- [ ] Comparison table: V1 vs V2 vs V3 results
- [ ] Final report / technical document
- [ ] Video demonstration
- [ ] Viva / presentation readiness
