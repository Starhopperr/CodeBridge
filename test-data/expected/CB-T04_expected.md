# Expected Result Specification: CB-T04

## Metadata
- **Test ID:** CB-T04
- **Case Type:** Normal
- **Source Language:** Python
- **Target Language:** Java
- **Target Component:** List max finder returning value and index

---

## 1. P1 Static Analysis Expectations
- **Functions:** `find_max_element(items: list[int]) -> tuple[int, int]`.
- **Inputs & Outputs:** List of integers; Output: 2-tuple `(max_value, max_index)`.
- **Control Flow:** Guard clause checking empty list and throwing `ValueError`. Linear traversal tracking both current max and its index.
- **Language Semantics to Preserve:** Python multiple return / tuple structure. In the event of duplicate maximums, strict `>` retains the index of the first occurrence.
- **Edge Cases:** Single-element list, list with negative numbers, list with duplicate maximums.

---

## 2. P2 Translation Expectations
- Java does not provide native pairs/tuples in standard library; expected representation is either:
  - Custom Java record or static class: `public record MaxResult(int value, int index) {}`
  - Or an `int[]` array of size 2.
- Exception handling: `if (items == null || items.isEmpty()) throw new IllegalArgumentException(...)`.
- Preserves first occurrence semantics (`items.get(idx) > maxVal`).

---

## 3. P3 Review Expectations
- Assessment: `PASS` or `PASS_WITH_RISKS`.
- Validates the tuple replacement pattern used in Java.
- Confirms empty collection guard prevents index out of bounds on `items.get(0)`.

---

## 4. P4 Test Proposals Expectations
- Proposed Test 1: `items = [42]` → `(42, 0)` (Boundary).
- Proposed Test 2: `items = [10, 50, 50, 20]` → `(50, 1)` (Duplicate max - first occurrence).
- Proposed Test 3: `items = [-10, -5, -20]` → `(-5, 1)` (All negatives).
- Proposed Test 4: `items = []` → `IllegalArgumentException` (Exception check).
