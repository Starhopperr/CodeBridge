# Test Case: CB-T08

- **Test ID:** CB-T08
- **Type:** Edge
- **Source Language:** Python
- **Target Language:** C++
- **Description:** Function with zero and negative value boundary edge cases

## Source Code

```python
def classify_and_clamp(val: int, lower: int, upper: int) -> dict[str, int | str]:
    """Clamp an integer val between lower and upper bounds and determine its sign.
    lower must be less than or equal to upper.
    """
    if lower > upper:
        raise ValueError("lower bound cannot exceed upper bound")
        
    clamped = max(lower, min(val, upper))
    
    if clamped > 0:
        sign = "positive"
    elif clamped < 0:
        sign = "negative"
    else:
        sign = "zero"
        
    return {"clamped": clamped, "sign": sign}


if __name__ == "__main__":
    print(classify_and_clamp(0, -10, 10))
    print(classify_and_clamp(-15, -10, 10))
    print(classify_and_clamp(25, -10, 10))
```

## Expected Behaviour (Pre-defined)

1. Static analysis (P1) identifies:
   - Dynamic return dictionary with mixed types `int | str`.
   - Bounds validation `lower > upper`.
   - Boundary cases around 0, negative values, and lower/upper clamping limits.
2. Translation (P2) translates to C++:
   - C++ requires a typed structure (e.g., `struct ClampResult { int clamped; std::string sign; };`) or `std::pair<int, std::string>`.
   - `std::clamp` (C++17) or `std::max(lower, std::min(val, upper))` can be used.
   - Throws `std::invalid_argument` for `lower > upper`.
3. Review (P3) evaluates type representation in C++ and verifies zero sign handling.
4. Tests (P4) propose tests for `val = 0`, `val = lower`, `val = upper`, `val < lower`, `val > upper`, and `lower > upper` exception.
