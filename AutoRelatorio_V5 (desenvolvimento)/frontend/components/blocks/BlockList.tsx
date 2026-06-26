'use client';

/**
 * BlockList — Lista de blocos detectados + seletor de pasta.
 *
 * Orquestra:
 * - FolderPicker (input webkitdirectory)
 * - Lista de BlockCard
 * - Barra de progresso (fotos com item / total)
 */

import { useRef } from 'react';
import type { Bloco, ItemContrato } from '@/hooks/useBlocks';
import { BlockCard } from './BlockCard';

interface BlockListProps {
  blocos:      Bloco[];
  items:       ItemContrato[];
  itemsLoading: boolean;
  fotosComItem: number;
  onCarregar:  (files: FileList) => void;
  onSetItem:   (id: string, item: ItemContrato | undefined) => void;
  onSetMedida: (id: string, campo: keyof Bloco['medidas'], valor: number) => void;
  onRemover:   (id: string) => void;
  onLimpar:    () => void;
}

export function BlockList({
  blocos, items, itemsLoading, fotosComItem,
  onCarregar, onSetItem, onSetMedida, onRemover, onLimpar,
}: BlockListProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onCarregar(e.target.files);
      // Reset para permitir re-seleção da mesma pasta
      e.target.value = '';
    }
  };

  const total = blocos.length;
  const progresso = total > 0 ? Math.round((fotosComItem / total) * 100) : 0;

  return (
    <div className="blocklist-root">
      {/* ── Input oculto ──────────────────────────────────────────────── */}
      <input
        ref={inputRef}
        type="file"
        /* @ts-expect-error — webkitdirectory não está no tipo padrão mas funciona */
        webkitdirectory="true"
        multiple
        accept="image/*"
        style={{ display: 'none' }}
        onChange={handleInputChange}
      />

      {/* ── Zona de seleção ───────────────────────────────────────────── */}
      <div className="scan-zone" onClick={() => inputRef.current?.click()}>
        <div className="scan-zone-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round">
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
          </svg>
        </div>
        <div className="scan-zone-title">
          {total > 0 ? `${total} foto${total > 1 ? 's' : ''} carregada${total > 1 ? 's' : ''} — clique para trocar` : 'Selecionar Pasta de Fotos'}
        </div>
        <div className="scan-zone-sub">
          {total > 0
            ? 'Seleciona uma nova pasta para substituir'
            : 'Abre o explorador de arquivos — selecione a pasta da agência'}
        </div>
      </div>

      {/* ── Barra de progresso ────────────────────────────────────────── */}
      {total > 0 && (
        <div className="bl-progress-wrap">
          <div className="bl-progress-bar" style={{ '--prog': `${progresso}%` } as React.CSSProperties} />
          <div className="bl-progress-label">
            <span>{fotosComItem} de {total} fotos com item associado</span>
            <button className="bl-clear-btn" onClick={onLimpar}>Limpar tudo</button>
          </div>
        </div>
      )}

      {/* ── Items loading ─────────────────────────────────────────────── */}
      {itemsLoading && (
        <p className="bl-items-loading">
          <svg className="spinner-svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
          </svg>
          Carregando itens do contrato...
        </p>
      )}

      {/* ── Lista de blocos ───────────────────────────────────────────── */}
      <div className="bl-list">
        {blocos.map(b => (
          <BlockCard
            key={b.id}
            bloco={b}
            items={items}
            onSetItem={onSetItem}
            onSetMedida={onSetMedida}
            onRemover={onRemover}
          />
        ))}
      </div>

      {/* ── Empty state ───────────────────────────────────────────────── */}
      {total === 0 && (
        <div className="empty-state" style={{ marginTop: 12 }}>
          <div className="empty-state-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round">
              <path d="M4 16l4.586-4.586a2 2 0 0 1 2.828 0L16 16m-2-2l1.586-1.586a2 2 0 0 1 2.828 0L20 14m-6-6h.01M6 20h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2z" />
            </svg>
          </div>
          <div className="empty-state-title">Nenhuma foto carregada</div>
          <div className="empty-state-desc">
            Selecione a pasta da agência para detectar as fotos automaticamente
          </div>
        </div>
      )}
    </div>
  );
}
