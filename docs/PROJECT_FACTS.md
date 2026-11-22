# PROJECT_FACTS.md — CodeBridge

## Project Overview

| Field | Value |
|---|---|
| **Project Name** | CodeBridge — Semantics-Aware Code Translation and Verification |
| **Course** | Prompt Engineering (SCSE4041) |
| **Problem Pool** | C7 |
| **Model** | `gemini-1.5-flash` (API model ID: `models/gemini-1.5-flash`) |
| **Status** | Implementation in progress (22 November 2026) |

## Technology Stack

| Layer | Technology |
|---|---|
| **Frontend** | React + Vite + TypeScript |
| **Backend** | Python 3.11 + FastAPI + Uvicorn |
| **LLM API** | Google Gemini API (`google-generativeai` SDK) |
| **Validation** | Pydantic v2 (JSON schema enforcement) |
| **Environment** | `.env` file for secret management |

## Supported Languages

| Language | Source | Target | Notes |
|---|---|---|---|
| Python | ✅ | ✅ | Primary source language in test suite |
| Java | ✅ | ✅ | Primary target language in test suite |
| C++ | ✅ | ✅ | Secondary target language |

> [!NOTE]
> Only a documented subset of each language is supported. Advanced features (decorators, reflection, generics, templates, macros, async/await, OS-level calls) are explicitly flagged as out of scope.

## Key Design Decisions

1. **4-Prompt Chain (P1 → P2 → P3 → P4):**
   - P1: Static Analysis — understands source semantics before translating
   - P2: Translation — guided by P1's structured JSON analysis
   - P3: Semantic Review — independently compares source, analysis, and translation
   - P4: Test Generation — proposes (not executes) test cases

2. **JSON Schema Validation:**
   Each LLM response is validated against a strict Pydantic schema before the next step. Malformed responses are caught and reported without crashing the pipeline.

3. **No Arbitrary Code Execution:**
   The backend never executes user-supplied code. All test cases are "proposed" — the model derives expected outputs analytically, not by running code.

4. **Separation of Concern per Prompt:**
   Each prompt has a single responsibility. No prompt is asked to both translate and review simultaneously.

5. **Assumption Transparency:**
   P1 and P2 both have explicit `assumptions` fields. Users can see exactly what the model assumed.

## Team

> [!IMPORTANT]
> **[TO BE PROVIDED]** — Team member names and enrollment numbers must be filled in before submission.

| Role | Name | Enrollment No. |
|---|---|---|
| Team Member 1 | [TO BE PROVIDED] | [TO BE PROVIDED] |
| Team Member 2 | [TO BE PROVIDED] | [TO BE PROVIDED] |
| Team Member 3 | [TO BE PROVIDED] | [TO BE PROVIDED] |

## Repository

- **GitHub / GitLab URL:** [TO BE PROVIDED]
- **Branch:** `main`

## Important Dates

| Milestone | Deadline | Status |
|---|---|---|
| M1 Proposal | [Original deadline passed] | Completed |
| M2 Prototype | 22 November 2026, 11:59 PM | In Progress |
| M3 Final | 1 December 2026 | Not Started |
