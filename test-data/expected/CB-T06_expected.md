# Expected Result Specification: CB-T06

## Metadata
- **Test ID:** CB-T06
- **Case Type:** Normal
- **Source Language:** Python
- **Target Language:** Java
- **Target Component:** Dictionary word frequency counter

---

## 1. P1 Static Analysis Expectations
- **Functions:** `count_word_frequencies(words: list[str]) -> dict[str, int]`.
- **Inputs & Outputs:** Input: list of strings; Output: dictionary mapping string to integer count.
- **Control Flow:** For loop over items. String whitespace stripping and lowercase normalisation. Skip condition for empty normalized tokens. Key existence check and counter increment.
- **Language Semantics to Preserve:** Case-insensitivity through lowercase folding. Whitespace stripping equivalent to `.strip()`.

---

## 2. P2 Translation Expectations
- Return type: `Map<String, Integer>`.
- Java idiom:
  ```java
  import java.util.HashMap;
  import java.util.List;
  import java.util.Map;

  public static Map<String, Integer> countWordFrequencies(List<String> words) {
      Map<String, Integer> counts = new HashMap<>();
      if (words == null) return counts;
      for (String word : words) {
          if (word == null) continue;
          String normalized = word.trim().toLowerCase();
          if (normalized.isEmpty()) continue;
          counts.put(normalized, counts.getOrDefault(normalized, 0) + 1);
      }
      return counts;
  }
  ```

---

## 3. P3 Review Expectations
- Assessment: `PASS` or `PASS_WITH_RISKS`.
- Verifies null safety: what happens if `words` list contains `null` or if `words` itself is null.
- Identifies `trim()` matching `strip()`.

---

## 4. P4 Test Proposals Expectations
- Proposed Test 1: `words = []` → `{}` (Empty list).
- Proposed Test 2: `words = ["  ", ""]` → `{}` (Whitespace tokens skipped).
- Proposed Test 3: `words = ["Apple", "apple", "APPLE"]` → `{"apple": 3}` (Case insensitivity).
