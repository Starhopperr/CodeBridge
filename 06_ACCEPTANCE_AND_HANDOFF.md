# Acceptance Tests and Antigravity Handoff

## End-to-end scenario

1.  User opens CodeBridge and selects source/target languages.
2.  User pastes a supported snippet.
3.  Backend invokes P1, validates output, invokes P2, validates
    translation, then invokes P3 and P4.
4.  UI displays analysis, translated code, language differences,
    assumptions, review findings, generated tests and uncertainty.
5.  If a safe runner exists, user explicitly runs supported tests.
    Otherwise tests are clearly marked proposed/not executed.
6.  User can copy/export code and view/download a report.
7.  Unsupported language pairs, malformed responses and API failures are
    handled clearly.

## Functional acceptance checklist

-   [ ] Empty source is rejected clearly.
-   [ ] Unsupported languages are rejected.
-   [ ] Same-language translation is handled explicitly.
-   [ ] API/model failure does not lose input.
-   [ ] Malformed JSON is detected safely.
-   [ ] Missing code blocks are handled.
-   [ ] Long inputs are bounded.
-   [ ] Generated tests are distinguished from executed tests.
-   [ ] Review findings show severity and explanation.
-   [ ] No false "verified/equivalent" status is shown.
-   [ ] API key is absent from frontend, logs and Git.
-   [ ] Fresh setup/start commands work.

## Minimum evaluation

At least 10 unique cases and 3 or more Edge/Invalid cases. See
`02_MILESTONE_2.md`. Retain exact inputs, expected results, actual
results and evidence.

## Antigravity instruction

Read every Markdown file in this pack before coding.

**Phase A --- Inspect and plan** - Inspect current workspace and list
files/runtime/dependencies. - Identify existing implementation and
preserve useful work. - Create `docs/PROJECT_FACTS.md`,
`docs/MILESTONE_STATUS.md` and an implementation plan. - Use
placeholders for missing team facts; do not block on nonessential
unknowns.

**Phase B --- Build** - Implement the smallest coherent application
demonstrating P1→P2→P3→P4. - Keep prompts in versioned files, not buried
in UI code. - Validate model outputs with schemas. - Add loading/error
states and deterministic tests. - Configure model/API through
environment variables.

**Phase C --- Experiment** - Save V1, V2 and V3 separately. - Run the
same test inputs against each version. - Save raw outputs, model
ID/settings, validation status and measured results. - Preserve failures
and unrun cases.

**Phase D --- Evidence and documents** - Populate milestone documents
from actual facts. - Generate diagrams matching the implementation. -
Capture genuine screenshots. - Generate PDFs only after verifying
content and file size. - Prepare reel/video scripts; do not claim a
video exists until created.

**Phase E --- Quality gate** - Run full tests and clean setup. - Scan
for secrets. - Verify links in a private/incognito session. - Reconcile
names, dates, counts, model IDs, statuses and results across
documents. - Produce PASS/FAIL/BLOCKED checklist with evidence paths.

## Required phase handoff

Report completed work, files changed, commands/tests and results, known
issues, missing user facts and next actions. Anything incomplete must be
marked BLOCKED or NOT DONE, never silently represented as complete.
