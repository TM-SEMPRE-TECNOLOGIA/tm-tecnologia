# 🔄 FLUXO DE TRABALHO — TM Sempre Tecnologia
**Processos e Procedimentos Operacionais Padrão**
**Atualizado em:** 2026-05-27

---

## 1. FLUXO GERAL DE SESSÃO COM AGENTE IA

```
INÍCIO DE SESSÃO
      │
      ▼
1. Ler CONTEXTO_PROJETO.md
      │
      ▼
2. Ler _workspace/memoria/descobertas/ (últimas)
      │
      ▼
3. Verificar ROADMAP.md → o que está em andamento?
      │
      ▼
4. Consultar MAPA_AUTOMACOES.md → existe algo pronto?
      │
      ▼
5. Executar tarefa
      │
      ▼
6. Documentar descobertas em memoria/descobertas/
      │
      ▼
7. Atualizar ROADMAP.md se houver mudança de status
      │
      ▼
FIM DE SESSÃO
```

---

## 2. FLUXO: CRIAR UMA NOVA AUTOMAÇÃO

```
NOVA AUTOMAÇÃO SOLICITADA
      │
      ├─── Verificar em prompts/reutilizaveis/ e automacoes/
      │    └── Se existir: REUTILIZAR → ir para Execução
      │
      ▼
Não existe → Criar
      │
      ▼
1. Criar spec em docs/specs/YYYY-MM-DD-nome-automacao.md
   (use template: templates/relatorio/TEMPLATE_SPEC_AUTOMACAO.md)
      │
      ▼
2. Implementar script em scripts/python/ ou scripts/powershell/
   (com cabeçalho obrigatório: OBJETIVO, ENTRADA, SAÍDA, DEPENDÊNCIAS, RISCOS)
      │
      ▼
3. Testar com fixtures em testes/fixtures/
      │
      ▼
4. Registrar resultado em testes/resultados/
      │
      ▼
5. Se aprovado → mover para automacoes/
      │
      ▼
6. Atualizar MAPA_AUTOMACOES.md
```

---

## 3. FLUXO: GERAR RELATÓRIO PREVENTIVO (AutoRelatório V5)

```
RECEBER PASTA DE FOTOS
      │
      ▼
1. Identificar contrato (0908/1507/1565/2056/2057/2626/2627/3575/6122)
      │
      ▼
2. Verificar se pasta segue estrutura esperada
   └── Tradicional: - Área externa/ + - Área interna/ + subpastas
   └── SP2 (1565): faces, croquis, arquivos com "Faces 2"
      │
      ▼
3. Abrir AutoRelatório V5 (run.bat)
      │
      ▼
4. Step 1: Preencher formulário (nr_os, ag_cod, ag_nome, etc.)
      │
      ▼
5. Step 2: Associar blocos de fotos
      │
      ▼
6. Step 3: Revisar resumo → Gerar .docx
      │
      ▼
7. Verificar output em Documentos Preventivas/
```

---

## 4. FLUXO: ADICIONAR NOVO CONTRATO AO V5

```
NOVO CONTRATO RECEBIDO
      │
      ▼
1. Receber 3 materiais:
   ├── Planilha de Itens (→ items.json)
   ├── Planilha Padrão (→ referência de tabelas)
   └── Exemplo de Relatório Pronto (.docx de referência)
      │
      ▼
2. Criar pasta: backend/contracts/cXXXX/
   ├── engine/engine.py         (herda ContractEngine)
   ├── engine/scanner_*.py      (scan() → conteudo[])
   ├── engine/word_builder_*.py (build_word() → .docx)
   ├── items/items.json
   └── template/MODELO-XXXX.docx
      │
      ▼
3. Registrar engine em backend/core/registry.py
      │
      ▼
4. Criar fixture de teste em _workspace/testes/fixtures/cXXXX/
      │
      ▼
5. Criar spec em _workspace/docs/specs/contrato-XXXX.md
      │
      ▼
6. Testar: output V5 ≈ relatório de exemplo
      │
      ▼
7. Atualizar CONTEXTO_PROJETO.md e ROADMAP.md
```

---

## 5. FLUXO: DEBUGGING DE REGRESSÃO

```
COMPORTAMENTO INCORRETO DETECTADO
      │
      ▼
1. Registrar em logs/erros/YYYY-MM-DD_erro-descricao.md
      │
      ▼
2. Isolar: qual contrato? qual modo? qual etapa?
      │
      ▼
3. Reproduzir com fixture mínima em testes/fixtures/
      │
      ▼
4. Consultar memoria/heuristicas/ — existe padrão documentado?
      │
      ▼
5. Comparar com V4 (referência canônica em AutoRelatorio_V4/)
      │
      ▼
6. Aplicar correção
      │
      ▼
7. Testar snapshot: output igual ao esperado?
      │
      ▼
8. Documentar solução em memoria/descobertas/
      │
      ▼
9. Atualizar PADROES_TECNICOS.md se for regra nova
```

---

## 6. FLUXO: SCAN DE QUALIDADE DO PROJETO

```
SCAN PERIÓDICO (recomendado: a cada sprint)
      │
      ▼
1. Verificar duplicações em módulos Python
   └── usar skill: finding-duplicate-functions
      │
      ▼
2. Verificar divergências docs vs código
      │
      ▼
3. Verificar itens pendentes em ROADMAP.md
      │
      ▼
4. Registrar resultado em scans/resultados/YYYY-MM-DD_scan.md
      │
      ▼
5. Atualizar MEMORIA_OPERACIONAL.md com achados
```

---

## 7. PROCEDIMENTOS RECORRENTES

### 7.1 Início de Sprint
- [ ] Ler ROADMAP.md
- [ ] Verificar PENDENCIAS_V5.md
- [ ] Definir objetivo da sprint no ROADMAP.md
- [ ] Criar task no TODO

### 7.2 Fim de Sprint
- [ ] Atualizar status no ROADMAP.md
- [ ] Registrar descobertas em memoria/descobertas/
- [ ] Fazer snapshot do estado em snapshots/contratos/
- [ ] Atualizar VALIDACAO_FINAL_V5.md se aplicável

### 7.3 Entrega de Relatório ao Cliente
- [ ] Verificar se template está atualizado
- [ ] Rodar V5 com pasta de fotos real
- [ ] Conferir output vs padrão esperado
- [ ] Salvar cópia em Documentos Preventivas/

---

## 8. CONVENÇÕES DE NOMENCLATURA

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Spec de automação | `YYYY-MM-DD-nome.md` | `2026-05-27-upload-fotos.md` |
| Log de execução | `YYYY-MM-DD_HH-MM_acao.log` | `2026-05-27_14-30_gerar-docx.log` |
| Snapshot | `YYYY-MM-DD_cXXXX_estado.zip` | `2026-05-27_c0908_estado.zip` |
| Script Python | `snake_case.py` | `gerar_memorial.py` |
| Fixture de teste | `fixture_cXXXX_<descricao>/` | `fixture_c0908_basico/` |
| Descoberta | `YYYY-MM-DD-descricao.md` | `2026-05-27-sort-regra.md` |

---

*Para mais detalhes sobre padrões técnicos, consulte: `PADROES_TECNICOS.md`*
