# Test Case: CB-T07

- **Test ID:** CB-T07
- **Type:** Edge
- **Source Language:** Python
- **Target Language:** Java
- **Description:** Function with empty list and None input handled gracefully

## Source Code

```python
def compute_average(values: list[float] | None) -> float:
    """Compute the arithmetic mean of a list of floating-point values.
    Returns 0.0 if values is None or empty.
    """
    if not values:
        return 0.0
    
    total = sum(values)
    return total / len(values)


if __name__ == "__main__":
    print("Avg empty:", compute_average([]))
    print("Avg None:", compute_average(None))
    print("Avg values:", compute_average([1.5, 2.5, 5.0]))
```

## Expected Behaviour (Pre-defined)

1. Static analysis (P1) identifies:
   - Python truthiness check `if not values:` handles BOTH `None` and empty list `[]`.
   - Division by zero risk if empty list wasn't guarded.
   - Return type float.
2. Translation (P2) must explicitly translate `if not values:` to Java null and empty checks:
   - `if (values == null || values.isEmpty()) return 0.0;`
   - Failure to check both `null` and `.isEmpty()` would cause `NullPointerException` or division by zero (`NaN`).
3. Review (P3) explicitly verifies that both `null` and empty collection are safely intercepted.
4. Tests (P4) propose tests for `null`, `new ArrayList<Double>()`, and normal lists.
