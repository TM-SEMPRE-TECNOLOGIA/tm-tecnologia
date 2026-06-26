'use client';

import { useContracts } from '@/hooks/useContracts';
import type { ContractMode } from '@/lib/contracts';

interface TopBarProps {
  onStartClick:    () => void;
  onNewClick:      () => void;
  onGenerateClick: () => void;
  isGenerating?:   boolean;
}

export function TopBar({ onStartClick, onNewClick, onGenerateClick, isGenerating }: TopBarProps) {
  const { currentContract } = useContracts();

  const modeConfig: Record<ContractMode, { label: string; className: string }> = {
    'trad': { label: 'TRADICIONAL', className: 'mode-trad' },
    'sp': { label: 'SP', className: 'mode-sp' },
    'sp2': { label: 'SP2', className: 'mode-sp2' },
  };

  const modeInfo = modeConfig[currentContract.mode];

  return (
    <header className="topbar">
      <a className="brand" href="#">
        <div className="brand-logo">📄</div>
        <span className="brand-name">AutoRelatório</span>
        <span className="brand-ver">V5</span>
      </a>

      <div className="topbar-div"></div>

      <div className="topbar-contract">
        <span className="contract-pill">{currentContract.id}</span>
        <span className="contract-name">{currentContract.name}</span>
        <span className={`mode-pill ${modeInfo.className}`}>{modeInfo.label}</span>
      </div>

      <div className="topbar-spacer"></div>

      <div className="topbar-actions">
        <div className="status-badge">
          <span className="dot-live"></span>
          VISUALIZAÇÃO PRÉVIA
        </div>

        <button className="btn btn-primary btn-sm" onClick={onStartClick} title="Inicia servidor local">
          ▶ START
        </button>

        <button className="btn btn-ghost btn-sm" onClick={onNewClick} title="Novo relatório">
          ← Novo
        </button>

        <button
          className="btn btn-primary btn-sm"
          onClick={onGenerateClick}
          disabled={isGenerating}
          title="Gera arquivo .docx"
        >
          {isGenerating ? (
            <>
              <svg className="spinner-svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
              </svg>
              Gerando...
            </>
          ) : (
            <>📄 Gerar .docx</>
          )}
        </button>
      </div>
    </header>
  );
}
