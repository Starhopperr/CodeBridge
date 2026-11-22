import React, { useState, useRef } from 'react';
import { translate } from './api';
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
    title: 'Python → Java: Factorial',
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
    title: 'Java → Python: Solution Class',
    sourceLang: 'Java',
    targetLang: 'Python',
    code: `public class Solution {
    public static int add(int a, int b) {
        return a + b;
    }
}
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

export default function App() {
  const [sourceLang, setSourceLang] = useState('Python');
  const [targetLang, setTargetLang] = useState('Java');
  const [sourceCode, setSourceCode] = useState(SAMPLES[0].code);
  const [translatedCode, setTranslatedCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [engineInfo, setEngineInfo] = useState<string | null>(null);

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
      setEngineInfo(null);
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
      const code = res.p2_translation?.translated_code || '';
      setTranslatedCode(code);
      setEngineInfo(res.metadata?.model_id || 'CodeBridge Engine');
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
    const filename = `Solution.${ext}`;
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
    setError(null);
    setEngineInfo(null);
  };

  const inputLines = sourceCode.split('\n').length;
  const outputLines = translatedCode ? translatedCode.split('\n').length : 0;

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

        {/* Center Language & Action Bar */}
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
              aria-label="Swap source and target languages"
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

        {/* Right Samples Dropdown */}
        <div className="cb-samples">
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
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <span className="cb-error-msg">{error}</span>
          <button className="cb-error-dismiss" onClick={() => setError(null)} aria-label="Dismiss error">
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
                  setEngineInfo(null);
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
            <span className="cb-hint">Press <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to translate</span>
          </div>
        </section>

        {/* Box 2: Output Code Box */}
        <section className="cb-box cb-output-box">
          <div className="cb-box-header">
            <div className="cb-box-title">
              <span className={`cb-dot ${translatedCode ? 'cb-dot-active' : 'cb-dot-idle'}`} />
              <span>Output ({targetLang})</span>
            </div>
            <div className="cb-box-meta">
              {translatedCode && (
                <>
                  <span className="cb-stat">{outputLines} lines</span>
                  <span className="cb-stat-sep">•</span>
                  <span className="cb-stat">{translatedCode.length} chars</span>
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

          <div className="cb-editor-wrapper cb-output-wrapper">
            {translatedCode ? (
              <pre className="cb-code-pre">
                <code>{translatedCode}</code>
              </pre>
            ) : (
              <div className="cb-empty-state">
                <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                  <polyline points="10 9 9 9 8 9" />
                </svg>
                <p className="cb-empty-text">Translated {targetLang} code will appear here</p>
                <span className="cb-empty-sub">Click "Translate" or press Ctrl+Enter</span>
              </div>
            )}
          </div>

          <div className="cb-box-footer">
            <span className="cb-hint">
              {engineInfo ? `Engine: ${engineInfo}` : `Target: ${targetLang}`}
            </span>
          </div>
        </section>
      </main>
    </div>
  );
}
