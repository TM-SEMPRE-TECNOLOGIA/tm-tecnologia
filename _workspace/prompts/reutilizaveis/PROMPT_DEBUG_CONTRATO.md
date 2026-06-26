# PROMPT: Debug de Contrato Específico
**Use quando um contrato está gerando output incorreto**
**Versão:** 1.0.0 | Validado em: 2026-05-27

---

```
[COLE O BLOCO DE CONTEXTO BASE AQUI]

## TAREFA: DEBUG DO CONTRATO [CÓDIGO]

**Contrato:** [0908 | 1507 | 1565 | 2056 | 2057 | 2626 | 2627 | 3575 | 6122]
**Modo:** [Tradicional | SP | SP2]
**Problema:** [Descreva o comportamento incorreto observado]

### Comportamento Esperado
[O que deveria acontecer — baseado no V4 ou no relatório de exemplo]

### Comportamento Atual
[O que está acontecendo de errado]

### Arquivos Relevantes
- Engine: AutoRelatorio_V5/backend/contracts/c[CÓDIGO]/engine/engine.py
- Scanner: AutoRelatorio_V5/backend/contracts/c[CÓDIGO]/engine/scanner_*.py
- Builder: AutoRelatorio_V5/backend/contracts/c[CÓDIGO]/engine/word_builder_*.py
- Referência V4: AutoRelatorio_V4/APP/backend/generator*.py

### O Que Quero
1. Identifique a causa raiz do problema
2. Proponha correção mínima (não refatore além do necessário)
3. Indique como testar com fixture mínima
4. Registre descoberta em _workspace/memoria/descobertas/

### Restrições
- Não quebre outros contratos (mudança deve ser isolada no módulo c[CÓDIGO])
- Não altere core/ para acomodar este contrato específico (RN-08)
- Preserve o conteudo[] como único contrato de dados (RN-04)
```
