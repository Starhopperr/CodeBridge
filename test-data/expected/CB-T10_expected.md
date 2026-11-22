# Expected Result Specification: CB-T10

## Metadata
- **Test ID:** CB-T10
- **Case Type:** Invalid
- **Source Language:** Python
- **Target Language:** Java
- **Target Component:** Malformed input handling and syntax error flagging

---

## 1. P1 Static Analysis Expectations
- **Functions:** Source code contains malformed syntax on function declaration and statement lines:
  - Missing colon after `def broken_syntax_calculator(x, y)`
  - Unclosed parenthesis on line 3 `(x * 2 + (y / 3)`
  - Missing colons on `if` and `else` statements
  - Incomplete return statements `return result *` and `return result -`
- **Ambiguity & Unsupported Constructs:** P1 MUST flag these lines in `unsupported_or_ambiguous`.
- **Confidence:** Must be marked as low / caveat in `confidence_notes`.
- **Assumptions:** If analysis attempts to interpret the intended algorithm, it must explicitly document every repair assumption.

---

## 2. P2 Translation Expectations
- Two acceptable model behaviours:
  - **Option A (Strict):** States in `unsupported_features` that the code cannot be translated faithfully due to syntax errors.
  - **Option B (Heuristic repair with explicit assumptions):** Repairs syntax (e.g. assuming `result * 2` and `result - 1`), but logs every repair assumption in the `assumptions` array and adds caveats to `translation_notes`.
- Must NOT produce code while pretending the input was valid.

---

## 3. P3 Review Expectations
- Assessment: `FAIL` or `PASS_WITH_RISKS`.
- Findings: At least one `definite_defect` or high `risk` finding stating:
  - Source program has severe syntax errors.
  - Translated code is based on speculative reconstruction of incomplete expressions.

---

## 4. P4 Test Proposals Expectations
- Proposed tests should be flagged with:
  - `expected_output_confidence: "requires_human_confirmation"`.
  - Targeted against P3 finding on broken syntax.
- Notes should explicitly state that the original program cannot be executed in Python to verify expected outputs.
