"""
schemas.py — Pydantic v2 request/response models for CodeBridge.
Exactly aligned with 05_PROMPT_LIBRARY_SPEC.md and frontend/src/types.ts.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Request
# ---------------------------------------------------------------------------

class TranslateRequest(BaseModel):
    source_code: str
    source_language: str
    target_language: str
    user_context: str = ""


# ---------------------------------------------------------------------------
# P1 — Static Analysis
# ---------------------------------------------------------------------------

class P1Analysis(BaseModel):
    program_summary: str = ""
    functions: List[str] = Field(default_factory=list)
    inputs_and_outputs: str = ""
    control_flow: str = ""
    data_structures: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    language_semantics_to_preserve: List[str] = Field(default_factory=list)
    edge_cases: List[str] = Field(default_factory=list)
    unsupported_or_ambiguous: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    confidence_notes: str = ""
    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# P2 — Translation
# ---------------------------------------------------------------------------

class P2Translation(BaseModel):
    translated_code: str = ""
    target_language: str = ""
    language_differences: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    potential_issues: List[str] = Field(default_factory=list)
    unsupported_features: List[str] = Field(default_factory=list)
    manual_verification_required: bool = True
    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# P3 — Review
# ---------------------------------------------------------------------------

class Finding(BaseModel):
    severity: str = "INFO"  # HIGH | MEDIUM | LOW | INFO
    location: str = ""
    explanation: str = ""
    correction: str = ""
    model_config = {"extra": "allow"}


class P3Review(BaseModel):
    overall_assessment: str = ""
    findings: List[Finding] = Field(default_factory=list)
    behavioural_differences: List[str] = Field(default_factory=list)
    unverified_assumptions: List[str] = Field(default_factory=list)
    recommended_tests: List[str] = Field(default_factory=list)
    human_review_required: bool = True
    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# P4 — Tests
# ---------------------------------------------------------------------------

class TestCase(BaseModel):
    test_id: str = ""
    purpose: str = ""
    input: str = ""
    expected_output: str = ""
    expected_output_confidence: str = ""  # high | medium | low | human-confirmation-required
    case_type: str = ""                  # normal | boundary | empty | algorithm-specific
    risk_target: str = ""
    model_config = {"extra": "allow"}


class P4Tests(BaseModel):
    test_cases: List[TestCase] = Field(default_factory=list)
    execution_notes: str = ""
    tests_requiring_human_oracle: List[str] = Field(default_factory=list)
    model_config = {"extra": "allow"}


# ---------------------------------------------------------------------------
# Top-level response
# ---------------------------------------------------------------------------

class TranslateResponse(BaseModel):
    p1_analysis: Optional[P1Analysis] = None
    p2_translation: Optional[P2Translation] = None
    p3_review: Optional[P3Review] = None
    p4_tests: Optional[P4Tests] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    errors: Dict[str, str] = Field(default_factory=dict)
    model_config = {"extra": "allow"}
