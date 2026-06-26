'use client';

/**
 * BlockCard — Card de uma foto detectada no Step 2.
 *
 * Mostra: thumbnail da foto, nome do arquivo, pasta,
 * dropdown de item, formulário de medidas adaptativo e botão remover.
 */

import { useState } from 'react';
import type { Bloco, ItemContrato } from '@/hooks/useBlocks';
import { MeasureForm } from './MeasureForm';

interface BlockCardProps {
  bloco:      Bloco;
  items:      ItemContrato[];
  onSetItem:  (id: string, item: ItemContrato | undefined) => void;
  onSetMedida:(id: string, campo: keyof Bloco['medidas'], valor: number) => void;
  onRemover:  (id: string) => void;
}

export function BlockCard({ bloco, items, onSetItem, onSetMedida, onRemover }: BlockCardProps) {
  const [expanded, setExpanded] = useState(true);

  const handleItemChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    if (!val) {
      onSetItem(bloco.id, undefined);
      return;
    }
    const found = items.find(it => it.codigo === val);
    if (found) onSetItem(bloco.id, found);
  };

  const hasItem = !!bloco.item;
  const isOk    = hasItem && bloco.total > 0;

  return (
    <div className={`block-card ${isOk ? 'block-card--ok' : hasItem ? 'block-card--partial' : ''}`}>
      {/* ── Header ────────────────────────────────────────────────────── */}
      <div className="block-card-header" onClick={() => setExpanded(e => !e)}>
        <div className="block-thumb-wrap">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={bloco.previewUrl}
            alt={bloco.nome}
            className="block-thumb"
          />
        </div>
        <div className="block-meta">
          <div className="block-nome">
            {bloco.numero && <span className="block-num">{bloco.numero}</span>}
            {bloco.nome}
          </div>
          <div className="block-pasta">{bloco.pasta}</div>
          {bloco.item && (
            <div className="block-item-badge">
              <span className="block-item-cod">{bloco.item.codigo}</span>
              <span className="block-item-desc">{bloco.item.descricao}</span>
            </div>
          )}
        </div>
        <div className="block-header-right">
          {isOk && (
            <span className="block-total-pill">
              {bloco.total.toLocaleString('pt-BR', { minimumFractionDigits: 2 })} {bloco.item?.unidade}
            </span>
          )}
          <button
            className="block-remove-btn"
            title="Remover foto"
            onClick={e => { e.stopPropagation(); onRemover(bloco.id); }}
          >
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
          <svg
            className={`block-chevron ${expanded ? 'block-chevron--open' : ''}`}
            width="12" height="12" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"
          >
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </div>
      </div>

      {/* ── Body (expansível) ─────────────────────────────────────────── */}
      {expanded && (
        <div className="block-card-body">
          {/* Dropdown de item */}
          <div className="block-field">
            <label className="block-field-label">Item do Contrato</label>
            <select
              className="block-select"
              value={bloco.item?.codigo ?? ''}
              onChange={handleItemChange}
            >
              <option value="">— selecionar item —</option>
              {items.map(it => (
                <option key={it.codigo} value={it.codigo}>
                  {it.codigo} — {it.descricao} ({it.unidade})
                </option>
              ))}
            </select>
          </div>

          {/* Formulário de medidas (só aparece quando item selecionado) */}
          {bloco.item && (
            <MeasureForm
              unidade={bloco.item.unidade}
              medidas={bloco.medidas}
              total={bloco.total}
              onChange={(campo, valor) => onSetMedida(bloco.id, campo, valor)}
            />
          )}

          {/* Mensagem quando sem item */}
          {!bloco.item && (
            <p className="block-no-item-msg">
              Selecione o item acima para preencher as medidas.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
