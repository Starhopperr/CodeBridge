# COMPARABLE_TOOLS.md — Existing Solutions Research

**For:** CodeBridge M1/M2 — Prompt Engineering (SCSE4041), Problem Pool C7

> [!WARNING]
> The tool descriptions and limitations below are based on publicly known capabilities as of the research date.
> **Replace placeholder URLs with actually consulted sources before final submission.**
> Where a specific paper, blog post, or documentation page was read, cite it accurately.

---

## Comparison Framework

Each tool is evaluated on four axes:
1. **Translation Capability** — How well does it translate code between languages?
2. **Assumption Treatment** — Are translation assumptions surfaced to the user?
3. **Review / Verification** — Is there a structured review or test step?
4. **Known Limitations** — What does it not handle?

---

## 1. GitHub Copilot

**Type:** AI code completion / generation tool (GitHub / OpenAI)
**Primary Use Case:** Code completion, refactoring, and suggestion within an IDE
**URL:** https://github.com/features/copilot *(replace with actual doc page consulted)*

### Translation Capability
Copilot can translate code between languages when prompted (e.g. "Convert this Python function to Java"). It leverages a large code-trained model and produces syntactically plausible translations for common patterns. Quality varies significantly by construct complexity and language pair.

### Assumption Treatment
Assumptions are **implicit and not surfaced**. When Copilot translates code, it does not produce a list of what it assumed about edge cases, type handling, or semantic equivalence. The user must infer whether assumptions were made by reviewing the output.

### Review / Verification
No structured review step. Copilot does not independently compare its own translation to the source for semantic equivalence. It does not propose test cases for the translation.

### Known Limitations
- Functions as a suggestion tool, not a dedicated translation pipeline
- No JSON-structured output for downstream processing
- No explicit flagging of unsupported or ambiguous constructs
- No semantic analysis before translating
- Subscription required (free tier has limits)
- Translations can silently introduce semantic errors (e.g. integer division, exception handling differences)

---

## 2. ChatGPT / GPT-4 (Conversational LLM)

**Type:** General-purpose conversational LLM
**Primary Use Case:** General coding assistance, explanation, translation on demand
**URL:** https://chat.openai.com *(replace with actual paper/documentation consulted)*

### Translation Capability
GPT-4, when prompted carefully, produces high-quality code translations. It is capable of reasoning about semantic differences if explicitly asked. Translation quality is higher than Copilot for complex constructs when the user engineers the prompt well.

### Assumption Treatment
**Varies entirely by the user's prompt.** A simple "translate this to Java" prompt produces no assumption documentation. If the user adds "list your assumptions," GPT-4 will respond — but the output is unstructured prose, not a machine-parseable schema. There is no guarantee of completeness.

### Review / Verification
Can review its own translation if asked in a follow-up turn, but this is in the **same conversational context** — the model's self-review may be biased toward its own translation. No structured independent review. No test case proposals unless explicitly requested.

### Known Limitations
- No persistent structured pipeline — each conversation is independent
- No schema enforcement on output
- Self-review in the same context is not independent
- Relies entirely on the user to engineer the right prompts
- Rate limits on free tier; GPT-4 quality requires a paid subscription
- Cannot be programmatically integrated without the API, requiring additional setup
- No explicit differentiation between definite defects, risks, and open questions

---

## 3. Classic Transpilers (j2py, CoffeeScript → JavaScript, etc.)

**Type:** Rule-based syntactic transpiler
**Examples:** j2py (Java → Python), CoffeeScript compiler, Transcrypt, Babel
**URL:** https://github.com/natural/java2python *(replace with actual source consulted)*

### Translation Capability
Transpilers perform **syntactic, rule-based** translation. They map constructs from one language to another using predefined rules (e.g. `for (int i = 0; i < n; i++)` → `for i in range(n)`). They are fast and deterministic.

### Assumption Treatment
**None.** Transpilers do not reason about semantics. They apply rules without considering whether the semantic meaning is preserved. No assumptions are reported because no reasoning occurs.

### Review / Verification
**None.** Transpilers produce output and stop. There is no review pass, no semantic comparison, and no test generation.

### Known Limitations
- Purely syntactic — cannot handle semantic differences (integer division, null models, exception types, collection semantics)
- Narrow language pair support (each transpiler targets exactly one pair)
- Cannot handle constructs that have no syntactic equivalent in the target language
- Fail silently on unsupported constructs (may produce invalid or semantically wrong code without warning)
- Not maintained for most language pairs (many are abandoned projects)
- No LLM reasoning — quality bounded by the rule set written by the transpiler's authors

---

## 4. CodeBridge — Gap Analysis

> [!IMPORTANT]
> CodeBridge demonstrates a **narrower, documented workflow** with explicit assumption reporting and structured review — **not a universal improvement claim.**

| Capability | GitHub Copilot | ChatGPT / GPT-4 | Classic Transpilers | CodeBridge |
|---|---|---|---|---|
| Semantic analysis before translation | ❌ | ⚠️ (if prompted) | ❌ | ✅ (P1, always) |
| Structured JSON output at each stage | ❌ | ❌ | ❌ | ✅ (Pydantic-validated) |
| Explicit assumption documentation | ❌ | ⚠️ (prose, if asked) | ❌ | ✅ (structured field) |
| Independent semantic review step | ❌ | ⚠️ (same context) | ❌ | ✅ (P3, separate step) |
| Proposed test cases for the translation | ❌ | ⚠️ (if asked) | ❌ | ✅ (P4, structured) |
| Unsupported construct flagging | ❌ | ⚠️ (variable) | ❌ | ✅ (P1 `unsupported_or_ambiguous`) |
| Code execution / actual verification | ❌ | ❌ | ❌ | ❌ (not in scope for any) |
| Broad language support | ✅ | ✅ | ⚠️ (narrow pairs) | ⚠️ (3 languages, limited subset) |
| Free / open access | ⚠️ | ⚠️ | ✅ | ✅ (with API key) |

### Honest Position

CodeBridge's advantages are **workflow structure and transparency**, not raw translation power:
- It is narrower in scope than ChatGPT (only Python/Java/C++, only a documented subset)
- Its translation quality depends on Gemini 1.5 Flash, which may not outperform GPT-4 on complex cases
- It does not execute code, so no tool in this comparison (including CodeBridge) provides empirical semantic equivalence verification

CodeBridge's claim: *"For the documented language and construct subset, CodeBridge provides a more auditable, structured, and transparent translation workflow than the tools above — with explicit assumptions, structured review findings, and proposed tests."*

---

## Research Notes

> Replace this section with actual notes from papers and documentation you consulted.

| Source | Type | Key Finding | Consulted Date |
|---|---|---|---|
| [TO BE PROVIDED] | Paper / Blog | [TO BE PROVIDED] | [TO BE PROVIDED] |
| [TO BE PROVIDED] | Documentation | [TO BE PROVIDED] | [TO BE PROVIDED] |
| [TO BE PROVIDED] | GitHub Repository | [TO BE PROVIDED] | [TO BE PROVIDED] |
