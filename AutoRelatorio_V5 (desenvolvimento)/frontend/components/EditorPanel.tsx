'use client';

import { IFormData, IContract } from '@/lib/types';
import { DESCRIPTIONS } from '@/lib/descriptions';
import { BlockList } from '@/components/blocks/BlockList';
import { useItems }  from '@/hooks/useItems';
import type { Bloco, ItemContrato } from '@/hooks/useBlocks';
import type { MedidasBloco } from '@/hooks/useBlocks';

// Interface explícita para evitar import do hook como valor
interface BlocksApi {
  blocos:          Bloco[];
  fotosComItem:    number;
  totalFotos:      number;
  totalGeral:      number;
  prontoParaGerar: boolean;
  carregarArquivos:(files: FileList | File[]) => void;
  setItem:         (id: string, item: ItemContrato | undefined) => void;
  setMedida:       (id: string, campo: keyof MedidasBloco, valor: number) => void;
  removerBloco:    (id: string) => void;
  limpar:          () => void;
}

interface EditorPanelProps {
  currentStep:    number;
  formData:       IFormData;
  onUpdateField:  (field: keyof IFormData, value: string) => void;
  onSetStep:      (step: number) => void;
  currentContract: IContract;
  onGenerate?:    () => void;
  isGenerating?:  boolean;
  blocks:         BlocksApi;
}

export function EditorPanel({
  currentStep,
  formData,
  onUpdateField,
  onSetStep,
  currentContract,
  onGenerate,
  isGenerating,
  blocks,
}: EditorPanelProps) {
  // Carrega os itens do contrato atual (do backend ou fallback vazio)
  const { items, loading: itemsLoading } = useItems(currentContract.id);

  const getStepTitle = (step: number) => {
    const titles = ['Dados da OS', 'Estrutura de Blocos', 'Pronto para Gerar'];
    return titles[step - 1];
  };

  const getModeLabel = (mode: string) => {
    const labels: Record<string, string> = {
      'trad': 'TRADICIONAL',
      'sp': 'SP',
      'sp2': 'SP2',
    };
    return labels[mode] || mode;
  };

  const handleDescChange = (value: string) => {
    onUpdateField('desc', value as '1' | '2' | '3' | '4');
  };

  const getTodayFormatted = () => {
    const now = new Date();
    const day   = String(now.getDate()).padStart(2, '0');
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const year  = now.getFullYear();
    return `${day}/${month}/${year}`;
  };

  // Step 2: pode avançar para step 3 mesmo sem fotos (geração só com cabeçalho)
  const step2Hint = blocks.totalFotos > 0
    ? `${blocks.fotosComItem}/${blocks.totalFotos} fotos prontas`
    : 'Selecione pasta (opcional)';

  return (
    <section className="editor">
      <div className="editor-topbar">
        <span className="editor-title">{getStepTitle(currentStep)}</span>
        <span className={`mode-pill mode-${currentContract.mode}`}>
          {getModeLabel(currentContract.mode)}
        </span>
      </div>

      <div className="steps-bar">
        <button
          className={`step-btn ${currentStep > 1 ? 'done' : currentStep === 1 ? 'active' : ''}`}
          onClick={() => onSetStep(1)}
        >
          <span className="step-circle">{currentStep > 1 ? '✓' : '1'}</span> Cabeçalho
        </button>
        <button
          className={`step-btn ${currentStep === 2 ? 'active' : currentStep > 2 ? 'done' : ''}`}
          onClick={() => onSetStep(2)}
        >
          <span className="step-circle">{currentStep > 2 ? '✓' : '2'}</span> Estrutura
        </button>
        <button
          className={`step-btn ${currentStep === 3 ? 'active' : currentStep > 3 ? 'done' : ''}`}
          onClick={() => onSetStep(3)}
        >
          <span className="step-circle">{currentStep > 3 ? '✓' : '3'}</span> Gerar
        </button>
      </div>

      <div className="editor-body">

        {/* ── STEP 1: CABEÇALHO ─────────────────────────────────────────── */}
        {currentStep === 1 && (
          <div>
            <div className="field-group">
              <div className="field-group-title">Ordem de Serviço</div>
              <div className="field-row half">
                <div>
                  <div className="f-label">
                    Nº da OS <span className="req">*</span> <span className="ph">{'{{nr_os}}'}</span>
                  </div>
                  <input
                    className="f-input"
                    type="text"
                    placeholder="ex: 1753"
                    value={formData.nr_os}
                    onChange={(e) => onUpdateField('nr_os', e.target.value)}
                  />
                </div>
                <div>
                  <div className="f-label">
                    Data Atendimento <span className="req">*</span> <span className="ph">{'{{dt_atend}}'}</span>
                  </div>
                  <input
                    className="f-input"
                    type="date"
                    value={formData.dt_atend}
                    onChange={(e) => onUpdateField('dt_atend', e.target.value)}
                  />
                </div>
              </div>
            </div>

            <div className="field-group">
              <div className="field-group-title">Agência</div>
              <div className="field-row half">
                <div>
                  <div className="f-label">
                    Código <span className="req">*</span> <span className="ph">{'{{ag_cod}}'}</span>
                  </div>
                  <input
                    className="f-input"
                    type="text"
                    placeholder="ex: 1234-5"
                    value={formData.ag_cod}
                    onChange={(e) => onUpdateField('ag_cod', e.target.value)}
                  />
                </div>
                <div>
                  <div className="f-label">
                    Nome <span className="req">*</span> <span className="ph">{'{{ag_nome}}'}</span>
                  </div>
                  <input
                    className="f-input"
                    type="text"
                    placeholder="ex: Ag. Centro"
                    value={formData.ag_nome}
                    onChange={(e) => onUpdateField('ag_nome', e.target.value)}
                  />
                </div>
              </div>
              <div className="field-row">
                <div className="f-label">
                  Endereço <span className="ph">{'{{endereco}}'}</span>
                </div>
                <input
                  className="f-input"
                  type="text"
                  placeholder="Rua das Flores, 100 — São José do Rio Preto/SP"
                  value={formData.endereco}
                  onChange={(e) => onUpdateField('endereco', e.target.value)}
                />
              </div>
              <div className="field-row">
                <div className="f-label">
                  Responsável <span className="ph">{'{{responsavel_dependencia}}'}</span>
                </div>
                <input
                  className="f-input"
                  type="text"
                  placeholder="Mat. 12345 — João Silva"
                  value={formData.responsavel_dependencia}
                  onChange={(e) => onUpdateField('responsavel_dependencia', e.target.value)}
                />
              </div>
            </div>

            <div className="field-group">
              <div className="field-group-title">Datas e Descrição</div>
              <div className="field-row">
                <div className="f-label">
                  Data Elaboração <span className="tag-auto">AUTO</span> <span className="ph">{'{{dt_elab}}'}</span>
                </div>
                <input
                  className="f-input auto"
                  type="text"
                  value={getTodayFormatted()}
                  readOnly
                />
              </div>
              <div className="field-row">
                <div className="f-label">
                  Descrição do Serviço <span className="ph">{'{Desc_here}'}</span>
                </div>
                <select
                  className="f-select"
                  value={formData.desc}
                  onChange={(e) => handleDescChange(e.target.value)}
                >
                  <option value="1">Desc 1 — Informamos que foi realizada visita técnica...</option>
                  <option value="2">Desc 2 — No cumprimento das atividades programadas...</option>
                  <option value="3">Desc 3 — Informamos que nosso técnico realizou...</option>
                  <option value="4">Desc 4 — Nosso técnico realizou uma visita...</option>
                </select>
              </div>
            </div>

            <div className="field-group" id="fixed-fields-group">
              <div className="field-group-title" style={{ color: 'var(--shell-subtle)' }}>
                Fixos no template
              </div>
              <div className="field-row half">
                <div>
                  <div className="f-label" style={{ color: 'var(--shell-subtle)' }}>Contrato</div>
                  <input className="f-fixed" value="2025.7421.1565" readOnly />
                </div>
                <div>
                  <div className="f-label" style={{ color: 'var(--shell-subtle)' }}>UF</div>
                  <input className="f-fixed" value={currentContract.uf} readOnly />
                </div>
              </div>
              <div className="field-row">
                <div className="f-label" style={{ color: 'var(--shell-subtle)' }}>
                  Resp. Técnico/Empresa
                </div>
                <input
                  className="f-fixed"
                  value="Ygor Augusto Fernandes Ferrugem — CREA: 1017279403/D-GO"
                  readOnly
                />
              </div>
            </div>
          </div>
        )}

        {/* ── STEP 2: ESTRUTURA DE BLOCOS ───────────────────────────────── */}
        {currentStep === 2 && (
          <BlockList
            blocos={blocks.blocos}
            items={items}
            itemsLoading={itemsLoading}
            fotosComItem={blocks.fotosComItem}
            onCarregar={blocks.carregarArquivos}
            onSetItem={blocks.setItem}
            onSetMedida={blocks.setMedida}
            onRemover={blocks.removerBloco}
            onLimpar={blocks.limpar}
          />
        )}

        {/* ── STEP 3: RESUMO / GERAR ────────────────────────────────────── */}
        {currentStep === 3 && (
          <div>
            <div style={{ fontFamily: 'var(--mono)', fontSize: '9px', fontWeight: '600', letterSpacing: '.12em', textTransform: 'uppercase', color: 'var(--shell-subtle)', marginBottom: '14px' }}>
              Resumo da Geração
            </div>
            <div className="gen-row">
              <span className="gen-key">Contrato</span>
              <span className="gen-val">{currentContract.id}</span>
            </div>
            <div className="gen-row">
              <span className="gen-key">Agência</span>
              <span className="gen-val" style={{ fontFamily: 'var(--sans)' }}>
                {formData.ag_nome ? `${formData.ag_nome} — ${formData.ag_cod}` : '—'}
              </span>
            </div>
            <div className="gen-row">
              <span className="gen-key">OS</span>
              <span className="gen-val">{formData.nr_os || '—'}</span>
            </div>
            <div className="gen-row">
              <span className="gen-key">Motor</span>
              <span className={`gen-val ${currentContract.mode === 'sp2' ? 'sp2' : ''}`}>
                {getModeLabel(currentContract.mode)}
              </span>
            </div>
            <div className="gen-row">
              <span className="gen-key">Fotos</span>
              <span className="gen-val">
                {blocks.totalFotos > 0
                  ? `${blocks.fotosComItem}/${blocks.totalFotos} com item`
                  : 'Sem fotos (só cabeçalho)'}
              </span>
            </div>
            {blocks.totalGeral > 0 && (
              <div className="gen-row">
                <span className="gen-key">Total medido</span>
                <span className="gen-val" style={{ color: '#7DB863' }}>
                  {blocks.totalGeral.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                </span>
              </div>
            )}
            {blocks.totalFotos > 0 && blocks.fotosComItem < blocks.totalFotos && (
              <div style={{ marginTop: 12, padding: '8px 10px', background: 'var(--orange-dim)', border: '1px solid var(--orange-border)', borderRadius: 'var(--r-md)', fontSize: 11, color: 'var(--orange)' }}>
                ⚠️ {blocks.totalFotos - blocks.fotosComItem} foto(s) sem item associado. O relatório será gerado sem essas fotos.
              </div>
            )}
          </div>
        )}
      </div>

      {/* ── Footer de navegação ───────────────────────────────────────── */}
      <div className="editor-footer">
        <button
          className="btn btn-ghost btn-sm"
          onClick={() => onSetStep(currentStep - 1)}
          style={{ display: currentStep > 1 ? 'flex' : 'none' }}
        >
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="15 18 9 12 15 6" />
          </svg>
          Voltar
        </button>
        <div className="footer-spacer"></div>
        <span className="footer-hint">
          {currentStep === 2 ? step2Hint : `Passo ${currentStep} de 3`}
        </span>
        <button
          className="btn btn-primary btn-sm"
          onClick={() => onSetStep(currentStep + 1)}
          style={{ display: currentStep < 3 ? 'flex' : 'none' }}
        >
          Próximo
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </button>
        <button
          className="btn btn-primary btn-sm"
          style={{ display: currentStep === 3 ? 'flex' : 'none' }}
          onClick={onGenerate}
          disabled={isGenerating}
        >
          {isGenerating ? (
            <>
              <svg className="spinner-svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
              </svg>
              Gerando...
            </>
          ) : (
            <>
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
              </svg>
              Gerar .docx
            </>
          )}
        </button>
      </div>
    </section>
  );
}
