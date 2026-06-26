'use client';

/**
 * useItems — Carrega os itens do contrato atual para o dropdown do Step 2.
 *
 * Tenta buscar do backend GET /api/contracts/{id}/items.
 * Em caso de falha (backend offline), usa items.json estático local.
 */

import { useState, useEffect } from 'react';
import type { ItemContrato } from './useBlocks';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:5000';

// Formato do backend: { "17.2": { codigo, descricao, unidade }, ... }
type ItemsMap = Record<string, { descricao?: string; unidade?: string; codigo?: string }>;

function mapToArray(data: ItemsMap): ItemContrato[] {
  return Object.entries(data).map(([codigo, v]) => ({
    codigo:    v.codigo ?? codigo,
    descricao: v.descricao ?? codigo,
    unidade:   v.unidade  ?? 'un',
  })).sort((a, b) => {
    // Ordena por código numericamente (ex: 17.2 < 17.10)
    const numA = a.codigo.split('.').map(Number);
    const numB = b.codigo.split('.').map(Number);
    for (let i = 0; i < Math.max(numA.length, numB.length); i++) {
      const diff = (numA[i] ?? 0) - (numB[i] ?? 0);
      if (diff !== 0) return diff;
    }
    return 0;
  });
}

export function useItems(contractId: string) {
  const [items, setItems] = useState<ItemContrato[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!contractId) return;

    let cancelled = false;
    setLoading(true);
    setError(null);

    fetch(`${BASE_URL}/api/contracts/${contractId}/items`)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json() as Promise<ItemsMap>;
      })
      .then(data => {
        if (!cancelled) {
          setItems(mapToArray(data));
          setLoading(false);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setError('Backend offline — itens não carregados');
          setItems([]);
          setLoading(false);
        }
      });

    return () => { cancelled = true; };
  }, [contractId]);

  return { items, loading, error };
}
