# Test Case: CB-T05

- **Test ID:** CB-T05
- **Type:** Normal
- **Source Language:** Python
- **Target Language:** C++
- **Description:** In-place or two-pointer string reversal preserving whitespace and case

## Source Code

```python
def reverse_string(s: str) -> str:
    """Reverse a string character by character while preserving whitespace and symbols.
    Empty string returns an empty string.
    """
    if not s:
        return ""
    
    chars = list(s)
    left = 0
    right = len(chars) - 1
    
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
        
    return "".join(chars)


if __name__ == "__main__":
    original = "CodeBridge 2026!"
    print("Original:", original)
    print("Reversed:", reverse_string(original))
```

## Expected Behaviour (Pre-defined)

1. Static analysis (P1) identifies two-pointer swapping algorithm, boundary checks `left < right`, string immutability in Python being worked around by converting to `list(s)`.
2. Translation (P2) translates to C++:
   - Takes `std::string` or `const std::string&` and returns `std::string`.
   - In C++, strings are mutable, so either in-place `std::swap(s[left], s[right])` or `std::reverse(s.begin(), s.end())` can be used.
   - Preserves 0-based indexing and pointer increment/decrement.
3. Review (P3) checks UTF-8 multi-byte considerations (ASCII/single-byte assumption noted) and confirms edge case of empty string.
4. Tests (P4) propose tests for empty string `""`, single character `"A"`, palindrome `"racecar"`, and strings with punctuation and spaces.
