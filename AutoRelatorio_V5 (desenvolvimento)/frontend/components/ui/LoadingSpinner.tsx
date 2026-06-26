'use client';

/**
 * LoadingSpinner — indicador de carregamento contextual.
 *
 * Modos:
 *  - inline  : spinner pequeno + texto lado a lado (dentro de botão, etc.)
 *  - block   : spinner centralizado com mensagem abaixo (substitui seção)
 *  - overlay : tela toda bloqueada (operação global, ex: gerar .docx)
 */

interface LoadingSpinnerProps {
  mode?:    'inline' | 'block' | 'overlay';
  message?: string;
  size?:    number;
}

export function LoadingSpinner({
  mode    = 'block',
  message = 'Processando...',
  size    = 22,
}: LoadingSpinnerProps) {

  const spinner = (
    <svg
      className="spinner-svg"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="var(--orange)"
      strokeWidth="2.5"
      strokeLinecap="round"
    >
      <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
    </svg>
  );

  if (mode === 'inline') {
    return (
      <span className="spinner-inline">
        {spinner}
        {message && <span className="spinner-label">{message}</span>}
      </span>
    );
  }

  if (mode === 'overlay') {
    return (
      <div className="spinner-overlay">
        <div className="spinner-overlay-card">
          {spinner}
          <span className="spinner-overlay-msg">{message}</span>
        </div>
      </div>
    );
  }

  // block (default)
  return (
    <div className="spinner-block">
      {spinner}
      {message && <span className="spinner-block-msg">{message}</span>}
    </div>
  );
}
