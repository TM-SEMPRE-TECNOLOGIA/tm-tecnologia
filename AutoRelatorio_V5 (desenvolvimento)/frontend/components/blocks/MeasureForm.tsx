'use client';

/**
 * MeasureForm — Formulário adaptativo de medidas por unidade.
 *
 * m²  → Largura + Altura + Faces + Desconto
 * m³  → Largura + Altura + Profundidade + Faces
 * m   → Comprimento
 * km  → Comprimento
 * un/verba → Quantidade
 */

import { type MedidasBloco, type TipoUnidade } from '@/hooks/useBlocks';

interface MeasureFormProps {
  unidade:  TipoUnidade;
  medidas:  MedidasBloco;
  total:    number;
  onChange: (campo: keyof MedidasBloco, valor: number) => void;
}

function NumInput({
  label, value, onChange, placeholder = '0',
}: {
  label: string;
  value?: number;
  onChange: (v: number) => void;
  placeholder?: string;
}) {
  return (
    <div className="mf-field">
      <label className="mf-label">{label}</label>
      <input
        className="mf-input"
        type="number"
        step="0.01"
        min="0"
        placeholder={placeholder}
        value={value ?? ''}
        onChange={e => onChange(parseFloat(e.target.value) || 0)}
      />
    </div>
  );
}

export function MeasureForm({ unidade, medidas, total, onChange }: MeasureFormProps) {
  const u = unidade.toLowerCase();

  const isArea   = u === 'm²' || u === 'm2';
  const isVol    = u === 'm³' || u === 'm3';
  const isLinear = u === 'm' || u === 'km';
  const isUnit   = !isArea && !isVol && !isLinear;

  return (
    <div className="mf-root">
      {/* ── M² ───────────────────────────────────────────────────────────── */}
      {isArea && (
        <div className="mf-grid">
          <NumInput label="Larg (m)" value={medidas.largura} onChange={v => onChange('largura', v)} />
          <NumInput label="Alt (m)"  value={medidas.altura}  onChange={v => onChange('altura', v)} />
          <div className="mf-field">
            <label className="mf-label">Faces</label>
            <select
              className="mf-select"
              value={medidas.faces ?? 1}
              onChange={e => onChange('faces', parseInt(e.target.value))}
            >
              <option value={1}>1×</option>
              <option value={2}>2× (ambos os lados)</option>
            </select>
          </div>
          <NumInput label="Desconto (m²)" value={medidas.desconto} onChange={v => onChange('desconto', v)} placeholder="0" />
        </div>
      )}

      {/* ── M³ ───────────────────────────────────────────────────────────── */}
      {isVol && (
        <div className="mf-grid">
          <NumInput label="Larg (m)" value={medidas.largura} onChange={v => onChange('largura', v)} />
          <NumInput label="Alt (m)"  value={medidas.altura}  onChange={v => onChange('altura', v)} />
          <NumInput label="Prof (m)" value={medidas.prof}    onChange={v => onChange('prof', v)} />
          <div className="mf-field">
            <label className="mf-label">Faces</label>
            <select
              className="mf-select"
              value={medidas.faces ?? 1}
              onChange={e => onChange('faces', parseInt(e.target.value))}
            >
              <option value={1}>1×</option>
              <option value={2}>2×</option>
            </select>
          </div>
        </div>
      )}

      {/* ── M / KM ───────────────────────────────────────────────────────── */}
      {isLinear && (
        <div className="mf-grid mf-grid-1">
          <NumInput label={`Comprimento (${unidade})`} value={medidas.comp} onChange={v => onChange('comp', v)} />
        </div>
      )}

      {/* ── UN / VERBA ───────────────────────────────────────────────────── */}
      {isUnit && (
        <div className="mf-grid mf-grid-1">
          <NumInput label={`Quantidade (${unidade})`} value={medidas.quantidade} onChange={v => onChange('quantidade', v)} />
        </div>
      )}

      {/* ── Total ────────────────────────────────────────────────────────── */}
      <div className="mf-total">
        <span className="mf-total-label">TOTAL</span>
        <span className="mf-total-val">
          {total.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 4 })} {unidade}
        </span>
      </div>
    </div>
  );
}
