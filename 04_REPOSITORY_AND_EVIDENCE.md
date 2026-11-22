# Repository, Evidence and Build Standards

## Suggested repository layout

``` text
CodeBridge/
├── README.md
├── CHANGELOG.md
├── .gitignore
├── .env.example
├── frontend/
├── backend/
├── prompts/
│   ├── v1/
│   ├── v2/
│   ├── v3/
│   └── final/
├── test-data/
│   ├── inputs/
│   ├── expected/
│   ├── outputs/
│   └── evaluation/
├── docs/
│   ├── PROJECT_FACTS.md
│   ├── MILESTONE_STATUS.md
│   ├── BUILD_LOG.md
│   ├── diagrams/
│   ├── screenshots/
│   ├── reports/
│   └── feedback/
└── scripts/
```

## Evidence rules

-   Save real runs with timestamp, prompt version, exact model ID,
    input, raw response and parsed output where safe.
-   Remove secrets/personal data before committing.
-   Use stable test IDs (`CB-T01` etc.).
-   Keep expected and actual outputs separate.
-   A test passes only when its acceptance condition is met.
-   Keep failed/unexpected outputs.
-   Screenshots must be captured from the running app and captioned with
    test IDs.
-   Never rewrite old prompt versions; add new versions.

## Security

-   API keys only in environment variables; `.env` ignored by Git.
-   Validate input size and language choices.
-   Add timeouts, retry limits and clear error handling.
-   Never use `eval` or execute model output directly in the backend.
-   Public arbitrary code execution is out of scope unless robust
    isolation is implemented.
-   If running code: isolate with CPU/memory/time limits, no network,
    temporary filesystem and process cleanup.
-   Treat submitted source code as untrusted input; avoid sending
    proprietary code or personal data without consent.

## README must include

Summary/scope; supported languages and unsupported constructs;
architecture/prompt workflow; prerequisites/setup commands; environment
variable names (not values); run/test commands; experiment reproduction;
screenshots/demo; team placeholders; limitations and responsible-use
notes.

## Build log template

``` markdown
## YYYY-MM-DD — Task
- Owner:
- Files changed:
- Work completed:
- Tests executed:
- Results:
- Known issues:
- Next action:
```

## Contribution evidence

Each member must have a specific task and evidence (file, prompt ID,
test set, diagram, report section or commit) and be able to explain it.
Percentages are agreed by the team and total 100%.
