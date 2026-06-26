'use client';

import { useContracts } from '@/hooks/useContracts';
import { useTheme } from '@/hooks/useTheme';
import { useState } from 'react';

interface SidebarProps {
  onSettingsClick: () => void;
}

export function Sidebar({ onSettingsClick }: SidebarProps) {
  const { currentContract, contracts, selectContract } = useContracts();
  const { isDark, toggleTheme } = useTheme();
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <nav className={`nav ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="nav-section">
        <div className="nav-label">Menu</div>
        <button className="nav-item active">
          📄 Gerar Relatório
        </button>
        <button className="nav-item">
          🕐 Histórico
        </button>
      </div>

      <div className="nav-div"></div>

      <div className="nav-toggle-row">
        <div className="nav-label">Contratos</div>
        <button
          className="nav-toggle-btn"
          onClick={() => setIsCollapsed(!isCollapsed)}
          title="Encolher/Expandir"
        >
          ◀
        </button>
      </div>

      <div className="contract-list">
        {contracts.map(contract => (
          <div
            key={contract.id}
            className={`c-item ${contract.id === currentContract.id ? 'active' : ''}`}
            onClick={() => selectContract(contract.id)}
          >
            <span className="c-id">{contract.id}</span>
            {!isCollapsed && (
              <>
                <div className="c-info">
                  <div className="c-name">{contract.name}</div>
                  <div className="c-mode">{contract.mode.toUpperCase()} · {contract.uf}</div>
                </div>
                <div className="c-dot"></div>
              </>
            )}
          </div>
        ))}
      </div>

      <div className="nav-footer">
        <button
          className="nav-footer-btn"
          onClick={toggleTheme}
          title={isDark ? 'Modo claro' : 'Modo escuro'}
        >
          {isDark ? '☀️' : '🌙'}
        </button>
        <button
          className="nav-footer-btn"
          onClick={onSettingsClick}
          title="Configurações"
        >
          ⚙️
        </button>
      </div>
    </nav>
  );
}
