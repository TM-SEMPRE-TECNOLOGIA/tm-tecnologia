'use client';

/**
 * ErrorMessage — feedback de erro com opção de retry.
 *
 * Modos:
 *  - inline  : texto simples com ícone (próximo ao campo/seção afetada)
 *  - block   : card centralizado com botão retry (substitui seção)
 */

interface ErrorMessageProps {
  message:   string;
  mode?:     'inline' | 'block';
  onRetry?:  () => void;
}

export function ErrorMessage({
  message,
  mode    = 'block',
  onRetry,
}: ErrorMessageProps) {

  const icon = (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--error)" strokeWidth="2.5" strokeLinecap="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  );

  if (mode === 'inline') {
    return (
      <span className="error-inline">
        {icon}
        <span>{message}</span>
      </span>
    );
  }

  return (
    <div className="error-block">
      <div className="error-block-icon">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--error)" strokeWidth="1.75" strokeLinecap="round">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
      </div>
      <p className="error-block-msg">{message}</p>
      {onRetry && (
        <button className="btn btn-ghost btn-sm" onClick={onRetry}>
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
            <polyline points="1 4 1 10 7 10" />
            <path d="M3.51 15a9 9 0 1 0 .49-3.1" />
          </svg>
          Tentar novamente
        </button>
      )}
    </div>
  );
}
