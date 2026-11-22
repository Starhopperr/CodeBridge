# Expected Result Specification: CB-T02

## Metadata
- **Test ID:** CB-T02
- **Case Type:** Normal
- **Source Language:** Python
- **Target Language:** Java
- **Target Component:** FizzBuzz string generator

---

## 1. P1 Static Analysis Expectations
- **Functions:** `fizzbuzz(limit: int) -> list[str]`.
- **Inputs & Outputs:** Parameter `limit` (integer); Output: `list` of strings.
- **Control Flow:** Boundary guard for `limit < 1` returning empty list. For-loop from 1 to `limit + 1`. Chained conditional ladder testing `% 15`, `% 3`, `% 5`, with fallback to string representation of number.
- **Language Semantics to Preserve:** 1-based inclusive range (`range(1, limit + 1)` translates to `<= limit`). Order of branch evaluation (15 must precede 3 and 5).
- **Edge Cases:** `limit <= 0` (returns empty list), `limit = 1` (returns `["1"]`).

---

## 2. P2 Translation Expectations
- Target Java method returning `List<String>`.
- Correct container initialization: `List<String> results = new ArrayList<>();`.
- Correct loop bounds: `for (int i = 1; i <= limit; i++)`.
- Conditional ladder:
  ```java
  if (i % 15 == 0) {
      results.add("FizzBuzz");
  } else if (i % 3 == 0) {
      results.add("Fizz");
  } else if (i % 5 == 0) {
      results.add("Buzz");
  } else {
      results.add(String.valueOf(i));
  }
  ```

---

## 3. P3 Review Expectations
- Assessment: `PASS`.
- Verifies that `i % 15 == 0` is checked before individual 3 and 5 checks.
- Confirms 1-based index boundary is preserved.

---

## 4. P4 Test Proposals Expectations
- Proposed Test 1: `limit = 0` → `[]` (Empty/Boundary).
- Proposed Test 2: `limit = 1` → `["1"]` (Boundary).
- Proposed Test 3: `limit = 3` → `["1", "2", "Fizz"]` (Normal).
- Proposed Test 4: `limit = 15` → ends with `"FizzBuzz"` (Normal).
