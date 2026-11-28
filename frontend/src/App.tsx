import React, { useState, useRef, useEffect } from 'react';
import { translate } from './api';
import { TranslateResponse, Finding, TestCase } from './types';
import './App.css';

const LANGUAGES = [
  { label: 'Python 🐍', val: 'Python' },
  { label: 'Java ☕', val: 'Java' },
  { label: 'C++ ⚡', val: 'C++' },
];

interface Sample {
  title: string;
  badge: string;
  sourceLang: string;
  targetLang: string;
  code: string;
}

const SAMPLES: Sample[] = [
  {
    title: 'Floor Division',
    badge: '🍰 Math Semantics',
    sourceLang: 'Python',
    targetLang: 'Java',
    code: `def calculate_quotient(a: int, b: int) -> int:
    """Python // performs floor division (rounds towards -infinity)."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a // b

print("Quotient:", calculate_quotient(7, -2))
`,
  },
  {
    title: 'Factorial Recursion',
    badge: '🪄 Recursion',
    sourceLang: 'Python',
    targetLang: 'Java',
    code: `def factorial(n: int) -> int:
    """Calculate factorial recursively with validation."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print("Factorial of 5:", factorial(5))
`,
  },
  {
    title: 'Find Maximum',
    badge: '⭐ Collections',
    sourceLang: 'Python',
    targetLang: 'C++',
    code: `def find_max(numbers: list) -> int:
    max_val = numbers[0]
    for x in numbers:
        if x > max_val:
            max_val = x
    return max_val

print("Max value:", find_max([3, 7, 2, 9, 5]))
`,
  },
  {
    title: 'FizzBuzz Loop',
    badge: '⚡ Classic',
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

int main() {
    fizzbuzz(15);
    return 0;
}
`,
  },
];

type RightTab = 'code' | 'p3' | 'p4' | 'p1';

export default function App() {
  const [theme, setTheme] = useState<'dark' | 'light'>(() => {
    return (localStorage.getItem('cb_theme') as 'dark' | 'light') || 'dark';
  });
  const [sourceLang, setSourceLang] = useState('Python');
  const [targetLang, setTargetLang] = useState('Java');
  const [sourceCode, setSourceCode] = useState(SAMPLES[0].code);
  const [translatedCode, setTranslatedCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successToast, setSuccessToast] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<RightTab>('code');
  const [splitView, setSplitView] = useState(false);
  const [result, setResult] = useState<TranslateResponse | null>(null);

  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    localStorage.setItem('cb_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

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
    setSuccessToast(null);
    if (!sourceCode.trim()) {
      setError('Please provide code to translate! ✨');
      return;
    }
    if (sourceLang === targetLang) {
      setError('Source and target languages must be different! 🌸');
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
      setSuccessToast(`✨ Yay! Translated into ${targetLang} with Main entry point!`);
      setTimeout(() => setSuccessToast(null), 4000);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Translation request failed. Please try again!');
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
    setSuccessToast(null);
    setActiveTab('code');
  };

  const inputLines = sourceCode.split('\n').length;
  const outputLines = translatedCode ? translatedCode.split('\n').length : 0;
  const findingsCount = result?.p3_review?.findings?.length || 0;
  const testCount = result?.p4_tests?.test_cases?.length || 0;

  return (
    <div className={`cb-shell theme-${theme}`}>
      {/* ── Friendly & Sweet Header ── */}
      <header className="cb-header">
        <div className="cb-brand">
          <div className="cb-logo-cute" aria-hidden="true">
            <span className="cb-logo-icon">🌉</span>
            <span className="cb-logo-sparkle">✨</span>
          </div>
          <div className="cb-brand-text">
            <span className="cb-name">CodeBridge</span>
            <span className="cb-badge-sweet">💖 Cute Companion</span>
          </div>
        </div>

        {/* Center Language Controls & Cute Translate Button */}
        <div className="cb-actions">
          <div className="cb-lang-capsule">
            <select
              className="cb-select-cute"
              value={sourceLang}
              onChange={(e) => setSourceLang(e.target.value)}
              disabled={loading}
              aria-label="Source Language"
            >
              {LANGUAGES.map((l) => (
                <option key={l.val} value={l.val}>
                  {l.label}
                </option>
              ))}
            </select>

            <button
              type="button"
              className="cb-swap-btn-cute"
              onClick={handleSwap}
              title="Swap Languages ✨"
              disabled={loading}
              aria-label="Swap languages"
            >
              ⇄
            </button>

            <select
              className="cb-select-cute"
              value={targetLang}
              onChange={(e) => setTargetLang(e.target.value)}
              disabled={loading}
              aria-label="Target Language"
            >
              {LANGUAGES.map((l) => (
                <option key={l.val} value={l.val}>
                  {l.label}
                </option>
              ))}
            </select>
          </div>

          <button
            type="button"
            className={`cb-translate-btn-cute ${loading ? 'is-loading' : ''}`}
            onClick={handleTranslate}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="cb-magic-spinner" aria-hidden="true">🪄</span>
                <span>Casting Magic...</span>
              </>
            ) : (
              <>
                <span className="cb-btn-sparkle">✨</span>
                <span>Translate Magic</span>
              </>
            )}
          </button>
        </div>

        {/* Right Quick Controls */}
        <div className="cb-header-right">
          <button
            type="button"
            className="cb-theme-toggle"
            onClick={toggleTheme}
            title={theme === 'dark' ? 'Switch to Sweet Pastel Light' : 'Switch to Dreamy Midnight Dark'}
          >
            {theme === 'dark' ? '🌸 Pastel' : '🌙 Midnight'}
          </button>

          <button
            type="button"
            className={`cb-split-toggle-cute ${splitView ? 'is-active' : ''}`}
            onClick={() => setSplitView(!splitView)}
            title="Toggle Split View (Code + Audits)"
          >
            {splitView ? '📑 Single Tab' : '✨ Split View'}
          </button>
        </div>
      </header>

      {/* ── Welcoming Hero / Quick-Pick Ribbon ── */}
      <section className="cb-welcome-ribbon">
        <div className="cb-welcome-msg">
          <span className="cb-mascot-avatar">👋</span>
          <span>
            <strong>Hey there!</strong> Pick an example or paste your code below. We'll translate it safely with guaranteed <code>Main</code> entry points and full semantic audits! 💖
          </span>
        </div>
        <div className="cb-sample-pills">
          <span className="cb-pills-label">Quick Try:</span>
          {SAMPLES.map((s) => (
            <button
              key={s.title}
              type="button"
              className="cb-sample-pill-btn"
              onClick={() => handleLoadSample(s)}
            >
              {s.badge}
            </button>
          ))}
        </div>
      </section>

      {/* ── Toast / Feedback Alerts ── */}
      {successToast && (
        <div className="cb-toast cb-toast-success" role="status">
          <span>{successToast}</span>
          <button className="cb-toast-close" onClick={() => setSuccessToast(null)}>✕</button>
        </div>
      )}

      {error && (
        <div className="cb-toast cb-toast-error" role="alert">
          <span>🌸 {error}</span>
          <button className="cb-toast-close" onClick={() => setError(null)}>✕</button>
        </div>
      )}

      {/* ── Cute 2-Pane Editor Cards ── */}
      <main className="cb-studio">
        {/* Box 1: Input Code Card */}
        <section className="cb-box cb-input-box">
          <div className="cb-box-header">
            <div className="cb-box-title">
              <span className="cb-dot cb-dot-input" />
              <span>Input ({sourceLang})</span>
            </div>
            <div className="cb-box-meta">
              <span className="cb-pill-stat">{inputLines} lines</span>
              <span className="cb-pill-stat">{sourceCode.length} chars</span>
              <button
                type="button"
                className="cb-btn-ghost"
                onClick={() => {
                  setSourceCode('');
                  setTranslatedCode('');
                  setResult(null);
                  inputRef.current?.focus();
                }}
                title="Clear code"
              >
                ✨ Clear
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
              placeholder={`// 🌸 Write or paste your ${sourceLang} code here...\n// Press Ctrl + Enter to cast translation magic! ✨`}
              spellCheck={false}
              autoCapitalize="off"
              autoComplete="off"
              aria-label="Input code"
            />
          </div>

          <div className="cb-box-footer">
            <span className="cb-hint">
              💡 Tip: Press <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to translate instantly! 🪄
            </span>
          </div>
        </section>

        {/* Box 2: Output Card (Code + P3 Review + P4 Tests + P1 Analysis) */}
        <section className="cb-box cb-output-box">
          {/* Tabs Navigation */}
          <div className="cb-box-header cb-tabs-header">
            <div className="cb-tabs-nav">
              <button
                type="button"
                className={`cb-tab-btn-cute ${activeTab === 'code' ? 'is-active' : ''}`}
                onClick={() => setActiveTab('code')}
              >
                <span className={`cb-dot ${translatedCode ? 'cb-dot-active' : 'cb-dot-idle'}`} />
                <span>💻 Output Code ({targetLang})</span>
              </button>

              <button
                type="button"
                className={`cb-tab-btn-cute ${activeTab === 'p3' ? 'is-active' : ''}`}
                onClick={() => setActiveTab('p3')}
              >
                <span>🛡️ P3: Review</span>
                {findingsCount > 0 && (
                  <span className="cb-badge-count cb-badge-pink">{findingsCount}</span>
                )}
              </button>

              <button
                type="button"
                className={`cb-tab-btn-cute ${activeTab === 'p4' ? 'is-active' : ''}`}
                onClick={() => setActiveTab('p4')}
              >
                <span>🧪 P4: Tests</span>
                {testCount > 0 && (
                  <span className="cb-badge-count cb-badge-mint">{testCount}</span>
                )}
              </button>

              <button
                type="button"
                className={`cb-tab-btn-cute ${activeTab === 'p1' ? 'is-active' : ''}`}
                onClick={() => setActiveTab('p1')}
              >
                <span>🔍 P1: Analysis</span>
              </button>
            </div>

            <div className="cb-box-meta">
              {translatedCode && activeTab === 'code' && (
                <>
                  <span className="cb-pill-stat">{outputLines} lines</span>
                  <button
                    type="button"
                    className={`cb-btn-ghost ${copied ? 'cb-btn-copied' : ''}`}
                    onClick={handleCopy}
                    title="Copy code to clipboard"
                  >
                    {copied ? '💖 Copied!' : '📋 Copy'}
                  </button>
                  <button
                    type="button"
                    className="cb-btn-ghost"
                    onClick={handleDownload}
                    title="Download compilable code"
                  >
                    💾 Download Main.{targetLang === 'Java' ? 'java' : targetLang === 'C++' ? 'cpp' : 'py'}
                  </button>
                </>
              )}
            </div>
          </div>

          {/* Viewports */}
          <div className={`cb-viewport-container ${splitView ? 'is-split' : ''}`}>
            {/* View 1: Output Code */}
            {(activeTab === 'code' || splitView) && (
              <div className="cb-editor-wrapper cb-output-wrapper">
                {translatedCode ? (
                  <pre className="cb-code-pre">
                    <code>{translatedCode}</code>
                  </pre>
                ) : (
                  <div className="cb-empty-state-cute">
                    <div className="cb-cute-mascot-icon" aria-hidden="true">
                      <svg width="72" height="72" viewBox="0 0 64 64" fill="none">
                        <circle cx="32" cy="32" r="28" fill="currentColor" opacity="0.12" />
                        <rect x="14" y="16" width="36" height="32" rx="12" fill="#8B5CF6" />
                        <rect x="16" y="18" width="32" height="28" rx="10" fill="#A78BFA" />
                        <line x1="32" y1="16" x2="32" y2="8" stroke="#F472B6" strokeWidth="3" strokeLinecap="round" />
                        <circle cx="32" cy="7" r="4" fill="#F472B6" />
                        <path d="M22 28 Q 25 24 28 28" stroke="#1E1B4B" strokeWidth="2.5" strokeLinecap="round" fill="none" />
                        <path d="M36 28 Q 39 24 42 28" stroke="#1E1B4B" strokeWidth="2.5" strokeLinecap="round" fill="none" />
                        <ellipse cx="21" cy="33" rx="3" ry="2" fill="#FB7185" opacity="0.8" />
                        <ellipse cx="43" cy="33" rx="3" ry="2" fill="#FB7185" opacity="0.8" />
                        <path d="M29 33 Q 32 37 35 33" stroke="#1E1B4B" strokeWidth="2.2" strokeLinecap="round" fill="none" />
                      </svg>
                    </div>
                    <h3 className="cb-empty-heading">Ready when you are! ✨</h3>
                    <p className="cb-empty-text">
                      Choose an example above or write code on the left, then click <strong>"Translate Magic"</strong> to view clean, compilable {targetLang} with guaranteed entry points! 🌸
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* View 2: P3 Semantic Review */}
            {(activeTab === 'p3' || (splitView && activeTab !== 'code')) && (
              <div className="cb-panel-pane cb-p3-pane">
                {result?.p3_review ? (
                  <div className="cb-p3-content">
                    <div className="cb-verdict-card-cute">
                      <div className="cb-verdict-badge">
                        <span className="cb-verdict-icon">🛡️</span>
                        <strong>P3 Verification Assessment:</strong>
                      </div>
                      <p className="cb-verdict-text">{result.p3_review.overall_assessment}</p>
                    </div>

                    {result.p2_translation?.language_differences && result.p2_translation.language_differences.length > 0 && (
                      <div className="cb-section-block">
                        <h4 className="cb-section-title">🌸 Language Semantic Differences</h4>
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
                                <span className={`cb-sev-tag tag-${f.severity.toLowerCase()}`}>
                                  {f.severity === 'HIGH' ? '🚨 HIGH' : f.severity === 'MEDIUM' ? '⚠️ MEDIUM' : '💡 ' + f.severity}
                                </span>
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
                        <p className="cb-empty-sub">✨ All clear! No semantic divergence risks found.</p>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="cb-empty-state-cute">
                    <span className="cb-empty-emoji">🛡️</span>
                    <h3 className="cb-empty-heading">P3 Semantic Review</h3>
                    <p className="cb-empty-text">Click "Translate Magic" to inspect independent semantic audits and potential divergence risks.</p>
                  </div>
                )}
              </div>
            )}

            {/* View 3: P4 Tests */}
            {activeTab === 'p4' && !splitView && (
              <div className="cb-panel-pane cb-p4-pane">
                {result?.p4_tests?.test_cases && result.p4_tests.test_cases.length > 0 ? (
                  <div className="cb-p4-content">
                    <div className="cb-pane-intro">
                      <h4>🧪 P4 Synthesized Equivalence Test Vectors</h4>
                      <p>Equivalence vectors designed to verify behavioral parity between {sourceLang} and {targetLang}.</p>
                    </div>
                    <div className="cb-table-wrapper">
                      <table className="cb-tests-table">
                        <thead>
                          <tr>
                            <th>ID</th>
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
                              <td>
                                <span className={`cb-type-tag type-${tc.case_type.toLowerCase()}`}>
                                  {tc.case_type === 'normal' ? '🌟 normal' : tc.case_type === 'boundary' ? '🎯 boundary' : '⚡ ' + tc.case_type}
                                </span>
                              </td>
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
                  <div className="cb-empty-state-cute">
                    <span className="cb-empty-emoji">🧪</span>
                    <h3 className="cb-empty-heading">P4 Test Suite</h3>
                    <p className="cb-empty-text">Translate a program to automatically synthesize cross-language unit test cases.</p>
                  </div>
                )}
              </div>
            )}

            {/* View 4: P1 Analysis */}
            {activeTab === 'p1' && !splitView && (
              <div className="cb-panel-pane cb-p1-pane">
                {result?.p1_analysis ? (
                  <div className="cb-p1-content">
                    <div className="cb-pane-intro">
                      <h4>🔍 P1 Static AST Decomposition</h4>
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
                        <h5>Inferred I/O</h5>
                        <p>{result.p1_analysis.inputs_and_outputs}</p>
                      </div>

                      <div className="cb-card-box">
                        <h5>Control Flow</h5>
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
                  </div>
                ) : (
                  <div className="cb-empty-state-cute">
                    <span className="cb-empty-emoji">🔍</span>
                    <h3 className="cb-empty-heading">P1 Static Analysis</h3>
                    <p className="cb-empty-text">Translate your code to view the structural AST analysis and semantic constraints.</p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Footer Bar */}
          <div className="cb-box-footer">
            <span className="cb-hint">
              {result?.metadata
                ? `✨ Model: ${result.metadata.model_id} | Pipeline: 4 Steps (P1 → P2 → P3 → P4) | Semantics Preserved 💖`
                : `Target: ${targetLang} (with public class Main)`}
            </span>
          </div>
        </section>
      </main>
    </div>
  );
}