# M1 Proposal — CodeBridge: Semantics-Aware Code Translation and Verification

**Course:** Prompt Engineering (SCSE4041)
**Problem Pool:** C7
**Submission:** Milestone 1

> [!NOTE]
> This proposal represents the team's planned approach as of M1.
> **[TO BE PROVIDED]:** team details, actual stakeholder feedback date, actual citations.
> Replace all `[TO BE PROVIDED]` placeholders before final submission.

---

## 1. Project Title

**CodeBridge — Semantics-Aware Code Translation and Verification**

---

## 2. Problem Statement

### 2.1 The Problem

Software engineers frequently need to migrate code between programming languages — porting a Python data-processing script to Java for integration into an enterprise system, or translating a Java library to C++ for a performance-critical application. This task is tedious, error-prone, and time-consuming because:

- **Semantic differences are subtle:** Integer division, null handling, truthiness, collection mutability, string immutability, and exception models differ significantly across languages. A direct token-for-token translation frequently produces syntactically valid but semantically incorrect code.
- **Existing tools are shallow:** Simple transpilers perform syntactic translation with no semantic reasoning. General-purpose LLMs (ChatGPT, Copilot) produce translations but do not explicitly document their assumptions, verify semantic equivalence, or propose structured test cases.
- **Verification is manual:** After translation, engineers must manually review the output for correctness — a task requiring deep knowledge of both languages.

### 2.2 Target Users

| User Group | Pain Point |
|---|---|
| Software engineers | Spending hours manually porting functions; missing subtle semantic bugs |
| Students learning new languages | No structured explanation of *why* translated code differs |
| Small teams without formal migration tooling | No budget for proprietary migration suites |
| Educators | Need concrete examples of cross-language semantic differences |

---

## 3. Why Prompt Engineering?

Code translation requires **reasoning**, not just pattern matching. A prompt-engineered LLM pipeline can:

1. **Analyse before translating** — understand the source code's intent, control flow, and edge cases before producing any output.
2. **Apply structured constraints** — via JSON schema enforcement, ensuring each pipeline stage produces machine-parseable output.
3. **Verify its own translation** — by comparing source semantics against translated output in a separate step, reducing self-reinforcing errors.
4. **Document uncertainty explicitly** — assumptions and unsupported constructs are surfaced to the user rather than silently handled.

Traditional rule-based transpilers cannot perform this level of semantic reasoning. A single-prompt "translate this code" approach produces no structured analysis and cannot self-review.

---

## 4. Proposed Workflow

CodeBridge chains four sequential prompts. Each prompt receives the structured JSON output of the previous step as context.

```
User Input (source code, source lang, target lang)
        │
        ▼
  ┌─────────────────────────────────────────────────┐
  │  P1 — Static Analysis                           │
  │  Analyse source: functions, control flow,       │
  │  semantics, edge cases, unsupported constructs  │
  └─────────────────────┬───────────────────────────┘
                        │ JSON (P1Analysis)
                        ▼
  ┌─────────────────────────────────────────────────┐
  │  P2 — Semantics-Aware Translation               │
  │  Translate guided by P1 analysis.               │
  │  State assumptions; flag unsupported features   │
  └─────────────────────┬───────────────────────────┘
                        │ JSON (P2Translation)
                        ▼
  ┌─────────────────────────────────────────────────┐
  │  P3 — Semantic Review                           │
  │  Compare source, analysis, translation.         │
  │  Identify mismatches, risks, questions          │
  └─────────────────────┬───────────────────────────┘
                        │ JSON (P3Review)
                        ▼
  ┌─────────────────────────────────────────────────┐
  │  P4 — Test Generation                           │
  │  Propose test cases covering normal, edge,      │
  │  boundary scenarios from P1 analysis            │
  └─────────────────────┴───────────────────────────┘
                        │
                        ▼
            User-Readable Report + Translated Code
```

### Stage Responsibilities

| Stage | Input | Output | Key Responsibility |
|---|---|---|---|
| P1 | Source code | Structured analysis JSON | Extract semantics without translating |
| P2 | Source + P1 JSON | Translated code + assumption JSON | Translate with full semantic context |
| P3 | Source + P1 + P2 | Findings JSON (severity-tagged) | Independent semantic review |
| P4 | Source + P2 + P3 | Test case proposals JSON | Propose tests targeting findings |

---

## 5. Existing Solutions Survey

> [!WARNING]
> The citations and tool descriptions below are placeholder summaries for M1 purposes.
> **Replace with actually consulted sources before final submission.**

### 5.1 GitHub Copilot

**Capability:** GitHub Copilot can suggest code completions and, with prompting, translate code snippets between languages.
**Assumption treatment:** Assumptions are implicit and not surfaced to the user.
**Review/testing:** No structured review step; no test generation specific to the translation.
**Limitation:** Functions as a completion tool, not a dedicated translation pipeline. No JSON-structured semantic analysis. No assumption export.
**Source:** [github.com/features/copilot] — *[TO BE PROVIDED: actual paper/doc consulted]*

### 5.2 ChatGPT / GPT-4

**Capability:** With a well-crafted prompt, GPT-4 produces high-quality translations.
**Assumption treatment:** Varies by prompt; not structured or guaranteed.
**Review/testing:** Can review if prompted, but in a single session without separation of concerns.
**Limitation:** No persistent structured pipeline. Each conversation is independent. No schema enforcement. User must manually chain prompts.
**Source:** OpenAI documentation — *[TO BE PROVIDED: actual paper/doc consulted]*

### 5.3 Classic Transpilers (j2py, CoffeeScript compilers, etc.)

**Capability:** Rule-based, syntax-driven translation between specific language pairs.
**Assumption treatment:** None — purely syntactic.
**Review/testing:** None built in.
**Limitation:** Cannot handle semantic mismatches. Limited to specific language pairs. No reasoning about edge cases.
**Source:** j2py GitHub repository — *[TO BE PROVIDED: actual paper/doc consulted]*

### 5.4 CodeBridge's Differentiator

CodeBridge demonstrates a narrower, documented workflow with:
- Explicit assumption reporting (every assumption logged in the output)
- Structured semantic review by a separate prompt step
- Proposed test cases derived from the analysis
- JSON schema validation at every stage

**This is not a universal improvement claim.** CodeBridge supports a limited language subset and relies on a commercial LLM API. The gap vs. the tools above is in *workflow structure and transparency*, not raw translation quality.

---

## 6. Technology Proposal

| Component | Technology | Rationale |
|---|---|---|
| LLM | Gemini 1.5 Flash | Long context window; available via free-tier API; competitive at code tasks |
| Backend | Python 3.11 + FastAPI | Rapid development; native `google-generativeai` SDK; Pydantic validation |
| Frontend | React + Vite + TypeScript | Modern, fast dev setup; Monaco editor for syntax-highlighted code |
| Validation | Pydantic v2 | Strict JSON schema enforcement; structured error messages |
| Deployment | Local (`localhost:8000` + `localhost:5173`) | Sufficient for prototype; can be deployed to Cloud Run / Vercel for M3 |

---

## 7. Risks and Mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Gemini API returns malformed JSON | Medium | Strip markdown fences; retry once; return partial result with error note |
| Model fails on complex constructs | Medium | Explicitly flag `unsupported_or_ambiguous` constructs in P1; never silently skip |
| Free-tier rate limits | Medium | Test with small inputs; cache responses during development |
| Semantic bugs not caught by P3 | Medium | Acknowledge limitation; P4 test cases help surface them |
| Out-of-scope constructs | Low | Document supported subset; P1 flags unsupported constructs |

---

## 8. Team

> [!IMPORTANT]
> **[TO BE PROVIDED]** — Fill in team details before submission.

| Role | Name | Enrollment No. |
|---|---|---|
| Team Lead | [TO BE PROVIDED] | [TO BE PROVIDED] |
| Member | [TO BE PROVIDED] | [TO BE PROVIDED] |
| Member | [TO BE PROVIDED] | [TO BE PROVIDED] |

**Stakeholder feedback date:** [TO BE PROVIDED]
**Supervisor / TA:** [TO BE PROVIDED]
