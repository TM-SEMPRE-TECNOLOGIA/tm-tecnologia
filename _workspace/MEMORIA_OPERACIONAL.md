# 🧠 MEMÓRIA OPERACIONAL — TM Sempre Tecnologia
**Inteligência acumulada, descobertas técnicas e heurísticas validadas**
**Atualizado em:** 2026-05-27

---

## 1. DESCOBERTAS TÉCNICAS CRÍTICAS

### D01 — Altura de imagem mudou entre V3 e V4
**Data:** 2026-05-26  
**Impacto:** Alto  
**Detalhe:** A altura padrão de imagem era 6cm no V3 e passou para **10cm** nos modos Tradicional e SP. O contrato **1565 (SP2) usa 7cm** por ter layout mais compacto com croquis e tabelas de faces.  
**Arquivo de referência:** `AutoRelatorio_V5/backend/core/word_utils.py` (ALTURA_PADRAO=10) e `word_utils_sp2.py` (ALTURA_PADRAO=7)

### D02 — Regra "Faces 2" no SP2
**Data:** 2026-05-26  
**Impacto:** Alto  
**Detalhe:** Quando o nome de arquivo contém "Faces 2", a área deve ser multiplicada por 2.  
**Exemplo:** arquivo `parede norte - 5,00 x 2,00 - Faces 2.jpg` → total = 10m² × 2 = 20m²  
**Arquivo de referência:** `AutoRelatorio_V4/APP/backend/utils_sp2.py`

### D03 — Contrato 1565 é o único SP2
**Data:** 2026-05-20  
**Impacto:** Alto  
**Detalhe:** O modo SP2 (croquis + faces + tabela de itens SP2) é exclusivo do contrato 1565 (São José do Rio Preto / Ribeirão Preto). Todos os outros são Tradicional ou SP.

### D04 — Módulo generator_app.py potencialmente incompleto
**Data:** 2026-05-26  
**Impacto:** Médio  
**Detalhe:** `generator_app.py` (modo pasta plana) no V4 pode estar incompleto. Verificar antes de portar para V5.  
**Ação:** Testar com fixture de pasta plana antes de usar como referência.

### D05 — FormularioDinamico vs FormularioDinamico_integration
**Data:** 2026-05-26  
**Impacto:** Médio  
**Detalhe:** No V4 existem dois componentes: `FormularioDinamico.tsx` e `FormularioDinamico_integration.tsx`. A diferença não foi documentada. Verificar antes de portar para V5.

### D06 — extrair_itens_docx.py (Legacy) — funcionalidade perdida
**Data:** 2026-05-26  
**Impacto:** Médio  
**Detalhe:** O script de extração de itens de .docx existente no Legacy nunca foi portado para V4 ou V5. Pode ser necessário recriar.

### D07 — Markup `<RED>` em utils_sp.py pode não estar aplicado
**Data:** 2026-05-26  
**Impacto:** Médio  
**Detalhe:** `utils_sp.py` tem markup `<RED>` para destacar itens, mas `word_utils_sp.py` no V4 pode não estar processando esse markup. Verificar.

---

## 2. DECISÕES ARQUITETURAIS

### DA01 — 1 Contrato = 1 Módulo Python Isolado
**Data:** 2026-05-20  
**Decisão:** Cada contrato tem sua própria pasta `contracts/cXXXX/` com engine, scanner e word_builder isolados.  
**Motivo:** No V4, mudanças em um contrato quebravam outros. Isolamento elimina regressões cruzadas.  
**Impacto:** Não mudar o core para acomodar um contrato específico.

### DA02 — conteudo[] como único contrato de dados
**Data:** 2026-05-20  
**Decisão:** O array `conteudo[]` é a única interface entre scanner e word_builder.  
**Motivo:** Desacopla a leitura de pasta da geração de Word. Permite trocar qualquer lado sem afetar o outro.

### DA03 — Store Zustand por contrato (não global)
**Data:** 2026-05-21  
**Decisão:** `useContractStore(id)` ao invés de store global misturado.  
**Motivo:** Estado global de V4 causava vazamento de dados entre contratos diferentes na mesma sessão.

### DA04 — Logo TM em base64 com glow laranja
**Data:** 2026-05-21  
**Decisão:** Logo embarcada em base64 no HTML/CSS, sem arquivo externo.  
**Motivo:** Elimina dependência de caminho de arquivo. Glow laranja pulsante como identidade visual.

### DA05 — API sem flag tipo_relatorio
**Data:** 2026-05-20  
**Decisão:** Endpoints `/api/contracts/{id}/scan|generate|validate|items` sem parâmetro `tipo_relatorio`.  
**Motivo:** O ID do contrato já determina o modo. Flags adicionais eram fonte de bugs no V4.

---

## 3. HEURÍSTICAS VALIDADAS

### H01 — Sort de fotos: ordem sempre preservada
> "Vista ampla" vem SEMPRE antes, depois numérico, depois alfabético, "Detalhes" SEMPRE por último.  
> Nunca confiar no sort do sistema de arquivos — Windows e Python têm comportamentos diferentes.

### H02 — Nunca inventar itens
> Nenhum item deve ser criado fora de `items.json`. Se item não existe no JSON, reportar ao operador.

### H03 — Portrait ≠ Landscape
> Fotos em landscape (largura > altura) ocupam linha inteira. Fotos portrait ficam em 2 colunas.  
> Detectar orientação pelo tamanho real da imagem, não pelo nome do arquivo.

### H04 — Placeholders Word: case-sensitive
> `{{ag_cod}}` ≠ `{{AG_COD}}`. Os placeholders no .docx devem ser EXATAMENTE iguais à lista oficial.

### H05 — Testar com fixture mínima primeiro
> Antes de testar com pasta de produção (centenas de fotos), sempre criar fixture mínima com 2-3 fotos.  
> Economiza tempo de debug e isola o problema.

### H06 — V4 é a referência, não o padrão final
> O V4 tem bugs conhecidos. Ao portar para V5, replicar o comportamento CORRETO, não o comportamento atual do V4.

---

## 4. WORKFLOWS VALIDADOS

### WF01 — Geração de Relatório Tradicional (V4)
1. Organizar pasta: `- Área externa/` + `- Área interna/` + `- Fachada.jpg`
2. Subpastas por seção numerada: `1 - Pintura automotiva/`, etc.
3. Dentro de cada seção: fotos de medida + `- Detalhes/`
4. Rodar generator com caminho da pasta
5. Conferir .docx gerado

### WF02 — Geração de Relatório SP2 (V4, contrato 1565)
1. Organizar pasta com faces: `Santa Adélia - Face N/`
2. Nomear fotos com medidas: `5,00 x 2,00 - Faces 2.jpg`
3. Incluir croquis na raiz
4. Rodar generator_sp2
5. Conferir tabela de faces e croquis no .docx

---

## 5. TROUBLESHOOTING FREQUENTE

### TS01 — .docx gerado com conteúdo só no cabeçalho
**Causa:** `root_path` não está sendo passado corretamente ao scanner.  
**Solução:** Verificar se `{{start_here}}` existe no template. Ver Sprint 3 — endpoint de upload.

### TS02 — Foto com orientação errada no Word
**Causa:** Orientação detectada pelo tamanho nominal, mas EXIF pode ter rotação aplicada.  
**Solução:** Usar Pillow `Image.open().rotate()` com `exif_transpose=True` antes de inserir.

### TS03 — Sort de fotos em ordem errada
**Causa:** Sort usando `os.listdir()` que respeita case do Windows.  
**Solução:** Usar função `sort_key()` de `PADROES_TECNICOS.md` §1.4.

### TS04 — Placeholder não substituído no Word
**Causa:** Placeholder no template tem espaços ou quebra de linha interna no XML.  
**Solução:** Usar `fix_xml.py` para normalizar o XML do .docx antes de processar.

### TS05 — engine.py de contrato não encontrado no registry
**Causa:** Import no `registry.py` faltando ou com caminho errado.  
**Solução:** Verificar `backend/core/registry.py` — todos os 9 contratos devem estar registrados.

---

## 6. HISTÓRICO DE AUTOMAÇÕES EXECUTADAS

| Data | Automação | Contrato | Resultado | Observações |
|------|-----------|----------|-----------|-------------|
| 2026-05-26 | Engenharia reversa V4 | Todos | ✅ Sucesso | Gerou ENGENHARIA_REVERSA_COMPLETA.html |
| 2026-05-21 | Criação dos 9 engines V5 | Todos | ✅ Sucesso | Scaffold + engines base criados |
| 2026-05-20 | Análise macro V4 | Todos | ✅ Sucesso | PRD MVP + Wireframe gerados |

---

*Adicionar novas entradas conforme descobertas forem feitas. Ver `FLUXO_DE_TRABALHO.md` §1.*
