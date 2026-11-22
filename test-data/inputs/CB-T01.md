# Test Case: CB-T01

- **Test ID:** CB-T01
- **Type:** Normal
- **Source Language:** Python
- **Target Language:** Java
- **Description:** Recursive factorial function with base case validation

## Source Code

```python
def factorial(n: int) -> int:
    """Compute the factorial of a non-negative integer n.
    Raises ValueError if n is negative.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


if __name__ == "__main__":
    test_values = [0, 1, 5, 7]
    for val in test_values:
        print(f"factorial({val}) = {factorial(val)}")
```

## Expected Behaviour (Pre-defined)

1. Static analysis (P1) should identify:
   - Function `factorial(n: int) -> int` with recursion and input validation.
   - Base cases: `n == 0` and `n == 1` returning 1.
   - Validation checks for negative values (`ValueError`) and non-integers (`TypeError`).
2. Translation (P2) should produce valid Java code:
   - A public class (e.g., `Factorial`) with a static method `public static long factorial(int n)`.
   - `IllegalArgumentException` thrown for `n < 0`.
   - Recursive call preserving multiplication order and base cases.
3. Review (P3) should confirm algorithmic equivalence and identify any potential integer overflow for large `n` (noting 32-bit `int` vs 64-bit `long` vs Python arbitrary precision).
4. Tests (P4) should propose tests for: `0`, `1`, `5` (returns 120), negative number (`-1` throws exception), and large input boundary.
