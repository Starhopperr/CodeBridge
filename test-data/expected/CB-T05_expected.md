# Expected Result Specification: CB-T05

## Metadata
- **Test ID:** CB-T05
- **Case Type:** Normal
- **Source Language:** Python
- **Target Language:** C++
- **Target Component:** Two-pointer string reversal

---

## 1. P1 Static Analysis Expectations
- **Functions:** `reverse_string(s: str) -> str`.
- **Inputs & Outputs:** Input: string `s`; Output: reversed string.
- **Control Flow:** Early return on empty string. While-loop with two indices converging (`left < right`). In-place character swap.
- **Language Semantics to Preserve:** String character indexing and preservation of all ASCII characters, whitespace, and punctuation.
- **Edge Cases:** Empty string `""`, single-character string `"a"`, even-length string `"abcd"`, odd-length string `"abc"`.

---

## 2. P2 Translation Expectations
- Target function: `std::string reverse_string(std::string s)` or taking `const std::string& s`.
- Efficient string manipulation using mutable `std::string`:
  ```cpp
  #include <string>
  #include <utility>

  std::string reverse_string(std::string s) {
      if (s.empty()) return "";
      int left = 0;
      int right = static_cast<int>(s.length()) - 1;
      while (left < right) {
          std::swap(s[left], s[right]);
          left++;
          right--;
      }
      return s;
  }
  ```
- Alternatively standard `std::reverse(s.begin(), s.end())` with explanation.

---

## 3. P3 Review Expectations
- Assessment: `PASS`.
- Verifies 0-based indices and signed/unsigned index conversion safety (`s.length()` returns `size_t`).
- Notes potential UTF-8 multi-byte caveat if non-ASCII Unicode characters are passed.

---

## 4. P4 Test Proposals Expectations
- Proposed Test 1: `s = ""` → `""` (Empty string).
- Proposed Test 2: `s = "Z"` → `"Z"` (Single character).
- Proposed Test 3: `s = "hello"` → `"olleh"` (Normal odd).
- Proposed Test 4: `s = "CodeBridge 2026!"` → `"!6202 egdirBedoC"` (Spaces and punctuation).
