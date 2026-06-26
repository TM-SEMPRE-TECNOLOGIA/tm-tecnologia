# PROMPT: Análise de [Domínio]
**Categoria:** Análise | Debug | Geração | Validação | Refatoração  
**Versão:** 1.0.0  
**Validado em:** YYYY-MM-DD  
**Skill relacionada:** [nome da skill, se houver]

---

## Contexto
```
Você está trabalhando no projeto AutoRelatório V5 da TM Sempre Tecnologia.
O sistema gera relatórios fotográficos preventivos (.docx) para 9 contratos 
bancários do Banco do Brasil.

Regras críticas:
- conteudo[] é o único contrato de dados entre scanner e word_builder
- Sort: Vista ampla → Numérico → Alfabético → Detalhes
- Altura padrão de imagem: 10cm (Tradicional/SP) | 7cm apenas c1565 (SP2)
- 1 contrato = 1 módulo Python isolado
- Contrato 1565 é o único SP2
```

## Instruções
```
[Cole as instruções específicas para este tipo de análise]

Ao analisar, sempre:
1. Identifique o contrato afetado
2. Verifique se viola alguma RN (RN-01 a RN-08)
3. Consulte o V4 como referência antes de propor mudança
4. Documente descobertas no formato TEMPLATE_DESCOBERTA.md
```

## Exemplo de Uso
```
Input de exemplo:
[Descrever ou colar exemplo de input]

Output esperado:
[Descrever o que o agente deve retornar]
```

## Variáveis a Customizar
- `[CONTRATO]` → código do contrato (0908, 1507, etc.)
- `[ARQUIVO]` → caminho do arquivo a analisar
- `[MODO]` → tradicional | sp | sp2

---

## Prompt Completo (copiar e usar)

```
Você está trabalhando no projeto AutoRelatório V5 da TM Sempre Tecnologia.

CONTEXTO:
[Cole o contexto relevante]

TAREFA:
[Descreva a tarefa específica]

RESTRIÇÕES:
- Não modifique arquivos de produção sem confirmação
- Siga as RNs documentadas em _workspace/PADROES_TECNICOS.md
- Reutilize código do V4 em AutoRelatorio_V4/APP/backend/
- Registre descobertas em _workspace/memoria/descobertas/

OUTPUT ESPERADO:
[Descreva o formato de saída]
```
