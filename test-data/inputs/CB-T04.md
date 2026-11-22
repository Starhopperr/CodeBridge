# Test Case: CB-T04

- **Test ID:** CB-T04
- **Type:** Normal
- **Source Language:** Python
- **Target Language:** Java
- **Description:** List traversal to find the maximum element and its index

## Source Code

```python
def find_max_element(items: list[int]) -> tuple[int, int]:
    """Find the maximum integer in the list along with its first occurrence index.
    Raises ValueError if the input list is empty.
    """
    if not items:
        raise ValueError("Cannot find maximum of an empty list")
    
    max_val = items[0]
    max_idx = 0
    for idx in range(1, len(items)):
        if items[idx] > max_val:
            max_val = items[idx]
            max_idx = idx
            
    return max_val, max_idx


if __name__ == "__main__":
    nums = [12, 45, 7, 89, 45, 89, 23]
    val, idx = find_max_element(nums)
    print(f"Max value {val} at index {idx}")
```

## Expected Behaviour (Pre-defined)

1. Static analysis (P1) detects:
   - Function returning tuple `(int, int)`.
   - Empty list check throwing `ValueError`.
   - Linear scan finding first maximum element.
   - 0-based indexing.
2. Translation (P2) translates to Java:
   - Since Java does not have built-in tuples, P2 must create a custom class/record (e.g. `public record MaxResult(int value, int index)`) or return an `int[]` array.
   - Throws `IllegalArgumentException` or `NoSuchElementException` for empty list.
   - Iterates with standard `for (int i = 1; i < items.size(); i++)`.
3. Review (P3) highlights the tuple representation approach in Java and confirms strict greater-than `>` preserves the *first* occurrence index.
4. Tests (P4) propose tests for single-element list `[5]`, multiple occurrences `[10, 20, 20]`, negative values `[-5, -2, -10]`, and empty list.
