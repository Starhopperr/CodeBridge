import { TranslateRequest, TranslateResponse } from './types';

const BASE_URL = 'http://localhost:8000';

export async function translate(req: TranslateRequest): Promise<TranslateResponse> {
  const res = await fetch(`${BASE_URL}/api/translate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}
