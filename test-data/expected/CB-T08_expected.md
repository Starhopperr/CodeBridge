# Expected Result Specification: CB-T08

## Metadata
- **Test ID:** CB-T08
- **Case Type:** Edge
- **Source Language:** Python
- **Target Language:** C++
- **Target Component:** Zero and negative boundary clamping

---

## 1. P1 Static Analysis Expectations
- **Functions:** `classify_and_clamp(val: int, lower: int, upper: int) -> dict[str, int | str]`.
- **Inputs & Outputs:** Inputs: three integers; Output: heterogeneous dictionary `{clamped: int, sign: str}`.
- **Control Flow:** Argument validation guard (`lower > upper` throws `ValueError`), clamping computation (`max(lower, min(val, upper))`), three-way sign check (`> 0`, `< 0`, `== 0`).
- **Language Semantics to Preserve:** Python dynamic typing in return dictionary requires mapping to a static C++ structure.
- **Edge Cases:** `val == 0`, negative bounds, `lower == upper`, `val == lower`, `val == upper`, `lower > upper`.

---

## 2. P2 Translation Expectations
- Return representation: Custom `struct ClampResult { int clamped; std::string sign; };` or `std::pair<int, std::string>`.
- Exception: throws `std::invalid_argument` for `lower > upper`.
- Clamping and sign check:
  ```cpp
  #include <string>
  #include <stdexcept>
  #include <algorithm>

  struct ClampResult {
      int clamped;
      std::string sign;
  };

  ClampResult classify_and_clamp(int val, int lower, int upper) {
      if (lower > upper) {
          throw std::invalid_argument("lower bound cannot exceed upper bound");
      }
      int clamped = std::max(lower, std::min(val, upper));
      std::string sign;
      if (clamped > 0) sign = "positive";
      else if (clamped < 0) sign = "negative";
      else sign = "zero";
      return ClampResult{clamped, sign};
  }
  ```

---

## 3. P3 Review Expectations
- Assessment: `PASS` or `PASS_WITH_RISKS`.
- Reviews whether exception throwing in C++ matches Python `ValueError`.
- Reviews boundary correctness when `clamped == 0`.

---

## 4. P4 Test Proposals Expectations
- Proposed Test 1: `(0, -10, 10)` → `{clamped: 0, sign: "zero"}` (Boundary).
- Proposed Test 2: `(-15, -10, 10)` → `{clamped: -10, sign: "negative"}` (Clamp lower).
- Proposed Test 3: `(25, -10, 10)` → `{clamped: 10, sign: "positive"}` (Clamp upper).
- Proposed Test 4: `(5, 10, 0)` → `invalid_argument` (Invalid inputs).
