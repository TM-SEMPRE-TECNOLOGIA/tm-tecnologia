# PIPELINE: Geração de Relatório Fotográfico
**Pipeline completo do recebimento de fotos até o .docx final**
**Versão:** 1.0.0

---

## Diagrama do Pipeline

```
[PASTA DE FOTOS]
      │
      ▼
[ETAPA 1: VALIDAÇÃO]
  validate_folder() → erros e avisos
      │
      ├── Erros → PARAR + reportar ao operador
      └── OK → continuar
      │
      ▼
[ETAPA 2: SCAN]
  scan(root_path) → conteudo[]
      │
      ▼
[ETAPA 3: PREENCHIMENTO DE METADADOS]
  Formulário: nr_os, dt_atend, ag_cod, ag_nome, endereco, responsavel
      │
      ▼
[ETAPA 4: BUILD WORD]
  build_word(conteudo, meta) → .docx bytes
      │
      ▼
[ETAPA 5: DOWNLOAD]
  requestFile() → salvar .docx no computador
      │
      ▼
[ETAPA 6: REVISÃO MANUAL]
  Abrir .docx → verificar fotos, legendas, memorial
      │
      ├── Aprovado → entregar ao cliente
      └── Ajustes → registrar em logs/erros/ e iterar
```

## Configuração

```json
{
  "pipeline": "gerar-relatorio",
  "versao": "1.0.0",
  "etapas": [
    { "id": 1, "nome": "Validação", "endpoint": "/api/contracts/{id}/validate" },
    { "id": 2, "nome": "Scan", "endpoint": "/api/contracts/{id}/scan" },
    { "id": 3, "nome": "Metadados", "tipo": "formulario_manual" },
    { "id": 4, "nome": "Build Word", "endpoint": "/api/contracts/{id}/generate" },
    { "id": 5, "nome": "Download", "tipo": "blob_download" },
    { "id": 6, "nome": "Revisão", "tipo": "manual" }
  ]
}
```

## Pontos de Falha Conhecidos

| Etapa | Falha Comum | Solução |
|-------|-------------|---------|
| Scan | Pasta com estrutura errada | Usar fixture de exemplo como referência |
| Scan | Sort de fotos errado | Verificar RN-02 no scanner |
| Build | Placeholder não substituído | fix_xml.py no template |
| Build | Imagem com orientação errada | Usar Pillow exif_transpose |
| Download | .docx vazio | Sprint 3 não implementado — usar root_path local |
