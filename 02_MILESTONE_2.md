# Milestone 2 --- Prompt Design, Experimentation, Implementation and Demonstration

> The latest student-specific instructions supplied in this conversation
> state the deadline as **22 November 2026, 11:59 PM**, team leader
> submits once. The general project PDF contains an older 2 November
> date. Check the LMS for any later update and follow the latest
> official instruction.

## Submission package

1.  `M2_<TeamID>_CodeBridge.pdf` (max 10 MB).
2.  Separate 1--2 page supporting-document PDF (max 10 MB); recommended
    type: **Technical Report**.
3.  Prototype link.
4.  Public GitHub repository or viewable Drive/OneDrive folder.
5.  90--150 second reel link and exact duration.
6.  Team metadata, prompt count, test-row count, prompt-version count,
    working modules and contribution table.

Use the original Team ID/team name from M1. Team leader submits once.
Verify every link in a private/incognito window.

## Exact PDF structure --- seven sections

### 1. Cover page

Team ID, team name, project title, batch/group, faculty, all
members/enrollment numbers, prototype/repository/reel links.

### 2. Prompt and solution design

Half-to-one-page overview: problem/users, inputs/outputs, number of
prompt steps and rationale, tool/model and rationale, changes since M1.
Include prompt workflow, task decomposition, input-output and system
architecture diagrams (or screen flow for no-code). Include one prompt
sheet per final prompt.

Each prompt sheet must include: ID/name, workflow step, purpose, tool
and exact model ID, settings, full system prompt, full user template
with variables, variable meanings, number of examples, output
format/schema and one real sample run (input and actual output).

### 3. Implementation

What is built; module table
(`Module | What it does | Status: Working / Partly working / Not started | Notes`);
prompt iteration log with at least 3 meaningful versions and full prompt
texts.

### 4. Demonstration and testing

At least 10 unique test rows, including at least 3 Edge/Invalid cases.
Use columns: Test ID, input summary, type (Normal/Edge/Invalid),
expected result, actual result, Pass/Fail, evidence path. Include 2--3
genuine screenshots captioned with test IDs, plus 2--4 limitations and
next steps. Failed tests are acceptable; hiding them is not.

### 5. Repository

One repository/folder screenshot and 3--5 lines explaining changes since
M1.

### 6. Supporting document

Insert the same 1--2 page technical report uploaded separately. Cover
architecture, tools/models, prompt design, test results and limitations.

### 7. Team contribution

Table: member name, enrollment number, role, tasks done in M2, evidence
and contribution percentage. Every member needs a specific task and
evidence; percentages total 100 and members agree.

## Prompt pipeline

-   **P1 Source analyser:** identify intent, functions, inputs/outputs,
    data structures, control flow, dependencies, language semantics,
    edge cases and unsupported/ambiguous constructs. Do not rewrite
    code.
-   **P2 Constrained translator:** translate while preserving behaviour
    and algorithmic intent; state assumptions, language differences and
    unsupported features.
-   **P3 Semantic reviewer:** compare source and target for missing
    functionality, changed control flow, type conversions, integer
    division, null handling, collection/indexing and boundary risks. Do
    not assume correctness.
-   **P4 Test designer:** generate normal, boundary, empty-input and
    algorithm-specific tests. Mark uncertain expected outputs for human
    review.

The implementation may combine model calls only if the logical stages
remain clear and evidenceable. Count prompts according to distinct final
prompt sheets/LLM calls actually used.

## Meaningful prompt versions

-   V1 baseline: broad single-step translation.
-   V2 constrained: explicit role, source/target, behavioural
    constraints, unsupported-feature handling and structured output.
-   V3 chained/final: analysis → translation → review → test generation
    with schema validation and uncertainty reporting.

These are intended experiment variants, not results. Run the same fixed
test set against each version. Save exact inputs, outputs, model
ID/settings and observations. Mark unrun variants as not tested.

## Minimum test categories

1.  Arithmetic function (Normal).
2.  Conditional branching (Normal).
3.  Loop and accumulator (Normal).
4.  List/array traversal (Normal).
5.  String processing (Normal).
6.  Map/dictionary counting (Normal).
7.  Empty collection (Edge).
8.  Zero and negative values (Edge).
9.  Integer division/rounding boundary (Edge).
10. Unsupported dependency, malformed snippet or ambiguous intent
    (Invalid).

Use unique real code inputs. Define expected behaviour before running
the model.

## Evaluation

Measure applicable metrics: syntax/compile success, executable test pass
rate, behavioural match, completeness, reviewer usefulness, schema
validity, unsupported-feature disclosure and latency/model-call count if
collected. Report numerator and denominator. Never invent scores or use
an LLM self-rating as ground truth.

## Module status

Suggested modules: editor/language selection; analysis; translation;
review; test generation; safe execution/comparison (only if
implemented); results/export; experiment logging. Mark Working only
after a fresh end-to-end check. A UI placeholder is not a working
module.

## Reel

90--150 seconds: problem (\~10s), prompt before/after experiment
(30--40s), real demo (40--60s), progress/next steps (15--20s).
Voice-over or captions; faces optional. Must show real app/model runs,
not slides alone.

## Final reconciliation

Generate `docs/M2_FORM_VALUES.md` with exact team metadata, prompt
count, test-row count, prompt-version count, working module names,
links, reel duration, supporting document type and member task lines.
All values must match the PDF. Test links in incognito, check both PDFs
are under 10 MB and submit once through the team leader.
