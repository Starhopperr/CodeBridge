import React, { useState, useRef } from 'react';
import { translate } from './api';
import { TranslateResponse, Finding, TestCase } from './types';
import './App.css';

const LANGUAGES = ['Python', 'Java', 'C++'];

interface Sample {
  title: string;
  sourceLang: string;
  targetLang: string;
  code: string;
}

const SAMPLES: Sample[] = [
  {
    title: 'Python → Java: Floor Division (Semantics)',
    sourceLang: 'Python',
    targetLang: 'Java',
    code: `def calculate_quotient(a: int, b: int) -> int:
    """Python // performs floor division (rounds towards -infinity)."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a // b
`,
  },
  {
    title: 'Python → Java: Factorial (Recursion)',
    sourceLang: 'Python',
    targetLang: 'Java',
    code: `def factorial(n: int) -> int:
    """Calculate factorial recursively with validation."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return 1
    return n * factorial(n - 1)
`,
  },
  {
    title: 'Python → C++: Find Maximum',
    sourceLang: 'Python',
    targetLang: 'C++',
    code: `def find_max(numbers: list) -> int:
    max_val = numbers[0]
    for x in numbers:
        if x > max_val:
            max_val = x
    return max_val
`,
  },
  {
    title: 'C++ → Python: FizzBuzz',
    sourceLang: 'C++',
    targetLang: 'Python',
    code: `void fizzbuzz(int n) {
    for (int i = 1; i <= n; i++) {
        if (i % 15 == 0) {
            std::cout << "FizzBuzz" << std::endl;
        } else if (i % 3 == 0) {
            std::cout << "Fizz" << std::endl;
        } else if (i % 5 == 0) {
            std::cout << "Buzz" << std::endl;
        } else {
            std::cout << i << std::endl;
        }
    }
}
`,
  },
];

type RightTab = 'code' | 'p3' | 'p4' | 'p1';

export default function App() {
  const [sourceLang, setSourceLang] = useState('Python');
  const [targetLang, setTargetLang] = useState('Java');
  const [sourceCode, setSourceCode] = useState(SAMPLES[0].code);
  const [translatedCode, setTranslatedCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<RightTab>('code');
  const [splitView, setSplitView] = useState(false);
  const [result, setResult] = useState<TranslateResponse | null>(null);

  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleTranslate();
      return;
    }
    if (e.key === 'Tab') {
      e.preventDefault();
      const target = e.currentTarget;
      const start = target.selectionStart;
      const end = target.selectionEnd;
      const val = target.value;
      const nextVal = val.substring(0, start) + '    ' + val.substring(end);
      setSourceCode(nextVal);
      setTimeout(() => {
        target.selectionStart = target.selectionEnd = start + 4;
      }, 0);
    }
  };

  const handleSwap = () => {
    setSourceLang(targetLang);
    setTargetLang(sourceLang);
    if (translatedCode) {
      setSourceCode(translatedCode);
      setTranslatedCode('');
      setResult(null);
    }
  };

  const handleTranslate = async () => {
    setError(null);
    if (!sourceCode.trim()) {
      setError('Please provide code to translate.');
      return;
    }
    if (sourceLang === targetLang) {
      setError('Source and target languages must be different.');
      return;
    }

    setLoading(true);
    try {
      const res = await translate({
        source_code: sourceCode,
        source_language: sourceLang,
        target_language: targetLang,
      });
      setResult(res);
      const code = res.p2_translation?.translated_code || '';
      setTranslatedCode(code);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Translation request failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (!translatedCode) return;
    navigator.clipboard.writeText(translatedCode).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const handleDownload = () => {
    if (!translatedCode) return;
    const extMap: Record<string, string> = { Python: 'py', Java: 'java', 'C++': 'cpp' };
    const ext = extMap[targetLang] || 'txt';
    const filename = `Main.${ext}`;
    const blob = new Blob([translatedCode], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleLoadSample = (sample: Sample) => {
    setSourceLang(sample.sourceLang);
    setTargetLang(sample.targetLang);
    setSourceCode(sample.code);
    setTranslatedCode('');
    setResult(null);
    setError(null);
    setActiveTab('code');
  };

  const inputLines = sourceCode.split('\n').length;
  const outputLines = translatedCode ? translatedCode.split('\n').length : 0;
  const findingsCount = result?.p3_review?.findings?.length || 0;
  const testCount = result?.p4_tests?.test_cases?.length || 0;

  return (
    <div className="cb-shell">
      {/* ── Precision Navigation Bar ── */}
      <header className="cb-header">
        <div className="cb-brand">
          <div className="cb-logo" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="16 18 22 12 16 6" />
              <polyline points="8 6 2 12 8 18" />
            </svg>
          </div>
          <span className="cb-name">CodeBridge</span>
          <span className="cb-badge">Studio</span>
        </div>

        {/* Center Language Controls & Translate Button */}
        <div className="cb-actions">
          <div className="cb-lang-group">
            <select
              className="cb-select"
              value={sourceLang}
              onChange={(e) => setSourceLang(e.target.value)}
              disabled={loading}
              aria-label="Source Language"
            >
              {LANGUAGES.map((l) => (
                <option key={l} value={l}>
                  {l}
                </option>
              ))}
            </select>

            <button
              type="button"
              className="cb-swap-btn"
              onClick={handleSwap}
              title="Swap Languages"
              disabled={loading}
              aria-label="Swap languages"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="7 10 12 5 17 10" />
                <polyline points="17 14 12 19 7 14" />
              </svg>
            </button>

            <select
              className="cb-select"
              value={targetLang}
              onChange={(e) => setTargetLang(e.target.value)}
              disabled={loading}
              aria-label="Target Language"
            >
              {LANGUAGES.map((l) => (
                <option key={l} value={l}>
                  {l}
                </option>
              ))}
            </select>
          </div>

          <button
            type="button"
            className={`cb-translate-btn ${loading ? 'is-loading' : ''}`}
            onClick={handleTranslate}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="cb-spinner" aria-hidden="true" />
                <span>Translating...</span>
              </>
            ) : (
              <>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                  <polygon points="5 3 19 12 5 21 5 3" />
                </svg>
                <span>Translate</span>
              </>
            )}
          </button>
        </div>

        {/* Right Samples & View Mode */}
        <div className="cb-header-right">
          <button
            type="button"
            className={`cb-split-toggle ${splitView ? 'is-active' : ''}`}
            onClick={() => setSplitView(!splitView)}
            title="Toggle Split View (Code + Insights)"
          >
            {splitView ? '⊟ Tab View' : '⊞ Split View'}
          </button>

          <select
            className="cb-sample-select"
            onChange={(e) => {
              const idx = parseInt(e.target.value, 10);
              if (!isNaN(idx) && SAMPLES[idx]) {
                handleLoadSample(SAMPLES[idx]);
              }
            }}
            defaultValue=""
            aria-label="Load sample snippet"
          >
            <option value="" disabled>
              Select Example...
            </option>
            {SAMPLES.map((s, idx) => (
              <option key={s.title} value={idx}>
                {s.title}
              </option>
            ))}
          </select>
        </div>
      </header>

      {/* ── Error Banner ── */}
      {error && (
        <div className="cb-error" role="alert">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <span className="cb-error-msg">{error}</span>
          <button className="cb-error-dismiss" onClick={() => setError(null)}>
            ✕
          </button>
        </div>
      )}

      {/* ── Focused 2-Pane Code Editor Studio ── */}
      <main className="cb-studio">
        {/* Box 1: Input Code Box */}
        <section className="cb-box cb-input-box">
          <div className="cb-box-header">
            <div className="cb-box-title">
              <span className="cb-dot cb-dot-input" />
              <span>Input ({sourceLang})</span>
            </div>
            <div className="cb-box-meta">
              <span className="cb-stat">{inputLines} lines</span>
              <span className="cb-stat-sep">•</span>
              <span className="cb-stat">{sourceCode.length} chars</span>
              <button
                type="button"
                className="cb-btn-secondary"
                onClick={() => {
                  setSourceCode('');
                  setTranslatedCode('');
                  setResult(null);
                  inputRef.current?.focus();
                }}
                title="Clear code"
              >
                Clear
              </button>
            </div>
          </div>

          <div className="cb-editor-wrapper">
            <textarea
              ref={inputRef}
              className="cb-textarea"
              value={sourceCode}
              onChange={(e) => setSourceCode(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={`// Write or paste ${sourceLang} code here...\n// Press Ctrl+Enter to translate`}
              spellCheck={false}
              autoCapitalize="off"
              autoComplete="off"
              aria-label="Input code"
            />
          </div>

          <div className="cb-box-footer">
            <span className="cb-hint">Tip: Press <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to translate instantly</span>
          </div>
        </section>

        {/* Box 2: Output Studio (Code + P3 Review + P4 Tests + P1 Analysis) */}
        <section className="cb-box cb-output-box">
          {/* Navigation Tabs for Right Pane */}
          <div className="cb-box-header cb-tabs-header">
            <div className="cb-tabs-nav">
              <button
                type="button"
                className={`cb-tab-btn ${activeTab === 'code' ? 'is-active' : ''}`}
                onClick={() => setActiveTab('code')}
              >
                <span className={`cb-dot ${translatedCode ? 'cb-dot-active' : 'cb-dot-idle'}`} />
                <span>Output Code ({targetLang})</span>
              </button>

              <button
                type="button"
                className={`cb-tab-btn ${activeTab === 'p3' ? 'is-active' : ''}`}
                onClick={() => setActiveTab('p3')}
              >
                <span>P3: Review</span>
                {findingsCount > 0 && (
                  <span className="cb-tab-badge cb-badge-review">{findingsCount}</span>
                )}
              </button>

              <button
                type="button"
                className={`cb-tab-btn ${activeTab === 'p4' ? 'is-active' : ''}`}
                onClick={() => setActiveTab('p4')}
              >
                <span>P4: Tests</span>
                {testCount > 0 && (
                  <span className="cb-tab-badge cb-badge-tests">{testCount}</span>
                )}
              </button>

              <button
                type="button"
                className={`cb-tab-btn ${activeTab === 'p1' ? 'is-active' : ''}`}
                onClick={() => setActiveTab('p1')}
              >
                <span>P1: Analysis</span>
              </button>
            </div>

            <div className="cb-box-meta">
              {translatedCode && activeTab === 'code' && (
                <>
                  <span className="cb-stat">{outputLines} lines</span>
                  <span className="cb-stat-sep">•</span>
                  <button
                    type="button"
                    className={`cb-btn-secondary ${copied ? 'cb-btn-copied' : ''}`}
                    onClick={handleCopy}
                    title="Copy code to clipboard"
                  >
                    {copied ? '✓ Copied' : 'Copy'}
                  </button>
                  <button
                    type="button"
                    className="cb-btn-secondary"
                    onClick={handleDownload}
                    title="Download translated file"
                  >
                    Download
                  </button>
                </>
              )}
            </div>
          </div>

          {/* Main Output / Insights Viewport */}
          <div className={`cb-viewport-container ${splitView ? 'is-split' : ''}`}>
            {/* View 1: Output Code */}
            {(activeTab === 'code' || splitView) && (
              <div className="cb-editor-wrapper cb-output-wrapper">
                {translatedCode ? (
                  <pre className="cb-code-pre">
                    <code>{translatedCode}</code>
                  </pre>
                ) : (
                  <div className="cb-empty-state">
                    <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                      <polyline points="14 2 14 8 20 8" />
                      <line x1="16" y1="13" x2="8" y2="13" />
                      <line x1="16" y1="17" x2="8" y2="17" />
                    </svg>
                    <p className="cb-empty-text">Translated {targetLang} code will appear here</p>
                    <span className="cb-empty-sub">Click "Translate" or press Ctrl+Enter</span>
                  </div>
                )}
              </div>
            )}

            {/* View 2: P3 Semantic Review & Findings */}
            {(activeTab === 'p3' || (splitView && activeTab !== 'code')) && (
              <div className="cb-panel-pane cb-p3-pane">
                {result?.p3_review ? (
                  <div className="cb-p3-content">
                    <div className="cb-verdict-card">
                      <div className="cb-verdict-badge">
                        <span className="cb-verdict-icon">🛡️</span>
                        <strong>Review Assessment:</strong>
                      </div>
                      <p className="cb-verdict-text">{result.p3_review.overall_assessment}</p>
                    </div>

                    {result.p2_translation?.language_differences && result.p2_translation.language_differences.length > 0 && (
                      <div className="cb-section-block">
                        <h4 className="cb-section-title">Key Language Semantic Differences</h4>
                        <ul className="cb-diff-list">
                          {result.p2_translation.language_differences.map((d, i) => (
                            <li key={i}>{d}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    <div className="cb-section-block">
                      <h4 className="cb-section-title">
                        Audited Findings & Divergence Risks ({result.p3_review.findings?.length || 0})
                      </h4>
                      {result.p3_review.findings && result.p3_review.findings.length > 0 ? (
                        <div className="cb-findings-grid">
                          {result.p3_review.findings.map((f: Finding, i: number) => (
                            <div key={i} className={`cb-finding-card sev-${f.severity.toLowerCase()}`}>
                              <div className="cb-finding-header">
                                <span className={`cb-sev-tag tag-${f.severity.toLowerCase()}`}>{f.severity}</span>
                                <span className="cb-finding-loc">{f.location}</span>
                              </div>
                              <p className="cb-finding-exp">{f.explanation}</p>
                              {f.correction && (
                                <div className="cb-finding-fix">
                                  <strong>Mitigation:</strong> {f.correction}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="cb-empty-sub">No semantic divergences or defect risks detected.</p>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="cb-empty-state">
                    <p className="cb-empty-text">P3 Review will execute alongside translation</p>
                    <span className="cb-empty-sub">Translate a code snippet to view semantic audits</span>
                  </div>
                )}
              </div>
            )}

            {/* View 3: P4 Test Cases */}
            {activeTab === 'p4' && !splitView && (
              <div className="cb-panel-pane cb-p4-pane">
                {result?.p4_tests?.test_cases && result.p4_tests.test_cases.length > 0 ? (
                  <div className="cb-p4-content">
                    <div className="cb-pane-intro">
                      <h4>P4: Synthesized Equivalence Test Suite</h4>
                      <p>Concrete test vectors designed to verify behavioral and semantic parity across runtimes.</p>
                    </div>
                    <div className="cb-table-wrapper">
                      <table className="cb-tests-table">
                        <thead>
                          <tr>
                            <th>Test ID</th>
                            <th>Type</th>
                            <th>Purpose</th>
                            <th>Input</th>
                            <th>Expected Output</th>
                            <th>Target Risk</th>
                          </tr>
                        </thead>
                        <tbody>
                          {result.p4_tests.test_cases.map((tc: TestCase, i: number) => (
                            <tr key={i}>
                              <td><code className="cb-cell-id">{tc.test_id}</code></td>
                              <td><span className={`cb-type-tag type-${tc.case_type.toLowerCase()}`}>{tc.case_type}</span></td>
                              <td>{tc.purpose}</td>
                              <td><code className="cb-cell-code">{tc.input}</code></td>
                              <td><code className="cb-cell-code cb-cell-expect">{tc.expected_output}</code></td>
                              <td><span className="cb-risk-text">{tc.risk_target}</span></td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                    {result.p4_tests.execution_notes && (
                      <div className="cb-execution-note">
                        <strong>Execution Notes:</strong> {result.p4_tests.execution_notes}
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="cb-empty-state">
                    <p className="cb-empty-text">P4 Test Cases will appear here after translation</p>
                    <span className="cb-empty-sub">Translate code to view generated test vectors</span>
                  </div>
                )}
              </div>
            )}

            {/* View 4: P1 Static Analysis */}
            {activeTab === 'p1' && !splitView && (
              <div className="cb-panel-pane cb-p1-pane">
                {result?.p1_analysis ? (
                  <div className="cb-p1-content">
                    <div className="cb-pane-intro">
                      <h4>P1: Static AST Semantic Analysis</h4>
                      <p>{result.p1_analysis.program_summary}</p>
                    </div>

                    <div className="cb-grid-2col">
                      <div className="cb-card-box">
                        <h5>Functions & Scope</h5>
                        <ul className="cb-clean-list">
                          {result.p1_analysis.functions?.map((fn, i) => (
                            <li key={i}><code>{fn}</code></li>
                          ))}
                        </ul>
                      </div>

                      <div className="cb-card-box">
                        <h5>Inferred I/O & Types</h5>
                        <p>{result.p1_analysis.inputs_and_outputs}</p>
                      </div>

                      <div className="cb-card-box">
                        <h5>Control Flow & Logic</h5>
                        <p>{result.p1_analysis.control_flow}</p>
                      </div>

                      <div className="cb-card-box">
                        <h5>Data Structures</h5>
                        <div className="cb-chip-group">
                          {result.p1_analysis.data_structures?.map((ds, i) => (
                            <span key={i} className="cb-ds-chip">{ds}</span>
                          ))}
                        </div>
                      </div>
                    </div>

                    {result.p1_analysis.assumptions && result.p1_analysis.assumptions.length > 0 && (
                      <div className="cb-section-block">
                        <h5 className="cb-subheading">Model Assumptions</h5>
                        <ul className="cb-diff-list">
                          {result.p1_analysis.assumptions.map((a, i) => (
                            <li key={i}>{a}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="cb-empty-state">
                    <p className="cb-empty-text">P1 Analysis will extract AST facts upon translation</p>
                    <span className="cb-empty-sub">Click "Translate" to inspect semantic decomposition</span>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Footer Bar */}
          <div className="cb-box-footer">
            <span className="cb-hint">
              {result?.metadata ? `Model: ${result.metadata.model_id} | Pipeline: 4 Steps (P1 → P2 → P3 → P4)` : `Target: ${targetLang}`}
            </span>
          </div>
        </section>
      </main>
    </div>
  );
}
