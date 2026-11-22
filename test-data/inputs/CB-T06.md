# Test Case: CB-T06

- **Test ID:** CB-T06
- **Type:** Normal
- **Source Language:** Python
- **Target Language:** Java
- **Description:** Dictionary word counter and frequency aggregator

## Source Code

```python
def count_word_frequencies(words: list[str]) -> dict[str, int]:
    """Count the frequency of each lowercase word in the input list.
    Empty list returns an empty dictionary. Words are normalized to lowercase.
    """
    counts = {}
    for word in words:
        normalized = word.strip().lower()
        if not normalized:
            continue
        if normalized in counts:
            counts[normalized] += 1
        else:
            counts[normalized] = 1
    return counts


if __name__ == "__main__":
    sample_words = ["Bridge", "code", "bridge", "CODE", "prompt", ""]
    print("Frequencies:", count_word_frequencies(sample_words))
```

## Expected Behaviour (Pre-defined)

1. Static analysis (P1) identifies:
   - Takes `list[str]` and returns `dict[str, int]`.
   - String normalisation via `.strip().lower()`.
   - Skips empty normalized strings.
   - Dictionary insertion and increment logic.
2. Translation (P2) translates to Java:
   - Returns `Map<String, Integer>` using `HashMap<String, Integer>`.
   - Uses `word.trim().toLowerCase()`.
   - Uses `counts.put(normalized, counts.getOrDefault(normalized, 0) + 1)` or `merge()`.
3. Review (P3) checks null handling in the word list and locale-dependency of `toLowerCase()` (e.g. `toLowerCase(Locale.ROOT)`).
4. Tests (P4) propose tests for empty list `[]`, list with whitespace-only strings `["  ", ""]`, duplicate words with differing cases `["Test", "test"]`.
