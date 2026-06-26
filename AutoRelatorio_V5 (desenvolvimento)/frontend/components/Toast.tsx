'use client';

import { useEffect } from 'react';

export type ToastType = 'success' | 'error' | 'info' | 'loading';

interface ToastProps {
  message:  string;
  type?:    ToastType;
  onClose:  () => void;
  duration?: number; // ms — 0 = não fecha automaticamente (ex: loading)
}

const ICONS: Record<ToastType, React.ReactNode> = {
  success: (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--green)" strokeWidth="2.5" strokeLinecap="round">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  ),
  error: (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--error)" strokeWidth="2.5" strokeLinecap="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="15" y1="9" x2="9" y2="15" />
      <line x1="9" y1="9" x2="15" y2="15" />
    </svg>
  ),
  info: (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--blue-text)" strokeWidth="2.5" strokeLinecap="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  ),
  loading: (
    <svg className="spinner-svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--orange)" strokeWidth="2.5" strokeLinecap="round">
      <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
    </svg>
  ),
};

export function Toast({ message, type = 'success', onClose, duration }: ToastProps) {
  // Duração padrão por tipo (0 = não fecha)
  const ms = duration !== undefined ? duration : type === 'loading' ? 0 : type === 'error' ? 5000 : 3500;

  useEffect(() => {
    if (ms === 0) return; // loading/permanente não fecha automaticamente
    const timer = setTimeout(onClose, ms);
    return () => clearTimeout(timer);
  }, [onClose, ms]);

  return (
    <div className="toast-area" role="status" aria-live="polite">
      <div className={`toast toast-${type}`}>
        <span className="toast-icon">{ICONS[type]}</span>
        <span className="toast-msg">{message}</span>
        {type !== 'loading' && (
          <button className="toast-close" onClick={onClose} aria-label="Fechar">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
}
