# Test Case: CB-T03

- **Test ID:** CB-T03
- **Type:** Normal
- **Source Language:** Python
- **Target Language:** C++
- **Description:** For loop accumulator summing positive numbers in an array

## Source Code

```python
def sum_positive_numbers(numbers: list[int]) -> int:
    """Calculate the sum of all strictly positive integers in the provided list.
    Empty list or list with no positive numbers returns 0.
    """
    total = 0
    for num in numbers:
        if num > 0:
            total += num
    return total


if __name__ == "__main__":
    sample = [-3, 10, 0, 4, -1, 5]
    print("Sum of positive numbers:", sum_positive_numbers(sample))
```

## Expected Behaviour (Pre-defined)

1. Static analysis (P1) detects:
   - Function taking `list[int]` and returning `int`.
   - Accumulator pattern starting at 0.
   - Filtering condition `num > 0`.
2. Translation (P2) produces idiomatic C++:
   - Takes `const std::vector<int>& numbers`.
   - Uses range-based for loop `for (int num : numbers)` or `std::accumulate`.
   - Returns `int` or `long long` depending on accumulation size assumption.
3. Review (P3) checks that vector bounds and reference passing are efficient (`const &`), and checks for possible 32-bit signed integer overflow in C++.
4. Tests (P4) propose tests for empty vector `{}`, all negatives `{-1, -2}`, mixed `{-3, 10, 0, 4, -1, 5}`, and all positive.
