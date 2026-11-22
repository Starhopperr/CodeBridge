# Test Case: CB-T10

- **Test ID:** CB-T10
- **Type:** Invalid
- **Source Language:** Python
- **Target Language:** Java
- **Description:** Malformed Python snippet with broken syntax and unclosed brackets

## Source Code

```python
def broken_syntax_calculator(x, y)
    # Missing colon on function header
    result = (x * 2 + (y / 3)   # Unclosed parentheses
    if x > 10
        return result *
    else
        return result -
```

## Expected Behaviour (Pre-defined)

1. Static analysis (P1) should identify:
   - Malformed syntax: missing colon on `def broken_syntax_calculator`, unclosed parenthesis on line 3, missing colons on `if` and `else`, dangling operators on returns.
   - P1 should flag this in `unsupported_or_ambiguous` or note low confidence in `confidence_notes`.
   - The analysis should NOT attempt to hallucinate missing code without stating assumptions.
2. Translation (P2) should:
   - Either flag the code in `unsupported_features` as untranslatable, OR state explicit assumptions regarding how the syntax errors were fixed.
3. Review (P3) should report a `definite_defect` or `risk` indicating the source code is malformed and syntactically invalid.
4. Tests (P4) should identify that automated testing of the original function cannot run due to syntax errors, and mark confidence as `requires_human_confirmation`.
