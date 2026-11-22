export interface TranslateRequest {
  source_code: string;
  source_language: string;
  target_language: string;
  user_context?: string;
}

export interface Finding {
  severity: string;
  location: string;
  explanation: string;
  correction: string;
}

export interface TestCase {
  test_id: string;
  purpose: string;
  input: string;
  expected_output: string;
  expected_output_confidence: string;
  case_type: string;
  risk_target: string;
}

export interface P1Analysis {
  program_summary: string;
  functions?: string[];
  inputs_and_outputs?: string;
  control_flow?: string;
  data_structures?: string[];
  dependencies?: string[];
  language_semantics_to_preserve?: string[];
  edge_cases?: string[];
  unsupported_or_ambiguous?: string[];
  assumptions?: string[];
  confidence_notes?: string;
}

export interface P2Translation {
  translated_code: string;
  target_language: string;
  language_differences?: string[];
  assumptions?: string[];
  potential_issues?: string[];
  unsupported_features?: string[];
  manual_verification_required?: boolean;
}

export interface P3Review {
  overall_assessment: string;
  findings?: Finding[];
  behavioural_differences?: string[];
  unverified_assumptions?: string[];
  recommended_tests?: string[];
  human_review_required?: boolean;
}

export interface P4Tests {
  test_cases?: TestCase[];
  execution_notes?: string;
  tests_requiring_human_oracle?: string[];
}

export interface TranslateResponse {
  p1_analysis?: P1Analysis;
  p2_translation?: P2Translation;
  p3_review?: P3Review;
  p4_tests?: P4Tests;
  metadata?: {
    model_id: string;
    timestamp: string;
    source_language: string;
    target_language: string;
  };
  errors?: Record<string, string>;
}
