'use client';

/**
 * EmptyState — estado vazio com mensagem explicativa e CTA.
 * Guia o usuário para a próxima ação quando não há dados.
 */

interface EmptyStateProps {
  title?:      string;
  description?: string;
  actionLabel?: string;
  onAction?:   () => void;
  icon?:       React.ReactNode;
}

export function EmptyState({
  title       = 'Nenhum dado encontrado',
  description,
  actionLabel,
  onAction,
  icon,
}: EmptyStateProps) {
  return (
    <div className="empty-state">
      <div className="empty-state-icon">
        {icon ?? (
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="var(--shell-subtle)" strokeWidth="1.25" strokeLinecap="round">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
        )}
      </div>
      <p className="empty-state-title">{title}</p>
      {description && (
        <p className="empty-state-desc">{description}</p>
      )}
      {actionLabel && onAction && (
        <button className="btn btn-primary btn-sm" onClick={onAction}>
          {actionLabel}
        </button>
      )}
    </div>
  );
}
