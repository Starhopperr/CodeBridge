---
id: p4_final
version: final
step: 4
purpose: Production test case generation — receives P1, P2, P3 JSON automatically via pipeline
model: gemini-1.5-flash
variables:
  - source_language
  - target_language
  - source_code
  - translated_code
  - analysis_json
  - review_json
chain_position: fourth_and_final
chain_input_from: p3_final
chain_output_to: null
---

# P4 Final — Production Test Generation Prompt

> [!NOTE]
> **Final/production chained workflow.**
> Identical in specification to `prompts/v3/p4_v3.md`.
> Fourth and final step of the automated pipeline (`backend/pipeline.py`).
> Generates proposed test cases validated by Pydantic (`P4Tests` schema).

---

## System Prompt

```
Design tests for code translation.
Propose normal, boundary, empty-input and algorithm-specific cases based on the source.
Derive expected outputs from the original only when reliable; otherwise mark human
confirmation required.
Include tests targeting review findings.
Do not claim execution.
Return ONLY valid JSON.
```

---

## User Prompt

```
Design test cases for the translation from {{source_language}} to {{target_language}}.

Source Language: {{source_language}}
Target Language: {{target_language}}

Original Source Code:
<<<SOURCE_CODE_START>>>
{{source_code}}
<<<SOURCE_CODE_END>>>

Translated Code:
<<<TRANSLATION_START>>>
{{translated_code}}
<<<TRANSLATION_END>>>

P1 Analysis:
<<<ANALYSIS_START>>>
{{analysis_json}}
<<<ANALYSIS_END>>>

P3 Review Findings:
<<<REVIEW_START>>>
{{review_json}}
<<<REVIEW_END>>>

Return ONLY valid JSON with these exact fields:
{
  "test_cases": [
    {
      "test_id": "<TC-001, TC-002, ...>",
      "purpose": "<what this test verifies>",
      "input": "<the exact input to pass to the function/program>",
      "expected_output": "<the expected output or return value, derived from source behaviour>",
      "expected_output_confidence": "<high | medium | requires_human_confirmation>",
      "case_type": "<normal | boundary | empty_input | algorithm_specific | review_targeted>",
      "risk_target": "<finding ID from P3 this targets, or 'general'>"
    }
  ],
  "coverage_notes": "<explanation of what cases were chosen, what P3 findings are targeted, and any gaps>"
}
```

---

## Validation Schema

Validated via `backend/schemas.py::P4Tests`.
