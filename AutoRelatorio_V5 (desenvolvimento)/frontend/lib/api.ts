/**
 * AutoRelatório V5 — Cliente HTTP centralizado
 *
 * Consumo da API do backend Python (motor de geração).
 * URL base: variável de ambiente NEXT_PUBLIC_API_URL
 * fallback: http://localhost:5000 (backend FastAPI local)
 */

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:5000';

// ─── Tipos ────────────────────────────────────────────────────────────────────

export interface ApiError {
  status: number;
  message: string;
}

export interface GeneratePayload {
  contrato_id:   string;
  nr_os:         string;
  ag_cod:        string;
  ag_nome:       string;
  dt_atend:      string;
  endereco:      string;
  responsavel:   string;
  desc_index:    string;   // '1' | '2' | '3' | '4'
  modo:          string;   // 'trad' | 'sp' | 'sp2'
  root_path?:    string;   // pasta de fotos (opcional, enviado pelo Electron/futuro)
}

export interface GenerateResponse {
  ok:       boolean;
  filename: string;
  url:      string;   // blob URL para download direto no browser
  message?: string;
}

export interface HealthResponse {
  status: 'ok' | 'degraded';
  version: string;
}

// ─── Utilitário — JSON ────────────────────────────────────────────────────────

async function request<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const err: ApiError = {
      status:  res.status,
      message: (body as { detail?: string }).detail
               ?? `Erro ${res.status}: ${res.statusText}`,
    };
    throw err;
  }

  return res.json() as Promise<T>;
}

// ─── Utilitário — Download de arquivo ────────────────────────────────────────

/**
 * Faz POST e espera um arquivo binário (FileResponse do FastAPI).
 * Retorna um blob URL para download automático no browser.
 */
async function requestFile(
  path: string,
  body: unknown,
): Promise<GenerateResponse> {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    const err: ApiError = {
      status:  res.status,
      message: (errBody as { detail?: string }).detail
               ?? `Erro ${res.status}: ${res.statusText}`,
    };
    throw err;
  }

  // Extrai o nome do arquivo do header Content-Disposition
  const disposition = res.headers.get('content-disposition') ?? '';
  const filenameMatch = disposition.match(/filename[^;=\n]*=['"]?([^'";\n]+)['"]?/i);
  const filename = filenameMatch?.[1] ?? 'relatorio.docx';

  // Converte o binário em blob URL para download
  const blob = await res.blob();
  const url  = URL.createObjectURL(blob);

  return { ok: true, filename, url };
}

// ─── Endpoints públicos ───────────────────────────────────────────────────────

/** Verifica saúde do backend */
export const checkHealth = () =>
  request<HealthResponse>('/health');

/**
 * Solicita a geração do relatório .docx.
 * O backend processa scan + build_word e retorna o arquivo diretamente.
 * A função cria um blob URL para download automático no browser.
 */
export const generateReport = (payload: GeneratePayload) =>
  requestFile('/generate', payload);
