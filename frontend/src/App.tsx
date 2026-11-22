import { useState } from 'react';
import { translate } from './api';
import { TranslateResponse, Finding, TestCase } from './types';
import './App.css';

const LANGUAGES = ['Python', 'Java', 'C++'];

function safeText(val: unknown): string {
  if (val === null || val === undefined) return '';
  if (typeof val === 'object') return JSON.stringify(val, null, 2);
  return String(val);
}

function SeverityBadge({ severity }: { severity?: string }) {
  const sev = (severity || 'INFO').toUpperCase();
  const cls = `severity-badge severity-${sev}`;
  return <span className={cls}>{sev}</span>;
}

function AccordionPanel({
  title,
  children,
  defaultOpen = false,
}: {
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="panel-card">
      <button className="panel-header" onClick={() => setOpen((o) => !o)}>
        <span>{title}</span>
        <span className="panel-chevron">{open ? '▲' : '▼'}</span>
      </button>
      {open && <div className="panel-body">{children}</div>}
    </div>
  );
}

function P1Panel({ data }: { data?: TranslateResponse['p1_analysis'] }) {
  if (!data) return null;
  const functions = data.functions || [];
  const dataStructures = data.data_structures || [];
  const dependencies = data.dependencies || [];
  const semantics = data.language_semantics_to_preserve || [];
  const edgeCases = data.edge_cases || [];
  const assumptions = data.assumptions || [];
  const unsupported = data.unsupported_or_ambiguous || [];

  return (
    <AccordionPanel title="P1 — Source Analysis" defaultOpen>
      <p><strong>Summary:</strong> {data.program_summary}</p>
      {data.inputs_and_outputs && (
        <p><strong>Inputs & Outputs:</strong> {safeText(data.inputs_and_outputs)}</p>
      )}
      {data.control_flow && (
        <p><strong>Control Flow:</strong> {safeText(data.control_flow)}</p>
      )}
      {functions.length > 0 && (
        <>
          <strong>Functions:</strong>
          <ul>{functions.map((f, i) => <li key={i}>{safeText(f)}</li>)}</ul>
        </>
      )}
      {dataStructures.length > 0 && (
        <>
          <strong>Data Structures:</strong>
          <ul>{dataStructures.map((d, i) => <li key={i}>{safeText(d)}</li>)}</ul>
        </>
      )}
      {dependencies.length > 0 && (
        <>
          <strong>Dependencies:</strong>
          <ul>{dependencies.map((d, i) => <li key={i}>{safeText(d)}</li>)}</ul>
        </>
      )}
      {semantics.length > 0 && (
        <>
          <strong>Semantics to Preserve:</strong>
          <ul>{semantics.map((s, i) => <li key={i}>{safeText(s)}</li>)}</ul>
        </>
      )}
      {edgeCases.length > 0 && (
        <>
          <strong>Edge Cases:</strong>
          <ul>{edgeCases.map((e, i) => <li key={i}>{safeText(e)}</li>)}</ul>
        </>
      )}
      {assumptions.length > 0 && (
        <>
          <strong>Assumptions:</strong>
          <ul>{assumptions.map((a, i) => <li key={i}>{safeText(a)}</li>)}</ul>
        </>
      )}
      {unsupported.length > 0 && (
        <>
          <strong>Unsupported / Ambiguous:</strong>
          <ul>{unsupported.map((u, i) => <li key={i}>{safeText(u)}</li>)}</ul>
        </>
      )}
      {data.confidence_notes && (
        <p><strong>Confidence Notes:</strong> {data.confidence_notes}</p>
      )}
    </AccordionPanel>
  );
}

function P2Panel({ data }: { data?: TranslateResponse['p2_translation'] }) {
  if (!data) return null;
  const [copied, setCopied] = useState(false);
  const diffs = data.language_differences || [];
  const assumptions = data.assumptions || [];
  const issues = data.potential_issues || [];
  const unsupported = data.unsupported_features || [];

  const handleCopy = () => {
    navigator.clipboard.writeText(data.translated_code || '').then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <AccordionPanel title="P2 — Translated Code" defaultOpen>
      <div className="code-block-wrapper">
        <button className="copy-btn" onClick={handleCopy}>
          {copied ? '✓ Copied' : 'Copy'}
        </button>
        <pre><code>{data.translated_code}</code></pre>
      </div>
      {diffs.length > 0 && (
        <>
          <strong>Language Differences:</strong>
          <ul>{diffs.map((d, i) => <li key={i}>{safeText(d)}</li>)}</ul>
        </>
      )}
      {assumptions.length > 0 && (
        <>
          <strong>Assumptions:</strong>
          <ul>{assumptions.map((a, i) => <li key={i}>{safeText(a)}</li>)}</ul>
        </>
      )}
      {issues.length > 0 && (
        <>
          <strong>Potential Issues:</strong>
          <ul>{issues.map((p, i) => <li key={i}>{safeText(p)}</li>)}</ul>
        </>
      )}
      {unsupported.length > 0 && (
        <>
          <strong>Unsupported Features:</strong>
          <ul>{unsupported.map((u, i) => <li key={i}>{safeText(u)}</li>)}</ul>
        </>
      )}
      <p className="review-notice">
        ⚠ Manual verification required — translation has not been executed or tested.
      </p>
    </AccordionPanel>
  );
}

function P3Panel({ data }: { data?: TranslateResponse['p3_review'] }) {
  if (!data) return null;
  const findings = data.findings || [];
  const diffs = data.behavioural_differences || [];
  const unverified = data.unverified_assumptions || [];
  const recommendedTests = data.recommended_tests || [];

  return (
    <AccordionPanel title="P3 — Review & Risk Assessment">
      <p><strong>Assessment:</strong> {data.overall_assessment}</p>
      <p className="review-notice">
        ⚠ Human review required — no automated testing was performed. Results below are proposed findings only.
      </p>

      {findings.length > 0 && (
        <>
          <strong>Findings:</strong>
          <div className="table-wrapper">
            <table className="findings-table">
              <thead>
                <tr>
                  <th>Severity</th>
                  <th>Location</th>
                  <th>Explanation</th>
                  <th>Correction</th>
                </tr>
              </thead>
              <tbody>
                {findings.map((f: Finding, i: number) => (
                  <tr key={i}>
                    <td><SeverityBadge severity={f.severity} /></td>
                    <td><code>{safeText(f.location)}</code></td>
                    <td>{safeText(f.explanation)}</td>
                    <td>{safeText(f.correction)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {diffs.length > 0 && (
        <>
          <strong>Behavioural Differences:</strong>
          <ul>{diffs.map((d, i) => <li key={i}>{safeText(d)}</li>)}</ul>
        </>
      )}
      {unverified.length > 0 && (
        <>
          <strong>Unverified Assumptions:</strong>
          <ul>{unverified.map((a, i) => <li key={i}>{safeText(a)}</li>)}</ul>
        </>
      )}
      {recommendedTests.length > 0 && (
        <>
          <strong>Recommended Tests:</strong>
          <ul>{recommendedTests.map((t, i) => <li key={i}>{safeText(t)}</li>)}</ul>
        </>
      )}
    </AccordionPanel>
  );
}

function P4Panel({ data }: { data?: TranslateResponse['p4_tests'] }) {
  if (!data) return null;
  const testCases = data.test_cases || [];
  const oracleNeeded = data.tests_requiring_human_oracle || [];

  return (
    <AccordionPanel title="P4 — Proposed Test Cases">
      <div className="proposed-badge">Tests are PROPOSED — not executed</div>
      {testCases.length > 0 && (
        <div className="table-wrapper">
          <table className="tests-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Purpose</th>
                <th>Input</th>
                <th>Expected Output</th>
                <th>Confidence</th>
                <th>Type</th>
                <th>Risk Target</th>
              </tr>
            </thead>
            <tbody>
              {testCases.map((tc: TestCase, i: number) => (
                <tr key={i}>
                  <td><code>{tc.test_id}</code></td>
                  <td>{tc.purpose}</td>
                  <td><code>{safeText(tc.input)}</code></td>
                  <td><code>{safeText(tc.expected_output)}</code></td>
                  <td>{tc.expected_output_confidence}</td>
                  <td>{tc.case_type}</td>
                  <td>{safeText(tc.risk_target)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {data.execution_notes && (
        <p><strong>Execution Notes:</strong> {data.execution_notes}</p>
      )}
      {oracleNeeded.length > 0 && (
        <>
          <strong>Requires Human Oracle:</strong>
          <ul>{oracleNeeded.map((t, i) => <li key={i}>{safeText(t)}</li>)}</ul>
        </>
      )}
    </AccordionPanel>
  );
}

export default function App() {
  const [sourceCode, setSourceCode] = useState('');
  const [sourceLang, setSourceLang] = useState('Python');
  const [targetLang, setTargetLang] = useState('Java');
  const [userContext, setUserContext] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<TranslateResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!sourceCode.trim()) {
      setError('Source code cannot be empty.');
      return;
    }
    if (sourceLang === targetLang) {
      setError('Source and target languages must be different.');
      return;
    }

    setLoading(true);
    setResult(null);
    try {
      const res = await translate({
        source_code: sourceCode,
        source_language: sourceLang,
        target_language: targetLang,
        user_context: userContext || undefined,
      });
      setResult(res);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = () => {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'codebridge-report.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>CodeBridge</h1>
        <p className="app-subtitle">Semantics-aware code translation powered by Gemini</p>
      </header>

      <main>
        <form onSubmit={handleSubmit} className="translate-form">
          <div className="form-row lang-row">
            <div className="form-group">
              <label htmlFor="sourceLang">Source Language</label>
              <select
                id="sourceLang"
                value={sourceLang}
                onChange={(e) => setSourceLang(e.target.value)}
                disabled={loading}
              >
                {LANGUAGES.map((l) => <option key={l}>{l}</option>)}
              </select>
            </div>
            <div className="lang-arrow">→</div>
            <div className="form-group">
              <label htmlFor="targetLang">Target Language</label>
              <select
                id="targetLang"
                value={targetLang}
                onChange={(e) => setTargetLang(e.target.value)}
                disabled={loading}
              >
                {LANGUAGES.map((l) => <option key={l}>{l}</option>)}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="sourceCode">Source Code</label>
            <textarea
              id="sourceCode"
              className="code-textarea"
              value={sourceCode}
              onChange={(e) => setSourceCode(e.target.value)}
              placeholder="Paste your source code here..."
              rows={16}
              disabled={loading}
              spellCheck={false}
            />
          </div>

          <div className="form-group">
            <label htmlFor="userContext">Additional Context <span className="optional">(optional)</span></label>
            <textarea
              id="userContext"
              value={userContext}
              onChange={(e) => setUserContext(e.target.value)}
              placeholder="e.g. This is a web server handler, preserve HTTP status codes..."
              rows={3}
              disabled={loading}
            />
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner" />
                Analysing and translating...
              </>
            ) : (
              'Translate Code'
            )}
          </button>
        </form>

        {error && (
          <div className="error-banner" role="alert">
            <strong>Error:</strong> {error}
          </div>
        )}

        {result && (
          <section className="results-section">
            <div className="results-header">
              <h2>Translation Results</h2>
              <button className="export-btn" onClick={handleExport}>
                ⬇ Export Report (JSON)
              </button>
            </div>
            <div className="metadata-bar">
              <span>Model: <code>{result.metadata?.model_id || 'Gemini'}</code></span>
              <span>Time: <code>{result.metadata?.timestamp ? new Date(result.metadata.timestamp).toLocaleString() : ''}</code></span>
              <span>{result.metadata?.source_language} → {result.metadata?.target_language}</span>
            </div>
            <P1Panel data={result.p1_analysis} />
            <P2Panel data={result.p2_translation} />
            <P3Panel data={result.p3_review} />
            <P4Panel data={result.p4_tests} />
          </section>
        )}
      </main>
    </div>
  );
}
