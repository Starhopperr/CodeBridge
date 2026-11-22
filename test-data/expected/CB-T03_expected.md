# Expected Result Specification: CB-T03

## Metadata
- **Test ID:** CB-T03
- **Case Type:** Normal
- **Source Language:** Python
- **Target Language:** C++
- **Target Component:** For-loop accumulator

---

## 1. P1 Static Analysis Expectations
- **Functions:** `sum_positive_numbers(numbers: list[int]) -> int`.
- **Inputs & Outputs:** List of integers; Output: single integer sum.
- **Control Flow:** Sequential iteration over collection elements; predicate filtering `num > 0`; variable accumulation.
- **Language Semantics to Preserve:** Empty collection returns 0. Strict inequality `> 0` excludes zeros.
- **Edge Cases:** Empty vector, vector with only negative numbers, vector with all zeros.

---

## 2. P2 Translation Expectations
- Function signature: `int sum_positive_numbers(const std::vector<int>& numbers)`.
- Loop iteration using modern C++ idiom:
  ```cpp
  int total = 0;
  for (int num : numbers) {
      if (num > 0) {
          total += num;
      }
  }
  return total;
  ```
- Appropriate headers included: `<vector>`.

---

## 3. P3 Review Expectations
- Assessment: `PASS` or `PASS_WITH_RISKS` (evaluating potential integer overflow if sum exceeds `INT_MAX`).
- Confirms vector is passed by const reference (`const std::vector<int>&`) to prevent needless copying.

---

## 4. P4 Test Proposals Expectations
- Proposed Test 1: `numbers = {}` → `0` (Empty).
- Proposed Test 2: `numbers = {-5, -1, 0}` → `0` (Boundary).
- Proposed Test 3: `numbers = [-3, 10, 0, 4, -1, 5]` → `19` (Normal).
