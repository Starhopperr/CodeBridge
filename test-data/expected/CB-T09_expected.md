# Expected Result Specification: CB-T09

## Metadata
- **Test ID:** CB-T09
- **Case Type:** Edge
- **Source Language:** Python
- **Target Language:** Java
- **Target Component:** Integer division semantics

---

## 1. P1 Static Analysis Expectations
- **Functions:** `compute_page_count(total_items: int, items_per_page: int) -> int`.
- **Inputs & Outputs:** Inputs: two integers; Output: integer page count.
- **Control Flow:** Argument validation (`total_items < 0 or items_per_page <= 0`). Integer floor division `//` and remainder `%`. Conditional page increment if remainder exists.
- **Language Semantics to Preserve:** 
  - `total_items // items_per_page` must evaluate using integer arithmetic, not floating point.
  - In Python, `7 // 2` is `3`. In Java, integer division `7 / 2` is also `3`.
  - Must NOT cast to `double` or `float` prior to division without explicit rounding.
- **Edge Cases:** `total_items = 0`, exact multiples (`6` and `2`), non-exact multiples (`7` and `2`), `items_per_page = 0`.

---

## 2. P2 Translation Expectations
- Java method: `public static int computePageCount(int totalItems, int itemsPerPage)`.
- Input validation:
  ```java
  if (totalItems < 0 || itemsPerPage <= 0) {
      throw new IllegalArgumentException("total_items >= 0 and items_per_page > 0 required");
  }
  int fullPages = totalItems / itemsPerPage; // integer division preserved
  int remainder = totalItems % itemsPerPage;
  if (remainder > 0) {
      return fullPages + 1;
  }
  return fullPages;
  ```
- Must not introduce `(double) totalItems / itemsPerPage`.

---

## 3. P3 Review Expectations
- Assessment: `PASS`.
- Explicit verification: confirms integer types were used so `7 / 2` yields `3` and not `3.5`.
- Confirms division-by-zero guard `itemsPerPage <= 0`.

---

## 4. P4 Test Proposals Expectations
- Proposed Test 1: `(7, 2)` → `4` (Odd items, requires +1 page).
- Proposed Test 2: `(6, 2)` → `3` (Exact multiple, no +1).
- Proposed Test 3: `(0, 5)` → `0` (Zero items).
- Proposed Test 4: `(5, 0)` → `IllegalArgumentException` (Division by zero / invalid parameter).
