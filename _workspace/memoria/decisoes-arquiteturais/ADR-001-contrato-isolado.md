# ADR-001: 1 Contrato = 1 Módulo Python Isolado
**Status:** Aprovada  
**Data:** 2026-05-20  
**Decisores:** Thiago Nascimento + Claude Code

---

## Contexto

No AutoRelatório V4, toda a lógica de todos os contratos estava em arquivos compartilhados (`generator.py`, `generator_sp.py`, `generator_sp2.py`). Uma mudança no comportamento de SP2 (c1565) podia quebrar o comportamento de contratos Tradicionais inadvertidamente.

## Decisão

No V5, cada contrato tem seu próprio módulo Python isolado em `backend/contracts/cXXXX/`. A interface é definida pela classe abstrata `ContractEngine` e cada engine implementa o comportamento específico do seu contrato.

## Consequências

**Positivas:**
- Mudança em c1565 não afeta c0908 ou qualquer outro contrato
- Cada engine pode ser testado independentemente
- Novos contratos podem ser adicionados sem modificar código existente
- Bugs ficam contidos no módulo do contrato afetado

**Negativas:**
- Alguma duplicação de código entre engines (aceito — clareza > DRY absoluto)
- Mais arquivos para navegar
- Exige disciplina para não colocar lógica específica de contrato no core/

## Regra Derivada

RN-07: 1 contrato = 1 módulo Python isolado  
RN-08: Nunca mudar core/ para acomodar um contrato específico

## Alternativas Rejeitadas

**A. Flag `tipo_relatorio` no generator** — rejeitada porque criava acoplamento implícito e o histórico do V4 mostrou que flags proliferam e se tornam ilegíveis.

**B. Herança simples sem ABC** — rejeitada porque sem ABC o compilador não garante que todos os métodos obrigatórios foram implementados.
