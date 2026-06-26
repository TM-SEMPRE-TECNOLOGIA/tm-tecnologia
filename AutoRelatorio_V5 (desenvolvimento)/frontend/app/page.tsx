'use client';

import { useState, useCallback, useRef } from 'react';
import { TopBar }           from '@/components/TopBar';
import { Sidebar }          from '@/components/Sidebar';
import { EditorPanel }      from '@/components/EditorPanel';
import { PreviewPanel }     from '@/components/PreviewPanel';
import { ResizableDivider } from '@/components/ResizableDivider';
import { Toast }            from '@/components/Toast';
import type { ToastType }   from '@/components/Toast';
import { LoadingSpinner }   from '@/components/ui/LoadingSpinner';
import { useTheme }         from '@/hooks/useTheme';
import { useContracts }     from '@/hooks/useContracts';
import { useSteps }         from '@/hooks/useSteps';
import { useFormData }      from '@/hooks/useFormData';
import { useApiState }      from '@/hooks/useApiState';
import { useBlocks }        from '@/hooks/useBlocks';
import { generateReport, checkHealth } from '@/lib/api';
import type { GenerateResponse }       from '@/lib/api';

interface ToastState {
  message: string;
  type:    ToastType;
}

export default function Home() {
  // ─── TODOS OS HOOKS PRIMEIRO — nunca depois de um return condicional ──────
  const { mounted }                      = useTheme();
  const { currentContract }              = useContracts();
  const { currentStep, setStep }         = useSteps();
  const { formData, updateField, reset } = useFormData();
  const { state: genState, run: runGen } = useApiState<GenerateResponse>();
  const [toast, setToast]                = useState<ToastState | null>(null);

  // Blocos dinâmicos do Step 2
  const blocks = useBlocks();

  // Ref para ler o erro mais recente dentro de callbacks (evita stale closure)
  const genStateRef = useRef(genState);
  genStateRef.current = genState;

  // ─── Helpers de toast ────────────────────────────────────────────────────
  const showToast = useCallback((message: string, type: ToastType = 'info') => {
    setToast({ message, type });
  }, []);

  const closeToast = useCallback(() => setToast(null), []);

  // ─── Gerar relatório ─────────────────────────────────────────────────────
  const handleGenerate = useCallback(async () => {
    if (!formData.nr_os.trim()) {
      showToast('Preencha o Nº da OS antes de gerar.', 'error');
      setStep(1);
      return;
    }
    if (!formData.ag_cod.trim() || !formData.ag_nome.trim()) {
      showToast('Preencha o código e nome da agência.', 'error');
      setStep(1);
      return;
    }

    showToast('Gerando relatório...', 'loading');

    const result = await runGen(() =>
      generateReport({
        contrato_id: currentContract.id,
        nr_os:       formData.nr_os,
        ag_cod:      formData.ag_cod,
        ag_nome:     formData.ag_nome,
        dt_atend:    formData.dt_atend,
        endereco:    formData.endereco,
        responsavel: formData.responsavel_dependencia,
        desc_index:  formData.desc,
        modo:        currentContract.mode,
      })
    );

    closeToast();

    if (result?.ok) {
      showToast(`✓ ${result.filename} gerado com sucesso!`, 'success');
      if (result.url) {
        // Download automático via link temporário (evita bloqueio de popup)
        const a = document.createElement('a');
        a.href     = result.url;
        a.download = result.filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(() => URL.revokeObjectURL(result.url), 10_000);
      }
    } else if (!result) {
      showToast(genStateRef.current.error ?? 'Erro ao gerar relatório.', 'error');
    }
  }, [formData, currentContract, runGen, showToast, closeToast, setStep]);

  // ─── Verificar saúde do backend ──────────────────────────────────────────
  const handleStart = useCallback(async () => {
    showToast('Verificando conexão com o backend...', 'loading');
    try {
      const health = await checkHealth();
      closeToast();
      showToast(
        health.status === 'ok'
          ? `Backend OK — versão ${health.version}`
          : 'Backend degradado — verifique o servidor.',
        health.status === 'ok' ? 'success' : 'error',
      );
    } catch {
      closeToast();
      showToast('Backend offline. Inicie o servidor Python.', 'error');
    }
  }, [showToast, closeToast]);

  // ─── Novo relatório ──────────────────────────────────────────────────────
  const handleNew = useCallback(() => {
    reset();
    blocks.limpar();
    setStep(1);
    showToast('Formulário limpo. Novo relatório pronto.', 'info');
  }, [reset, blocks, setStep, showToast]);

  // ─── Guard de hidratação — SEMPRE após todos os hooks ────────────────────
  if (!mounted) return null;

  const isGenerating = genState.status === 'loading';

  // ─── Render ──────────────────────────────────────────────────────────────
  return (
    <div className="app-container">
      <TopBar
        onStartClick={handleStart}
        onNewClick={handleNew}
        onGenerateClick={handleGenerate}
        isGenerating={isGenerating}
      />

      <div className="app-layout">
        <Sidebar onSettingsClick={() => showToast('⚙️ Configurações em breve', 'info')} />

        <EditorPanel
          currentStep={currentStep}
          formData={formData}
          onUpdateField={updateField}
          onSetStep={setStep}
          currentContract={currentContract}
          onGenerate={handleGenerate}
          isGenerating={isGenerating}
          blocks={blocks}
        />

        <ResizableDivider />

        <PreviewPanel
          formData={formData}
          currentContract={currentContract}
          consolidado={blocks.consolidado}
        />
      </div>

      {isGenerating && (
        <LoadingSpinner
          mode="overlay"
          message="Gerando relatório .docx..."
          size={32}
        />
      )}

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={closeToast}
        />
      )}
    </div>
  );
}
