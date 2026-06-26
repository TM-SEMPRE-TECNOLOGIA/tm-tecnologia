# SPEC: [Nome da Automação]
**Data:** YYYY-MM-DD  
**Versão:** 1.0.0  
**Autor:** TM Sempre Tecnologia  
**Status:** Proposta | Em Desenvolvimento | Aprovada | Depreciada

---

## Objetivo
[O que esta automação faz em 1-2 linhas]

## Problema que Resolve
[Qual dor ou ineficiência operacional esta automação endereça]

## Entrada
- **Tipo:** arquivo | pasta | API | manual | combinado
- **Formato:** xlsx | docx | json | imagens | ...
- **Exemplo:** `_workspace/testes/fixtures/exemplo_entrada/`
- **Obrigatório:** [campos/arquivos obrigatórios]
- **Opcional:** [campos/arquivos opcionais]

## Saída
- **Tipo:** arquivo | relatório | API response | log
- **Formato:** docx | xlsx | json | log | html
- **Localização:** [onde o arquivo é salvo]
- **Exemplo:** `_workspace/testes/fixtures/exemplo_saida/`

## Dependências
```
# Python
pip install [pacotes necessários]

# Arquivos
- [arquivo1]: [propósito]
- [arquivo2]: [propósito]

# APIs / Endpoints
- [endpoint]: [método] [para que serve]
```

## Riscos e Mitigações
| Risco | Probabilidade | Impacto | Mitigação |
|-------|:-------------:|:-------:|-----------|
| [Risco 1] | Alta/Média/Baixa | Alto/Médio/Baixo | [Como mitigar] |
| [Risco 2] | Alta/Média/Baixa | Alto/Médio/Baixo | [Como mitigar] |

## Como Executar
```bash
# Execução básica
python _workspace/scripts/python/nome_script.py \
  --input "./entrada" \
  --output "./saida"

# Com opções avançadas
python _workspace/scripts/python/nome_script.py \
  --input "./entrada" \
  --output "./saida" \
  --contrato 0908 \
  --debug
```

## Como Testar
```bash
# Usando fixture mínima
python _workspace/scripts/python/nome_script.py \
  --input "_workspace/testes/fixtures/fixture_XXXX/" \
  --output "_workspace/testes/resultados/"

# Verificar resultado
# [Descrever como validar manualmente o output]
```

## Critérios de Aprovação
- [ ] Output estruturalmente correto
- [ ] Sem erros em console/log
- [ ] Performance aceitável: < [N] segundos para [X] itens
- [ ] [Critério específico 1]
- [ ] [Critério específico 2]

## Impacto Arquitetural
[O que muda no sistema se esta automação for integrada em produção]
[Quais outros módulos são afetados]
[Necessidade de atualizar registry, specs, ou documentação]

## Contratos Afetados
- [ ] 0908 — São Paulo
- [ ] 1507 — Cuiabá
- [ ] 1565 — S.J.R.Preto / Ribeirão Preto (SP2)
- [ ] 2056 — Divinópolis
- [ ] 2057 — Varginha
- [ ] 2626 — Salinas
- [ ] 2627 — Gov. Valadares
- [ ] 3575 — Tangará da Serra
- [ ] 6122 — Mato Grosso do Sul

## Referências
- Spec relacionada: `_workspace/docs/specs/[nome].md`
- Automação similar: `MAPA_AUTOMACOES.md` → A[NN]
- Código de referência: `AutoRelatorio_V4/APP/backend/[arquivo].py`

## Histórico de Versões
| Data | Versão | Mudança | Autor |
|------|--------|---------|-------|
| YYYY-MM-DD | 1.0.0 | Criação | TM |
