# HEURÍSTICAS — AutoRelatório
**Regras práticas validadas em produção. Confiar sempre.**
**Atualizado em:** 2026-05-27

---

## H01 — Sort de fotos: nunca confiar no filesystem
> Windows e Linux ordenam arquivos de forma diferente. Python `os.listdir()` não garante ordem.
> **Sempre** usar a função `sort_key()` definida em PADROES_TECNICOS.md §1.4.

## H02 — Nunca inventar itens
> Zero texto genérico. Nenhum item fora de `items.json`.
> Se o item não existe no banco, parar e reportar ao operador.

## H03 — Portrait vs Landscape: detectar pelo pixel, não pelo nome
> Não assumir orientação pelo nome do arquivo. Usar Pillow para ler dimensões reais.
> `Image.open(path).size` → `(width, height)` → se width > height → landscape.

## H04 — Placeholders: case-sensitive e sem espaços
> `{{ag_cod}}` ≠ `{{AG_COD}}` ≠ `{{ ag_cod }}`.
> Verificar com python-docx se o placeholder está intacto no XML — às vezes o Word quebra o texto em múltiplos runs.
> Usar `fix_xml.py` para normalizar antes de processar.

## H05 — Fixture mínima antes de dados reais
> Sempre criar pasta com 2-3 fotos para testar o scanner antes de usar a pasta real do cliente.
> Economiza 90% do tempo de debug.

## H06 — V4 é referência, não standard
> O V4 tem bugs documentados. Ao portar para V5, implementar o comportamento CORRETO, não copiar o bug.
> Consultar MEMORIA_OPERACIONAL.md §1 para lista de bugs conhecidos.

## H07 — conteudo[] como debug primário
> Se o .docx gerado está errado, o primeiro lugar para debugar é o array `conteudo[]`.
> Imprimir conteudo[] após scan revela 80% dos problemas.

## H08 — Mudanças em core/ → testar TODOS os contratos
> Qualquer mudança em `backend/core/` afeta todos os 9 contratos.
> Antes de commitar, rodar fixtures de no mínimo c0908 (Tradicional/SP) e c1565 (SP2).

## H09 — Template Word limpo antes de inserir conteúdo
> O template .docx tem XML complexo. Usar `extract_placeholders()` para verificar
> que todos os placeholders foram encontrados antes de processar.

## H10 — Sprint incremental: um contrato de cada vez
> Não tentar portar todos os 9 contratos de uma vez.
> Portar um, testar exaustivamente, depois o próximo.
> Ordem recomendada: c2626 (mais simples) → c0908 (SP) → c1565 (SP2).
