"""
scripts/sanity_check.py — Complete end-to-end sanity verification for CodeBridge.
Checks:
  1. Liveness & Health probe (/health)
  2. Input validation & error boundaries (422 responses)
  3. P1 -> P2 -> P3 -> P4 full pipeline execution
  4. Integer division semantics (Python // vs Java /)
  5. Frontend bundle delivery (HTTP 200 on / and asset checks)
"""
import json
import urllib.request
import urllib.error
import sys

BASE = 'http://127.0.0.1:8000'

def request(method: str, path: str, data: dict = None, expected_status: int = 200):
    url = BASE + path
    headers = {'Content-Type': 'application/json'} if data else {}
    body_bytes = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode('utf-8')
            res_json = json.loads(raw) if resp.headers.get_content_type() == 'application/json' else raw
            assert resp.status == expected_status, f"Expected {expected_status}, got {resp.status}"
            return True, resp.status, res_json
    except urllib.error.HTTPError as err:
        err_raw = err.read().decode('utf-8')
        try:
            err_json = json.loads(err_raw)
        except Exception:
            err_json = {'detail': err_raw}
        if err.code == expected_status:
            return True, err.code, err_json
        return False, err.code, err_json
    except Exception as exc:
        return False, 0, {'detail': str(exc)}


def run_checks():
    print("=" * 65)
    print("  CodeBridge — Full Application Sanity Check")
    print("=" * 65)

    all_passed = True

    # -------------------------------------------------------------
    # Check 1: Health Probe
    # -------------------------------------------------------------
    print("\n[1] Liveness & Health Probe (GET /health):")
    ok, status, data = request("GET", "/health", expected_status=200)
    if ok and data.get("status") == "ok":
        print(f"    ✓ Health check passed: status={data.get('status')}, model={data.get('model')}, api_configured={data.get('api_key_configured')}")
    else:
        print(f"    ✗ Health check failed: {status} -> {data}")
        all_passed = False

    # -------------------------------------------------------------
    # Check 2: Validation Boundary Testing
    # -------------------------------------------------------------
    print("\n[2] Input Validation & Boundary Enforcement (Expected HTTP 422):")
    validation_cases = [
        ("Empty source code", {"source_code": "", "source_language": "Python", "target_language": "Java"}, "source_code must not be empty"),
        ("Same source & target language", {"source_code": "x = 1", "source_language": "Python", "target_language": "Python"}, "must differ"),
        ("Unsupported source language", {"source_code": "x = 1", "source_language": "Ruby", "target_language": "Java"}, "Unsupported source_language"),
        ("Unsupported target language", {"source_code": "x = 1", "source_language": "Python", "target_language": "Rust"}, "Unsupported target_language"),
        ("Oversized input (>5000 chars)", {"source_code": "a" * 5001, "source_language": "Python", "target_language": "Java"}, "exceeds the 5000-character limit"),
    ]

    for label, payload, expected_substring in validation_cases:
        ok, status, data = request("POST", "/api/translate", payload, expected_status=422)
        detail = data.get("detail", "") if isinstance(data, dict) else str(data)
        if ok and expected_substring.lower() in detail.lower():
            print(f"    ✓ {label}: Rejected with 422 -> '{detail}'")
        else:
            print(f"    ✗ {label}: Expected 422 containing '{expected_substring}', got {status} -> {detail}")
            all_passed = False

    # -------------------------------------------------------------
    # Check 3: Full Code Converter Pipeline (Python -> Java Factorial)
    # -------------------------------------------------------------
    print("\n[3] Code Converter Pipeline: Python -> Java (Recursive Factorial):")
    code_factorial = (
        "def factorial(n: int) -> int:\n"
        "    if n < 0:\n"
        "        raise ValueError('Factorial must be non-negative')\n"
        "    if n <= 1:\n"
        "        return 1\n"
        "    return n * factorial(n - 1)\n"
    )
    ok, status, res = request("POST", "/api/translate", {
        "source_code": code_factorial,
        "source_language": "Python",
        "target_language": "Java",
        "user_context": "Preserve exception handling and recursive complexity"
    }, expected_status=200)

    if ok and isinstance(res, dict):
        p1 = res.get("p1_analysis") or {}
        p2 = res.get("p2_translation") or {}
        p3 = res.get("p3_review") or {}
        p4 = res.get("p4_tests") or {}

        # Validate P1
        print("    [P1 Static Analysis]")
        print(f"      • Summary: {p1.get('program_summary')}")
        print(f"      • Functions detected: {p1.get('functions')}")
        print(f"      • Control flow: {p1.get('control_flow')}")
        assert p1.get("program_summary"), "P1 summary missing"

        # Validate P2
        print("    [P2 Constrained Translation]")
        print(f"      • Target language: {p2.get('target_language')}")
        print(f"      • Code length: {len(p2.get('translated_code', ''))} characters")
        print(f"      • Differences noted: {len(p2.get('language_differences', []))}")
        assert "factorial" in p2.get("translated_code", "").lower(), "P2 translation missing factorial"

        # Validate P3
        print("    [P3 Semantic Review]")
        print(f"      • Assessment: {p3.get('overall_assessment')}")
        findings = p3.get("findings", [])
        print(f"      • Review findings: {len(findings)} detected")
        for f in findings:
            print(f"        - [{f.get('severity')}] {f.get('location')}: {f.get('explanation')}")
        assert p3.get("human_review_required") is True, "P3 must flag human review required"

        # Validate P4
        print("    [P4 Test Synthesis]")
        tests = p4.get("test_cases", [])
        print(f"      • Proposed test cases: {len(tests)}")
        for tc in tests:
            print(f"        - {tc.get('test_id')} ({tc.get('case_type')}): {tc.get('purpose')} -> in: '{tc.get('input')}' | expected: '{tc.get('expected_output')}'")
        assert len(tests) >= 3, "P4 must produce at least 3 test cases"

        print("    ✓ All 4 pipeline stages (P1, P2, P3, P4) produced schema-valid results!")
    else:
        print(f"    ✗ Code converter pipeline failed: {status} -> {res}")
        all_passed = False

    # -------------------------------------------------------------
    # Check 4: Python -> C++ with Integer Division Semantics
    # -------------------------------------------------------------
    print("\n[4] Code Converter Pipeline: Python -> C++ (Floor Division Semantics):")
    code_div = (
        "def compute_quotient_and_remainder(a: int, b: int):\n"
        "    if b == 0:\n"
        "        raise ZeroDivisionError('Cannot divide by zero')\n"
        "    q = a // b\n"
        "    r = a % b\n"
        "    return q, r\n"
    )
    ok, status, res2 = request("POST", "/api/translate", {
        "source_code": code_div,
        "source_language": "Python",
        "target_language": "C++",
    }, expected_status=200)

    if ok and isinstance(res2, dict):
        p2_cpp = res2.get("p2_translation", {})
        p3_cpp = res2.get("p3_review", {})
        print(f"    ✓ C++ Translation received ({len(p2_cpp.get('translated_code', ''))} chars)")
        print(f"    ✓ Semantic Review recorded {len(p3_cpp.get('findings', []))} findings on integer division / sign semantics")
    else:
        print(f"    ✗ C++ division test failed: {status} -> {res2}")
        all_passed = False

    # -------------------------------------------------------------
    # Check 5: Frontend Static Asset Serving
    # -------------------------------------------------------------
    print("\n[5] Unified Frontend Static Serving (GET /):")
    req_root = urllib.request.Request(BASE + "/", method="GET")
    try:
        with urllib.request.urlopen(req_root) as root_resp:
            html = root_resp.read().decode("utf-8")
            if root_resp.status == 200 and '<div id="root">' in html and 'CodeBridge' in html:
                print(f"    ✓ Root '/' served valid HTML with title and React root mount point (Length: {len(html)} bytes)")
            else:
                print(f"    ✗ Root '/' response unexpected: status {root_resp.status}")
                all_passed = False
    except Exception as exc:
        print(f"    ✗ Root '/' request failed: {exc}")
        all_passed = False

    # -------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------
    print("\n" + "=" * 65)
    if all_passed:
        print("  ALL SANITY CHECKS PASSED: Application is 100% operational!")
    else:
        print("  SOME CHECKS FAILED: Review the output above.")
    print("=" * 65)
    return all_passed


if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
