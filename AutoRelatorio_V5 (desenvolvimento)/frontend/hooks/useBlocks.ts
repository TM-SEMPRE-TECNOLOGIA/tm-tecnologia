'use client';

/**
 * useBlocks — Estado central dos blocos de conteúdo do Step 2.
 *
 * Um "bloco" representa uma foto detectada pelo seletor de pasta.
 * Cada bloco pode ter um item do contrato associado e medidas preenchidas.
 * O hook calcula os totais em tempo real e consolida os blocos por item
 * para renderização no preview.
 */

import { useState, useCallback, useMemo } from 'react';

// ─── Tipos ────────────────────────────────────────────────────────────────────

export type TipoUnidade = 'm²' | 'm³' | 'm' | 'un' | 'km' | 'verba' | string;

export interface ItemContrato {
  codigo:    string;
  descricao: string;
  unidade:   TipoUnidade;
}

export interface MedidasBloco {
  largura?:   number;   // m² e m³
  altura?:    number;   // m² e m³
  prof?:      number;   // m³
  comp?:      number;   // m
  faces?:     number;   // multiplicador (1 ou 2)
  desconto?:  number;   // m² subtraído
  quantidade?: number;  // un / verba / km
}

export interface Bloco {
  id:        string;          // uuid local
  arquivo:   File;            // objeto File do browser
  nome:      string;          // nome do arquivo sem extensão
  previewUrl: string;         // blob URL para <img>
  pasta:     string;          // caminho relativo da pasta
  numero:    string;          // número extraído do nome (ex: "01")
  item?:     ItemContrato;    // item selecionado
  medidas:   MedidasBloco;
  total:     number;          // calculado em tempo real
}

// Representa um item consolidado para o preview
export interface BlocoConsolidado {
  item:    ItemContrato;
  blocos:  Bloco[];
  total:   number;
  pasta:   string;           // pasta do serviço (nível folha)
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

let _idCounter = 0;
function uid() { return `bloco-${Date.now()}-${_idCounter++}`; }

/** Extrai o número sequencial do nome do arquivo (ex: "01 - 3,50 x 2,80.jpg" → "01") */
function extrairNumero(nome: string): string {
  const m = nome.match(/^(\d+)/);
  return m ? m[1] : '';
}

/** Calcula o total de medidas de acordo com a unidade do item */
export function calcularTotal(medidas: MedidasBloco, unidade: TipoUnidade): number {
  const { largura = 0, altura = 0, prof = 0, comp = 0,
          faces = 1, desconto = 0, quantidade = 0 } = medidas;

  const u = unidade.toLowerCase();

  if (u === 'm²' || u === 'm2') {
    return Math.max(0, parseFloat(((largura * altura * faces) - desconto).toFixed(4)));
  }
  if (u === 'm³' || u === 'm3') {
    return Math.max(0, parseFloat((largura * altura * prof * faces).toFixed(4)));
  }
  if (u === 'm' || u === 'km') {
    return Math.max(0, comp);
  }
  // un, verba, ou qualquer outra
  return Math.max(0, quantidade);
}

/** Agrupa blocos por pasta e item para o memorial de cálculo */
function consolidar(blocos: Bloco[]): BlocoConsolidado[] {
  const mapa = new Map<string, BlocoConsolidado>();

  for (const b of blocos) {
    if (!b.item) continue;
    const key = `${b.pasta}||${b.item.codigo}`;
    if (!mapa.has(key)) {
      mapa.set(key, { item: b.item, blocos: [], total: 0, pasta: b.pasta });
    }
    const grupo = mapa.get(key)!;
    grupo.blocos.push(b);
    grupo.total = parseFloat((grupo.total + b.total).toFixed(4));
  }

  return Array.from(mapa.values());
}

// ─── Hook ─────────────────────────────────────────────────────────────────────

export function useBlocks() {
  const [blocos, setBlocos] = useState<Bloco[]>([]);

  // Recebe File[] do <input webkitdirectory> e monta os blocos iniciais
  const carregarArquivos = useCallback((files: FileList | File[]) => {
    const arr = Array.from(files);
    const imagens = arr.filter(f =>
      /\.(jpe?g|png|webp)$/i.test(f.name)
    );

    // Revoga URLs anteriores para evitar vazamento de memória
    setBlocos(prev => {
      prev.forEach(b => URL.revokeObjectURL(b.previewUrl));
      return [];
    });

    const novos: Bloco[] = imagens.map(f => {
      // f.webkitRelativePath = "PastaRaiz/1 - Andar/1.1 - Servico/01 - 3,50 x 2,80.jpg"
      const partes = f.webkitRelativePath
        ? f.webkitRelativePath.split('/')
        : f.name.split('/');

      // Pasta é o penúltimo segmento do caminho
      const pasta = partes.length >= 2
        ? partes.slice(0, -1).join(' / ')
        : 'Raiz';

      const nomeSemExt = f.name.replace(/\.[^.]+$/, '');

      return {
        id:         uid(),
        arquivo:    f,
        nome:       nomeSemExt,
        previewUrl: URL.createObjectURL(f),
        pasta,
        numero:     extrairNumero(nomeSemExt),
        medidas:    { faces: 1 },
        total:      0,
      };
    });

    setBlocos(novos);
  }, []);

  // Associa um item a um bloco
  const setItem = useCallback((id: string, item: ItemContrato | undefined) => {
    setBlocos(prev => prev.map(b => {
      if (b.id !== id) return b;
      const medidas = { faces: 1 };  // reset medidas ao trocar item
      const total = item ? calcularTotal(medidas, item.unidade) : 0;
      return { ...b, item, medidas, total };
    }));
  }, []);

  // Atualiza uma medida de um bloco e recalcula o total
  const setMedida = useCallback((id: string, campo: keyof MedidasBloco, valor: number) => {
    setBlocos(prev => prev.map(b => {
      if (b.id !== id) return b;
      const medidas = { ...b.medidas, [campo]: valor };
      const total = b.item ? calcularTotal(medidas, b.item.unidade) : 0;
      return { ...b, medidas, total };
    }));
  }, []);

  // Remove um bloco
  const removerBloco = useCallback((id: string) => {
    setBlocos(prev => {
      const bloco = prev.find(b => b.id === id);
      if (bloco) URL.revokeObjectURL(bloco.previewUrl);
      return prev.filter(b => b.id !== id);
    });
  }, []);

  // Limpa tudo
  const limpar = useCallback(() => {
    setBlocos(prev => {
      prev.forEach(b => URL.revokeObjectURL(b.previewUrl));
      return [];
    });
  }, []);

  // Consolidado para preview (memoizado)
  const consolidado = useMemo(() => consolidar(blocos), [blocos]);

  // Total geral de fotos com item associado
  const totalFotos    = blocos.length;
  const fotosComItem  = blocos.filter(b => b.item).length;
  const totalGeral    = consolidado.reduce((s, g) => s + g.total, 0);
  const prontoParaGerar = totalFotos > 0 && fotosComItem === totalFotos;

  return {
    blocos,
    consolidado,
    totalFotos,
    fotosComItem,
    totalGeral,
    prontoParaGerar,
    carregarArquivos,
    setItem,
    setMedida,
    removerBloco,
    limpar,
  };
}
