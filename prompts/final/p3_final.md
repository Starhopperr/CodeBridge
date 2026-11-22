---
id: p3_final
version: final
step: 3
purpose: Production independent semantic review — receives P1 and P2 JSON automatically via pipeline
model: gemini-1.5-flash
variables:
  - source_language
  - target_language
  - source_code
  - analysis_json
  - translated_code
chain_position: third
chain_input_from: p2_final
chain_output_to: p4_final
---

# P3 Final — Production Semantic Review Prompt

> [!NOTE]
> **Final/production chained workflow.**
> Identical in specification to `prompts/v3/p3_v3.md`.
> Third step of the automated pipeline (`backend/pipeline.py`).
> Evaluates semantic equivalence independently and outputs findings validated by Pydantic (`P3Review` schema).

---

## System Prompt

```
Independently compare the source, analysis and target program.
Look for changed behaviour, missing branches/functions, type conversions, integer division,
overflow, null handling, collection/indexing differences, exception behaviour, ordering
assumptions, I/O mismatches and boundary errors.
Do not assume correctness.
Do not invent defects; explain evidence.
Distinguish definite defects, risks and questions.
Return ONLY valid JSON. Do not claim tests ran without test evidence.
```

---

## User Prompt

```
Perform an independent semantic review of the following translation from {{source_language}} to {{target_language}}.

Source Language: {{source_language}}
Target Language: {{target_language}}

Original Source Code:
<<<SOURCE_CODE_START>>>
{{source_code}}
<<<SOURCE_CODE_END>>>

P1 Static Analysis:
<<<ANALYSIS_START>>>
{{analysis_json}}
<<<ANALYSIS_END>>>

P2 Translated Code:
<<<TRANSLATION_START>>>
{{translated_code}}
<<<TRANSLATION_END>>>

Return ONLY valid JSON with these exact fields:
{
  "overall_assessment": "<PASS | PASS_WITH_RISKS | FAIL>",
  "findings": [
    {
      "severity": "<definite_defect | risk | question>",
      "location": "<function name, line reference, or construct>",
      "explanation": "<what the problem is and what evidence supports this finding>",
      "correction": "<suggested correction or action to resolve this finding>"
    }
  ],
  "summary": "<one paragraph overall assessment of the translation quality and key risks>"
}
```

---

## Validation Schema

Validated via `backend/schemas.py::P3Review`.
