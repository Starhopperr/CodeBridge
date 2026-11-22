# CodeBridge --- Antigravity Execution Pack

**Project:** CodeBridge --- Semantics-Aware Code Translation and
Verification\
**Problem pool:** C7 --- Code translation between languages\
**Course:** Prompt Engineering (SCSE4041)\
**Model:** Use Gemini 3.8 Flash only if that exact model is available;
record the actual API model ID.

## How to use

1.  Open the project workspace in Antigravity.
2.  Copy the full contents of this pack into the workspace, preserving
    filenames.
3.  Give Antigravity the instruction in `06_ACCEPTANCE_AND_HANDOFF.md`.
4.  Ask it to inspect existing work before modifying anything.
5.  Execute milestones in order, but prioritize M2's immediate
    submission requirements and M3's remaining work.

## Non-negotiable rules

-   Never invent team details, feedback, citations, screenshots, test
    results, links, commits or submission confirmations.
-   Use `[TO BE PROVIDED]` for missing team metadata.
-   Preserve the original Milestone 1 submission. Any later additions
    must be labelled as later additions, not backdated.
-   Never expose API keys. Use `.env`, `.env.example` and `.gitignore`.
-   Do not claim semantic equivalence because an LLM says so. Separate
    model review from executable test evidence.
-   Do not run arbitrary generated code on a public server. Any
    execution must be isolated with strict resource limits and no
    network/secrets; otherwise label tests as proposed, not executed.
-   Keep every prompt version, test input, actual output, evaluation
    record and real screenshot.
-   Do not hide failures or report unrun tests as passed.
-   Prefer a reliable small MVP over unfinished features.

## Product scope

Accept a code snippet and source/target language. Analyse it, translate
it, explain language differences and assumptions, review likely semantic
mismatches, and generate test cases. Initial languages: Python, Java and
C++, limited to a documented subset. Unsupported constructs must be
flagged rather than silently mistranslated.

## Prompt-engineering core

P1 source analysis → P2 constrained translation → P3 semantic review →
P4 test generation. Demonstrate task decomposition, role/context
prompting, explicit constraints, structured output, prompt chaining,
meaningful iteration and test-based evaluation.

## First Antigravity actions

-   Inspect the workspace and current implementation.
-   Create `docs/PROJECT_FACTS.md` and `docs/MILESTONE_STATUS.md`.
-   Create the repository structure in `04_REPOSITORY_AND_EVIDENCE.md`.
-   Implement and test the core workflow.
-   Populate milestone documents only from actual project evidence.
-   Reconcile all counts, names, model IDs, links and results before
    submission.
