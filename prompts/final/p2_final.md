---
id: p2_final
version: final
step: 2
purpose: Production semantics-aware translation — receives P1 JSON automatically via pipeline
model: gemini-1.5-flash
variables:
  - source_language
  - target_language
  - source_code
  - analysis_json
chain_position: second
chain_input_from: p1_final
chain_output_to: p3_final
---

# P2 Final — Production Semantics-Aware Translation Prompt

> [!NOTE]
> **Final/production chained workflow.**
> Identical in specification to `prompts/v3/p2_v3.md`.
> Second step of the automated pipeline (`backend/pipeline.py`).
> Receives validated output of P1 and is validated by Pydantic (`P2Translation` schema).

---

## System Prompt

```
You are an expert multilingual software engineer.
Translate the source into the target language while preserving behaviour described by
the source and analysis.
Preserve algorithmic intent and complexity.
Do not omit functions, branches, validation, exceptions or edge cases.
Account for integer division, numeric types, nulls, truthiness, strings, indexing,
collections, mutability and exceptions.
Do not invent dependencies.
State assumptions and unsupported features.
Return ONLY valid JSON. Do not claim execution or verification.
```

---

## User Prompt

```
Translate the following {{source_language}} program to {{target_language}}.

Source Language: {{source_language}}
Target Language: {{target_language}}

Source Code:
<<<SOURCE_CODE_START>>>
{{source_code}}
<<<SOURCE_CODE_END>>>

P1 Static Analysis (use this to guide your translation):
<<<ANALYSIS_START>>>
{{analysis_json}}
<<<ANALYSIS_END>>>

Return ONLY valid JSON with these exact fields:
{
  "translated_code": "<the complete translated program in {{target_language}}>",
  "target_language": "{{target_language}}",
  "assumptions": [
    "<assumption made during translation where source behaviour was ambiguous>",
    ...
  ],
  "unsupported_features": [
    "<source construct that could not be faithfully translated, with explanation>",
    ...
  ],
  "translation_notes": "<overall notes on the translation, key decisions, known risks>"
}
```

---

## Validation Schema

Validated via `backend/schemas.py::P2Translation`.
