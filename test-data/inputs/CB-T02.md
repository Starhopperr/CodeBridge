# Test Case: CB-T02

- **Test ID:** CB-T02
- **Type:** Normal
- **Source Language:** Python
- **Target Language:** Java
- **Description:** Conditional FizzBuzz generator returning a list of strings

## Source Code

```python
def fizzbuzz(limit: int) -> list[str]:
    """Generate FizzBuzz outputs from 1 up to limit inclusive.
    Multiples of 15 yield 'FizzBuzz', 3 yield 'Fizz', 5 yield 'Buzz'.
    """
    if limit < 1:
        return []
    
    results = []
    for i in range(1, limit + 1):
        if i % 15 == 0:
            results.append("FizzBuzz")
        elif i % 3 == 0:
            results.append("Fizz")
        elif i % 5 == 0:
            results.append("Buzz")
        else:
            results.append(str(i))
    return results


if __name__ == "__main__":
    output = fizzbuzz(15)
    print(", ".join(output))
```

## Expected Behaviour (Pre-defined)

1. Static analysis (P1) identifies loop iteration `1` to `limit` inclusive, conditional branches checking `% 15`, `% 3`, `% 5`, string conversion of integers, and edge case `limit < 1` returning an empty list.
2. Translation (P2) translates to Java using `List<String>` and `ArrayList<String>`. Correct loop bounds (`int i = 1; i <= limit; i++`), string conversions (`String.valueOf(i)` or `Integer.toString(i)`), and modulo operators `%`.
3. Review (P3) confirms condition precedence order (15 before 3 and 5) is preserved.
4. Tests (P4) propose tests for `limit = 0`, `limit = 1`, `limit = 5`, `limit = 15`.
