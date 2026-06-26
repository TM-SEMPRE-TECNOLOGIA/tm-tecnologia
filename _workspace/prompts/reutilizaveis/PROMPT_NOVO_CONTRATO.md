# PROMPT: Migrar Contrato do V4 para V5
**Use ao adicionar ou migrar um contrato para o AutoRelatório V5**
**Versão:** 1.0.0 | Validado em: 2026-05-27

---

```
[COLE O BLOCO DE CONTEXTO BASE AQUI]

## TAREFA: MIGRAR CONTRATO [CÓDIGO] PARA V5

**Contrato:** [CÓDIGO] — [Região]
**Modo:** [Tradicional | SP | SP2]

### Materiais Disponíveis
- [ ] Planilha de Itens: [caminho ou "não disponível"]
- [ ] Planilha Padrão: [caminho ou "não disponível"]
- [ ] Exemplo de Relatório (.docx): [caminho ou "não disponível"]

### Referência no V4
- Generator: AutoRelatorio_V4/APP/backend/generator[_sp|_sp2].py
- Utils: AutoRelatorio_V4/APP/backend/utils_[sp|sp2].py
- Word Utils: AutoRelatorio_V4/APP/backend/word_utils[_sp|_sp2].py

### Estrutura a Criar no V5
```
AutoRelatorio_V5/backend/contracts/c[CÓDIGO]/
├── engine/
│   ├── __init__.py
│   ├── engine.py          ← herda ContractEngine
│   ├── scanner_*.py       ← scan(root_path) → conteudo[]
│   └── word_builder_*.py  ← build_word(conteudo, meta) → bytes
├── items/
│   └── items.json         ← banco de itens do contrato
└── template/
    └── MODELO-[CÓDIGO].docx  ← template Word com placeholders
```

### O Que Fazer
1. Analisar o exemplo de relatório .docx (se disponível)
2. Extrair regras de formatação específicas deste contrato
3. Criar engine.py herdando ContractEngine ABC
4. Criar scanner que retorna conteudo[] correto
5. Criar word_builder que gera .docx igual ao exemplo
6. Criar items.json a partir da planilha de itens
7. Registrar engine em backend/core/registry.py
8. Criar fixture de teste em _workspace/testes/fixtures/c[CÓDIGO]/
9. Criar spec em _workspace/docs/specs/contrato-[CÓDIGO].md

### Restrições
- RN-07: Este módulo deve ser 100% isolado (mudanças não afetam outros contratos)
- RN-08: Não altere core/ para acomodar este contrato
- Reutilize utils do core/ (word_utils.py, utils_sp.py) — não recrie
- Siga o padrão de sort (RN-02)
```
