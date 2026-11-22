# Expected Result Specification: CB-T07

## Metadata
- **Test ID:** CB-T07
- **Case Type:** Edge
- **Source Language:** Python
- **Target Language:** Java
- **Target Component:** Empty list and None input handling

---

## 1. P1 Static Analysis Expectations
- **Functions:** `compute_average(values: list[float] | None) -> float`.
- **Inputs & Outputs:** Parameter `values` is an optional list of floats; Output: `float`.
- **Control Flow:** `if not values:` returns `0.0`.
- **Language Semantics to Preserve:** In Python, `not values` is true for BOTH `None` and an empty list `[]`. In Java, these are separate checks (`values == null || values.isEmpty()`).
- **Edge Cases:** `values = None`, `values = []`, division by zero if unguarded.

---

## 2. P2 Translation Expectations
- Java signature: `public static double computeAverage(List<Double> values)`.
- Explicit null and empty guard:
  ```java
  if (values == null || values.isEmpty()) {
      return 0.0;
  }
  double total = 0.0;
  for (Double v : values) {
      if (v != null) {
          total += v;
      }
  }
  return total / values.size();
  ```
- Stated assumption: whether elements inside the list could themselves be `null`.

---

## 3. P3 Review Expectations
- Assessment: `PASS` if both `null` and `.isEmpty()` are guarded; `FAIL` or `risk` if only one is checked.
- Explicit verification that `values.size() == 0` cannot cause `NaN` or `ArithmeticException`.

---

## 4. P4 Test Proposals Expectations
- Proposed Test 1: `values = null` → `0.0` (Edge / Null check).
- Proposed Test 2: `values = []` → `0.0` (Edge / Empty collection).
- Proposed Test 3: `values = [10.0, 20.0]` → `15.0` (Normal average).
