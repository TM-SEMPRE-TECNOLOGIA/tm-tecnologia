/**
 * useApiState — padrão UiState para chamadas ao backend.
 *
 * Encapsula loading / error / data / empty em um objeto coeso,
 * expõe `run(asyncFn)` que gerencia todo o ciclo automaticamente.
 *
 * Uso:
 *   const { state, run } = useApiState<GenerateResponse>();
 *   const handleGenerate = () => run(() => generateReport(payload));
 */

import { useState, useCallback } from 'react';
import type { ApiError } from '@/lib/api';

export type ApiStatus = 'idle' | 'loading' | 'success' | 'error';

export interface UiState<T> {
  status:  ApiStatus;
  data:    T | null;
  error:   string | null;
  isEmpty: boolean;
}

const INITIAL = <T>(): UiState<T> => ({
  status:  'idle',
  data:    null,
  error:   null,
  isEmpty: false,
});

export function useApiState<T>() {
  const [state, setState] = useState<UiState<T>>(INITIAL<T>());

  const run = useCallback(async (asyncFn: () => Promise<T>) => {
    // 1. Loading
    setState({ status: 'loading', data: null, error: null, isEmpty: false });

    try {
      const data = await asyncFn();

      // 2. Detecta empty (arrays vazios ou objetos sem dados)
      const isEmpty =
        data === null ||
        data === undefined ||
        (Array.isArray(data) && data.length === 0);

      // 3. Sucesso
      setState({ status: 'success', data, error: null, isEmpty });
      return data;
    } catch (err) {
      // 4. Erro — trata ApiError ou Error genérico
      const message =
        (err as ApiError)?.message ??
        (err as Error)?.message ??
        'Erro desconhecido. Tente novamente.';

      setState({ status: 'error', data: null, error: message, isEmpty: false });
      return null;
    }
  }, []);

  const reset = useCallback(() => setState(INITIAL<T>()), []);

  return { state, run, reset };
}
