'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { IFormData, IContract } from '@/lib/types';
import { DESCRIPTIONS } from '@/lib/descriptions';
import type { BlocoConsolidado } from '@/hooks/useBlocks';

interface PreviewPanelProps {
  formData:       IFormData;
  currentContract: IContract;
  consolidado:    BlocoConsolidado[];
}

export function PreviewPanel({ formData, currentContract, consolidado }: PreviewPanelProps) {
  const [zoomPercent, setZoomPercent] = useState(90);
  const viewportRef = useRef<HTMLDivElement>(null);

  const applyZoom = useCallback(() => {
    const vp = viewportRef.current;
    if (!vp) return;
    const available = vp.clientWidth - 40;
    const docWidth  = Math.max(320, Math.round(available * (zoomPercent / 100)));
    vp.style.setProperty('--doc-zoom-width', `${docWidth}px`);
  }, [zoomPercent]);

  useEffect(() => {
    applyZoom();
    const observer = new ResizeObserver(applyZoom);
    if (viewportRef.current) observer.observe(viewportRef.current);
    return () => observer.disconnect();
  }, [applyZoom]);

  const zoom = (delta: number) =>
    setZoomPercent(prev => Math.min(150, Math.max(40, prev + delta)));

  const getDescription = () => DESCRIPTIONS[formData.desc] || DESCRIPTIONS['1'];

  const formatDate = (dateStr: string) => {
    if (!dateStr) return '—';
    const [year, month, day] = dateStr.split('-');
    return `${day}/${month}/${year}`;
  };

  const getValue = (value: string, placeholder: string) => {
    if (!value || value.trim() === '') {
      return <span style={{ color: '#C8541C', fontStyle: 'italic' }}>{placeholder}</span>;
    }
    return <span style={{ color: '#1A1A1A' }}>{value}</span>;
  };

  const getFilename = () =>
    `RELATÓRIO-${currentContract.id}-${currentContract.short.toUpperCase()}.docx`;

  // Agrupa consolidado por pasta (seção/subseção)
  const secoes = consolidado.reduce<Map<string, BlocoConsolidado[]>>((map, g) => {
    if (!map.has(g.pasta)) map.set(g.pasta, []);
    map.get(g.pasta)!.push(g);
    return map;
  }, new Map());

  return (
    <section className="preview">
      <div className="preview-topbar">
        <span className="preview-label">Preview</span>
        <div className="preview-topbar" style={{ border: 'none', background: 'transparent', padding: '0', height: 'auto', gap: '6px' }}>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--shell-muted)" strokeWidth="1.75" strokeLinecap="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
          </svg>
          <span className="preview-filename">{getFilename()}</span>
        </div>
        <div className="preview-spacer"></div>
        <div className="preview-badge">DOCX LIVE</div>
        <div className="preview-zoom">
          <button className="zoom-btn" onClick={() => zoom(-10)}>−</button>
          <span>{zoomPercent}%</span>
          <button className="zoom-btn" onClick={() => zoom(10)}>+</button>
        </div>
      </div>

      <div className="preview-viewport" id="preview-viewport" ref={viewportRef}>
        <div className="doc-page-wrapper">
          <div className="doc-page">

            {/* ── Cabeçalho institucional ─────────────────────────────── */}
            <table className="doc-header-table">
              <tbody>
                <tr>
                  <td rowSpan={4} style={{ width: '70px', textAlign: 'center', padding: '6px' }}>
                    <div className="doc-logo-bb">BB</div>
                  </td>
                  <td rowSpan={4} style={{ textAlign: 'center', width: '140px' }}>
                    <div className="doc-rel-title">RELATÓRIO TÉCNICO<br />FOTOGRÁFICO</div>
                  </td>
                  <td style={{ width: '90px', background: '#F5F4F1' }}>
                    <span className="doc-field-label">Contrato:</span>
                  </td>
                  <td>
                    <span className="doc-field-val">2025.7421.{currentContract.id}</span>
                  </td>
                  <td rowSpan={4} style={{ width: '74px', textAlign: 'center', padding: '6px' }}>
                    <div className="doc-logo-maffeng">MAFF<br />ENG</div>
                  </td>
                </tr>
                <tr>
                  <td style={{ background: '#F5F4F1' }}>
                    <span className="doc-field-label">Nr. Ordem de Serviço:</span>
                  </td>
                  <td>
                    <span className="doc-field-val">{getValue(formData.nr_os, '{{nr_os}}')}</span>
                  </td>
                </tr>
                <tr>
                  <td style={{ background: '#F5F4F1' }}>
                    <span className="doc-field-label">Elaboração: Ygor A. Fernandes<br />Data de Elaboração:</span>
                  </td>
                  <td>
                    <span className="doc-field-val">{formatDate(formData.dt_atend)}</span>
                  </td>
                </tr>
                <tr>
                  <td colSpan={2} style={{ textAlign: 'center', background: '#F5F4F1' }}>
                    <span className="doc-field-label">Tipo: Preventivo</span>
                  </td>
                </tr>
                <tr>
                  <td colSpan={5} style={{ padding: '0' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                      <tbody>
                        <tr>
                          <td style={{ width: '80px', borderRight: '1px solid var(--doc-table-border)', padding: '4px 6px' }}>
                            <span className="doc-field-label">Agência:</span><br />
                            <span className="doc-field-val">{getValue(formData.ag_cod, '{{ag_cod}}')}</span>
                          </td>
                          <td style={{ padding: '4px 6px' }}>
                            <span className="doc-field-label">Nome:</span><br />
                            <span className="doc-field-val">{getValue(formData.ag_nome, '{{ag_nome}}')}</span>
                          </td>
                          <td style={{ width: '80px', borderLeft: '1px solid var(--doc-table-border)', padding: '4px 6px', textAlign: 'center' }}>
                            <span className="doc-field-label">UF:</span><br />
                            <span className="doc-field-val">{currentContract.uf}</span>
                          </td>
                          <td style={{ width: '120px', borderLeft: '1px solid var(--doc-table-border)', padding: '4px 6px' }}>
                            <span className="doc-field-label">Data Atendimento:</span><br />
                            <span className="doc-field-val">{getValue(formatDate(formData.dt_atend), '{{dt_atend}}')}</span>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>

            {/* ── Dados da dependência ────────────────────────────────── */}
            <div className="doc-dep-title">Dados da Dependência</div>
            <table className="doc-dep-table">
              <tbody>
                <tr><td><b>Endereço:</b> {getValue(formData.endereco, '{{endereco}}')}</td></tr>
                <tr><td><b>Responsável da Dependência:</b> {getValue(formData.responsavel_dependencia, '{{responsavel_dependencia}}')}</td></tr>
                <tr><td><b>Responsável Técnico:</b> Laura Mota</td></tr>
                <tr><td><b>Responsável Técnico/Empresa:</b> Ygor Augusto Fernandes Ferrugem – CREA: 1017279403/D-GO</td></tr>
              </tbody>
            </table>

            {/* ── Descrição do serviço ────────────────────────────────── */}
            <div className="doc-desc-block">{getDescription()}</div>

            {/* ── Blocos dinâmicos (tabelas de memória de cálculo) ────── */}
            {consolidado.length > 0 ? (
              Array.from(secoes.entries()).map(([pasta, grupos]) => (
                <div key={pasta}>
                  {/* Título da seção (pasta) */}
                  <div className="doc-heading1">{pasta}</div>

                  {grupos.map(grupo => (
                    <div key={`${pasta}||${grupo.item.codigo}`}>
                      {/* Enunciado do item */}
                      <div className="doc-enunciado">
                        Item {grupo.item.codigo} – {grupo.item.descricao}
                      </div>

                      {/* Fotos (thumbs) */}
                      {grupo.blocos.length > 0 && (
                        <div className="doc-photo-row">
                          {grupo.blocos.map(b => (
                            <div key={b.id} className="doc-photo-thumb-wrap">
                              {/* eslint-disable-next-line @next/next/no-img-element */}
                              <img
                                src={b.previewUrl}
                                alt={b.nome}
                                className="doc-photo-thumb"
                              />
                              <div className="doc-photo-thumb-label">{b.numero || b.nome}</div>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Tabela de memória de cálculo */}
                      <MemoriaCalculo grupo={grupo} />
                    </div>
                  ))}
                </div>
              ))
            ) : (
              /* Placeholder quando Step 2 ainda vazio */
              <div>
                <div className="doc-heading1">1 — 1º Andar – Espaço Desativado</div>
                <div className="doc-heading2">1.1 — Emassamento e pintura de teto</div>
                <div className="doc-photo-row">
                  <div className="doc-photo landscape">📷 01 — 16,20×4,63</div>
                  <div className="doc-photo landscape">📷 02 — vista</div>
                </div>
                <div className="doc-enunciado">Item 17.2 – Emassamento de parede interna ou teto com massa corrida a base de PVA com duas demãos</div>
                <table className="doc-mem-table">
                  <thead>
                    <tr>
                      <th>FOTO</th><th>COMP (m)</th><th>ALT (m)</th><th>DESCONTO (m²)</th><th>TOTAL (m²)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr><td>01</td><td>16,20</td><td>4,63</td><td>—</td><td>75,01</td></tr>
                    <tr><td>02</td><td>8,40</td><td>3,00</td><td>—</td><td>25,20</td></tr>
                    <tr className="total">
                      <td colSpan={4} style={{ textAlign: 'right' }}>TOTAL</td>
                      <td>100,21</td>
                    </tr>
                  </tbody>
                </table>
                <div className="doc-section-empty">
                  Selecione fotos no Step 2 para ver as tabelas reais aqui
                </div>
              </div>
            )}

            {/* ── Rodapé ──────────────────────────────────────────────── */}
            <div className="doc-footer">
              <span>AutoRelatório V5 · TM Sempre Tecnologia</span>
              <span>Pág. 1</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

// ─── Sub-componente: tabela de memória de cálculo ─────────────────────────────

function MemoriaCalculo({ grupo }: { grupo: BlocoConsolidado }) {
  const { item, blocos, total } = grupo;
  const u = item.unidade.toLowerCase();
  const isArea   = u === 'm²' || u === 'm2';
  const isVol    = u === 'm³' || u === 'm3';
  const isLinear = u === 'm' || u === 'km';

  const fmt = (n: number) =>
    n.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 4 });

  if (isArea) {
    return (
      <table className="doc-mem-table">
        <thead>
          <tr>
            <th>FOTO</th><th>LARG (m)</th><th>ALT (m)</th><th>FACES</th><th>DESCONTO (m²)</th><th>TOTAL (m²)</th>
          </tr>
        </thead>
        <tbody>
          {blocos.map(b => (
            <tr key={b.id}>
              <td>{b.numero || '—'}</td>
              <td>{fmt(b.medidas.largura ?? 0)}</td>
              <td>{fmt(b.medidas.altura  ?? 0)}</td>
              <td>{b.medidas.faces ?? 1}×</td>
              <td>{b.medidas.desconto ? fmt(b.medidas.desconto) : '—'}</td>
              <td>{fmt(b.total)}</td>
            </tr>
          ))}
          <tr className="total">
            <td colSpan={5} style={{ textAlign: 'right' }}>TOTAL</td>
            <td>{fmt(total)}</td>
          </tr>
        </tbody>
      </table>
    );
  }

  if (isVol) {
    return (
      <table className="doc-mem-table">
        <thead>
          <tr>
            <th>FOTO</th><th>LARG (m)</th><th>ALT (m)</th><th>PROF (m)</th><th>TOTAL (m³)</th>
          </tr>
        </thead>
        <tbody>
          {blocos.map(b => (
            <tr key={b.id}>
              <td>{b.numero || '—'}</td>
              <td>{fmt(b.medidas.largura ?? 0)}</td>
              <td>{fmt(b.medidas.altura  ?? 0)}</td>
              <td>{fmt(b.medidas.prof    ?? 0)}</td>
              <td>{fmt(b.total)}</td>
            </tr>
          ))}
          <tr className="total">
            <td colSpan={4} style={{ textAlign: 'right' }}>TOTAL</td>
            <td>{fmt(total)}</td>
          </tr>
        </tbody>
      </table>
    );
  }

  // Linear ou unitário — tabela simples
  return (
    <table className="doc-mem-table">
      <thead>
        <tr>
          <th>FOTO / REF</th>
          <th>{isLinear ? `COMP (${item.unidade})` : `QTD (${item.unidade})`}</th>
        </tr>
      </thead>
      <tbody>
        {blocos.map(b => (
          <tr key={b.id}>
            <td>{b.numero || b.nome}</td>
            <td>{fmt(b.total)}</td>
          </tr>
        ))}
        <tr className="total">
          <td style={{ textAlign: 'right' }}>TOTAL</td>
          <td>{fmt(total)}</td>
        </tr>
      </tbody>
    </table>
  );
}
