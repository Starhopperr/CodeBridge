# Expected Result Specification: CB-T01

## Metadata
- **Test ID:** CB-T01
- **Case Type:** Normal
- **Source Language:** Python
- **Target Language:** Java
- **Target Component:** Recursive factorial

---

## 1. P1 Static Analysis Expectations
- **Functions:** Identify `factorial(n: int) -> int`.
- **Inputs & Outputs:** Input `n` (non-negative integer); Output: integer factorial.
- **Control Flow:** Validation guard (`n < 0` throws `ValueError`), base cases (`n == 0 or n == 1` returns 1), recursive call `n * factorial(n - 1)`.
- **Language Semantics to Preserve:** Python integers have arbitrary precision; Java standard `int` overflows at `13!`, `long` at `21!`. Model should note this numeric capacity difference.
- **Edge Cases:** `n = 0`, `n = 1`, negative values (`n < 0`).
- **Confidence:** High.

---

## 2. P2 Translation Expectations
- Target class with static method: e.g. `public static long factorial(int n)`.
- Explicit argument validation:
  ```java
  if (n < 0) {
      throw new IllegalArgumentException("Factorial is not defined for negative numbers");
  }
  if (n == 0 || n == 1) {
      return 1L;
  }
  return n * factorial(n - 1);
  ```
- Stated assumptions: Selection of `long` or `BigInteger` for return type to mitigate overflow.

---

## 3. P3 Review Expectations
- Assessment: `PASS` or `PASS_WITH_RISKS` (if integer overflow without `BigInteger` is flagged as a risk).
- Verification of exception conversion from `ValueError` to `IllegalArgumentException`.
- Verification of base case completeness.

---

## 4. P4 Test Proposals Expectations
- Proposed Test 1: `input: 0` → `expected: 1` (Boundary).
- Proposed Test 2: `input: 1` → `expected: 1` (Boundary).
- Proposed Test 3: `input: 5` → `expected: 120` (Normal).
- Proposed Test 4: `input: -1` → `expected: IllegalArgumentException` (Edge/Exception).
