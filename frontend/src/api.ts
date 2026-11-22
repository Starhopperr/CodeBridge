import { TranslateRequest, TranslateResponse } from './types';

// Use relative path so Vite proxy (dev) or unified server (prod) handles routing cleanly.
// Can be overridden with VITE_API_URL environment variable if backend is on a separate port/domain.
const BASE_URL = import.meta.env.VITE_API_URL || '';

export async function translate(req: TranslateRequest): Promise<TranslateResponse> {
  const url = BASE_URL ? `${BASE_URL}/api/translate` : '/api/translate';
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}` }));
      throw new Error(err.detail || `Server error (${res.status})`);
    }
    return res.json();
  } catch (err: unknown) {
    if (err instanceof TypeError && err.message.toLowerCase().includes('fetch')) {
      throw new Error(
        'Backend server is not reachable. Please ensure the FastAPI backend is running on http://localhost:8000 (run: uvicorn main:app --app-dir backend --reload).'
      );
    }
    throw err;
  }
}
