# Test Case: CB-T09

- **Test ID:** CB-T09
- **Type:** Edge
- **Source Language:** Python
- **Target Language:** Java
- **Description:** Integer floor division semantics (e.g. 7 // 2 = 3 vs float division)

## Source Code

```python
def compute_page_count(total_items: int, items_per_page: int) -> int:
    """Calculate the number of pages required to display total_items,
    using floor division and remainder. Both inputs must be positive integers.
    """
    if total_items < 0 or items_per_page <= 0:
        raise ValueError("total_items >= 0 and items_per_page > 0 required")
    
    full_pages = total_items // items_per_page
    remainder = total_items % items_per_page
    
    if remainder > 0:
        return full_pages + 1
    return full_pages


if __name__ == "__main__":
    print("7 items, 2 per page:", compute_page_count(7, 2))  # expected 4
    print("6 items, 2 per page:", compute_page_count(6, 2))  # expected 3
    print("0 items, 5 per page:", compute_page_count(0, 5))  # expected 0
```

## Expected Behaviour (Pre-defined)

1. Static analysis (P1) explicitly highlights Python `//` floor division returning integer:
   - For positive numbers, Java `int / int` also truncates towards zero (matching floor division for positives).
   - Warning/note on negative floor division differences (Python `-7 // 2 = -4`, Java `-7 / 2 = -3`).
2. Translation (P2) must ensure integer types are used in Java (`int fullPages = totalItems / itemsPerPage;`).
   - Must NOT use floating-point division (`double`) which would yield `3.5`.
   - Must throw `IllegalArgumentException` for invalid arguments.
3. Review (P3) verifies that integer division semantics are preserved and that no floating point conversions were introduced.
4. Tests (P4) propose tests for `7 // 2`, `6 // 2`, `0 // 5`, and invalid inputs.
