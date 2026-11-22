# M2_FORM_VALUES.md — Milestone 2 Submission Form Reference

Use this document to fill in the M2 submission form. Items marked **[TO BE PROVIDED]** must be completed by the team before submitting.

---

## Section 1 — Team Identification

| Field | Value |
|---|---|
| **Team ID** | [TO BE PROVIDED] |
| **Team Name** | [TO BE PROVIDED] |

### Team Members

| Name | Enrollment Number |
|---|---|
| [TO BE PROVIDED] | [TO BE PROVIDED] |
| [TO BE PROVIDED] | [TO BE PROVIDED] |
| [TO BE PROVIDED] | [TO BE PROVIDED] |

---

## Section 2 — Project Details

| Field | Value |
|---|---|
| **Project Title** | CodeBridge — Semantics-Aware Code Translation and Verification |
| **Problem Pool** | C7 |
| **Model Used** | `gemini-1.5-flash` |

---

## Section 3 — Prototype Access

| Field | Value |
|---|---|
| **Prototype Link** | `http://localhost:5173` (local development) |
| **Backend API** | `http://localhost:8000` |
| **Repository Link** | [TO BE PROVIDED] |

> [!IMPORTANT]
> The prototype runs locally. To run it:
> 1. `cd backend && pip install -r requirements.txt`
> 2. Add `GOOGLE_API_KEY=...` to `backend/.env`
> 3. `uvicorn main:app --reload`
> 4. `cd frontend && npm install && npm run dev`
> 5. Open `http://localhost:5173`

---

## Section 4 — Demonstration Reel

| Field | Value |
|---|---|
| **Reel Link** | [TO BE PROVIDED] |
| **Duration** | [TO BE PROVIDED] (expected: 2–5 minutes) |

> [!NOTE]
> The reel should demonstrate: code input → P1 analysis panel → translated code → P3 review findings → P4 test cases → export.

---

## Section 5 — Prompt Information

| Field | Value |
|---|---|
| **Number of Prompts in Pipeline** | 4 (P1, P2, P3, P4) |
| **Number of Prompt Versions** | 3 (V1 baseline, V2 constrained, V3 chained/final) |

### Prompt Summary

| Prompt | V1 (Baseline) | V2 (Constrained) | V3/Final (Chained) |
|---|---|---|---|
| P1 — Static Analysis | `prompts/v1/p1_v1.md` | `prompts/v2/p1_v2.md` | `prompts/v3/p1_v3.md` |
| P2 — Translation | `prompts/v1/p2_v1.md` | `prompts/v2/p2_v2.md` | `prompts/v3/p2_v3.md` |
| P3 — Semantic Review | _(not in V1)_ | `prompts/v2/p3_v2.md` | `prompts/v3/p3_v3.md` |
| P4 — Test Generation | _(not in V1)_ | `prompts/v2/p4_v2.md` | `prompts/v3/p4_v3.md` |

---

## Section 6 — Test Suite

| Field | Value |
|---|---|
| **Number of Test Rows** | 10 |
| **Test Case IDs** | CB-T01 through CB-T10 |
| **Test Types** | Normal (6), Edge (3), Invalid (1) |

### Test Case Summary

| ID | Type | Source → Target | Description |
|---|---|---|---|
| CB-T01 | Normal | Python → Java | Factorial function (recursive) |
| CB-T02 | Normal | Python → Java | FizzBuzz conditional |
| CB-T03 | Normal | Python → C++ | Sum accumulator with for loop |
| CB-T04 | Normal | Python → Java | List max finder |
| CB-T05 | Normal | Python → C++ | String reversal |
| CB-T06 | Normal | Python → Java | Dictionary word counter |
| CB-T07 | Edge | Python → Java | Function with empty list input |
| CB-T08 | Edge | Python → C++ | Function with zero/negative values |
| CB-T09 | Edge | Python → Java | Integer division semantics (7//2 = 3) |
| CB-T10 | Invalid | Python → Java | Malformed Python with syntax error |

---

## Section 7 — Working Modules

| Module | Status |
|---|---|
| Code Editor with Syntax Highlighting | ✅ Working |
| Source / Target Language Selection | ✅ Working |
| P1 Static Analysis Panel | ✅ Working |
| P2 Translation Panel | ✅ Working |
| P3 Semantic Review Panel | ✅ Working |
| P4 Test Generation Panel | ✅ Working |
| Export (JSON / Copy) | ✅ Working |

---

## Section 8 — Supporting Document

| Field | Value |
|---|---|
| **Supporting Document Type** | Technical Report |
| **Document Location** | `docs/` directory |

Key supporting documents:
- `docs/PROJECT_FACTS.md` — project overview
- `docs/M1_PROPOSAL.md` — full proposal
- `docs/VIVA_PREPARATION.md` — Q&A preparation
- `research/COMPARABLE_TOOLS.md` — existing tools analysis
- `prompts/` — full prompt library with version history
- `test-data/` — 10 test inputs + expected outputs
