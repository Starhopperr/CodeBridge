# Milestone 1 --- Problem Identification, Use-Case and Prompt Proposal

> M1's original deadline has passed. Audit the submitted proposal and
> fill genuine gaps. Do not backdate new work or fabricate stakeholder
> feedback.

## Rubric (8 marks)

  -------------------------------------------------------------------------
  Component                                    Marks Evidence
  --------------------- ---------------------------- ----------------------
  Project title /                                1.0 Clear title and
  prompt-engineering                                 concise use case
  use case                                           

  Problem and user                               1.0 Problem, users,
  context                                            context, inputs and
                                                     outcome

  Reason for selection                           0.5 Why selected and why
                                                     prompt engineering
                                                     matters

  Target users /                                 0.5 Users and
  stakeholders                                       beneficiaries

  Prompt-engineering                             1.0 Tasks, inputs and
  task definition                                    outputs

  Technology / model /                           0.5 Initial
  tool approach                                      model/tool/interface
                                                     rationale

  Existing solutions /                           1.0 Comparable tools and
  gap                                                defensible gap

  Research / evidence                            1.0 Credible sources,
                                                     domain references or
                                                     user evidence

  Initial prompt /                               0.5 Baseline prompt and
  workflow concept                                   representative output

  Industry / faculty /                           1.0 Genuine feedback,
  senior feedback                                    date, role and action;
                                                     otherwise mark pending
  -------------------------------------------------------------------------

## Project statement

**CodeBridge --- Semantics-Aware Code Translation and Verification.** A
prompt-engineering workflow for translating small, self-contained
programs between programming languages while making assumptions,
language differences and potential behavioural mismatches inspectable.

**Problem-pool mapping:** C7 --- Code translation between languages.
Confirm this matches the team's approved M1 selection before using it in
the final submission.

## Problem and users

-   Primary users: developers and computer-science learners porting
    small code snippets.
-   Inputs: source code, source language, target language, optional
    intent/context and optional examples.
-   Outputs: source analysis, translated code, language-difference
    notes, assumptions, reviewer findings and proposed tests.
-   Out of scope: whole repositories, complex build systems, proprietary
    dependencies, guaranteed correctness and unrestricted public code
    execution.

## Why prompt engineering?

Translation requires preserving intent and observable behaviour, not
merely rewriting syntax. The workflow uses decomposition, explicit
constraints, structured outputs, independent review and test generation
to expose uncertainty and support evaluation.

## Initial workflow

1.  Analyse source code without modifying it.
2.  Translate using the analysis and behavioural constraints.
3.  Review source and target for likely semantic mismatches.
4.  Generate normal, boundary and edge tests.
5.  Compare actual outputs only when a safe runner is available;
    otherwise mark tests as proposed.

## Existing solutions and research

Research at least three comparable tools/workflows (e.g. IDE assistants,
general LLM coding assistants and transpilers). Record official URL,
translation capability, treatment of assumptions/language differences,
review/testing features and observed limitations. Do not claim no tool
offers these capabilities; state the narrow opportunity demonstrated by
this project. Cite only sources actually consulted.

## Technology proposal

-   Frontend: React + Vite + TypeScript.
-   Backend: Python FastAPI.
-   Editor: Monaco if it does not delay the MVP; a simple editor is
    acceptable.
-   Model: configured Gemini model; record exact API model ID.
-   Storage: local JSON/SQLite if needed.
-   Execution: optional restricted local runner; never expose
    unrestricted arbitrary execution publicly.

## M1 outputs

-   `docs/M1_PROPOSAL.md`
-   `docs/M1_RUBRIC_AUDIT.md`
-   `research/COMPARABLE_TOOLS.md`
-   `prompts/v1/` baseline prompts and a real sample run
-   genuine feedback notes, if available

## Acceptance

Every claim is evidenced or labelled an assumption. No fabricated
feedback or references. The selected problem, users, task,
inputs/outputs, baseline prompt and sample run are explicit.
