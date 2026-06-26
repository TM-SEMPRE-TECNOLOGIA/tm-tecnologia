# 🤖 GUIA PARA AGENTES IA — TM Sempre Tecnologia
**Manual de operação para Claude Code e agentes autônomos**
**Atualizado em:** 2026-05-27

---

## 1. COMO COMEÇAR UMA SESSÃO

### Protocolo de Onboarding (OBRIGATÓRIO)

```
1. Ler este guia (GUIA_AGENTES_IA.md)
2. Ler CONTEXTO_PROJETO.md (quem somos, o que fazemos)
3. Ler ROADMAP.md (o que está em andamento)
4. Ler MEMORIA_OPERACIONAL.md seções relevantes
5. Perguntar ao operador: "Qual é o objetivo desta sessão?"
```

### Verificação de Saúde do Projeto

```powershell
# Verificar se V5 está rodando
Invoke-WebRequest http://localhost:5000/docs -UseBasicParsing | Select-Object StatusCode

# Verificar estrutura do workspace
Get-ChildItem "c:\Users\thiag\Desktop\tm-tecnologia\_workspace" | Select-Object Name
```

---

## 2. COMO INVESTIGAR O PROJETO

### Mapa de Navegação Rápida

**Ecossistema completo (3 pilares):**

| Pilar | O que encontrar | Caminho |
|-------|----------------|---------|
| 🏭 Produto | AutoRelatório V5 (backend + frontend) | `c:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V5\` |
| 🏭 Produto | Referência canônica V4 | `c:\Users\thiag\Desktop\tm-tecnologia\AutoRelatorio_V4\APP\backend\` |
| 🔧 Ferramentas | Skills Claude Code | `C:\Users\thiag\Desktop\TM-MEUS-APPS\Meus Plugins e Skills\` |
| 🔧 Ferramentas | Golden Apps em produção | `C:\Users\thiag\Desktop\TM-MEUS-APPS\01_Golden_Apps_meu_uso\` |
| 🔧 Ferramentas | Design System TM | `C:\Users\thiag\Desktop\TM-MEUS-APPS\TM Design System - NOVO Laranjado\` |
| 📋 Operação | Demandas em andamento | `C:\Users\thiag\Desktop\000 - Minha Demanda\2 - Em andamento\` |
| 📋 Operação | Preventivas 2026 | `C:\Users\thiag\Desktop\000 - Minha Demanda\1 - Preventivas 2026\` |
| 📋 Operação | Sala de controle | `C:\Users\thiag\Desktop\000 - Minha Demanda\0 - Sala de controle\` |

**Documentação do workspace:**

| O que investigar | Onde olhar |
|-----------------|-----------|
| Mapa do ecossistema | `_workspace/ECOSISTEMA_TM.md` |
| Arquitetura geral | `AutoRelatorio_V5/.context/ARQUITETURA_FINAL_V5.md` |
| Regras de negócio | `_workspace/CONTEXTO_PROJETO.md` + `PADROES_TECNICOS.md` |
| Estado atual | `_workspace/ROADMAP.md` + `AutoRelatorio_V5/PENDENCIAS_V5.md` |
| Bugs conhecidos | `_workspace/MEMORIA_OPERACIONAL.md` §5 (Troubleshooting) |
| Código de referência | `AutoRelatorio_V4/APP/backend/` |
| Código atual | `AutoRelatorio_V5/backend/` |
| Skills disponíveis | `C:\Users\thiag\Desktop\TM-MEUS-APPS\Meus Plugins e Skills\` |

### Ordem de Leitura de Código (para entender o fluxo completo)

```
1. backend/core/contract_engine.py   → interface ABC
2. backend/core/registry.py          → quais contratos existem
3. backend/contracts/c0908/engine/engine.py  → exemplo de implementação
4. backend/core/word_utils.py        → como o Word é gerado
5. backend/core/server.py            → endpoints FastAPI
6. frontend/app/                     → UI Next.js
7. frontend/lib/api.ts               → chamadas de API
```

---

## 3. COMO REGISTRAR DESCOBERTAS

### Formato Padrão

Criar arquivo em `_workspace/memoria/descobertas/YYYY-MM-DD-titulo.md`:

```markdown
# DESCOBERTA: [Título Curto]
**Data:** YYYY-MM-DD
**Sessão:** [Breve descrição do objetivo da sessão]
**Impacto:** Alto | Médio | Baixo
**Arquivo(s):** `caminho/arquivo.py:linha`

## O Que Foi Encontrado
[Descrição técnica objetiva]

## Por Que Importa
[Consequências se não tratado]

## Como Aplicar / Corrigir
[Ação recomendada]

## Referências Cruzadas
- Relacionado a: [D01, DA03, H02, etc. de MEMORIA_OPERACIONAL.md]
```

### Gatilhos para Registrar

- Comportamento não documentado encontrado no código
- Regra de negócio implícita descoberta
- Bug identificado mas não corrigido na sessão
- Decisão arquitetural tomada em sessão
- Padrão reutilizável identificado

---

## 4. COMO PROPOR MUDANÇAS

### Regra: Sempre Spec Antes de Código

```
NUNCA escrever código de produção sem antes:
1. Criar spec em _workspace/docs/specs/YYYY-MM-DD-nome.md
2. Discutir com operador
3. Receber aprovação explícita
```

### Template de Proposta de Mudança

```markdown
## PROPOSTA: [Título]
**Tipo:** Nova Feature | Bug Fix | Refatoração | Otimização
**Impacto:** [Quais arquivos serão afetados]
**Risco:** Alto | Médio | Baixo
**Reversível:** Sim | Não

### O que muda
[Descrição da mudança]

### Por que é necessário
[Justificativa técnica ou de negócio]

### Alternativas consideradas
1. [Alternativa A] — descartada porque [razão]
2. [Alternativa B] — descartada porque [razão]

### Plano de execução
1. [Passo 1]
2. [Passo 2]
3. [Teste: como validar]
```

---

## 5. COMO EVITAR REGRESSÕES

### Checklist Antes de Qualquer Mudança em Core

```
□ Li a spec do módulo que vou alterar?
□ Existe teste para o comportamento atual?
□ Se não, criei fixture de teste mínima?
□ A mudança afeta mais de um contrato?
□ Testei isoladamente com fixture antes de testar com dados reais?
□ O sort de fotos (RN-02) continua funcionando?
□ Os placeholders do Word continuam sendo substituídos?
□ conteudo[] mantém a estrutura esperada?
```

### Contratos de Alta Sensibilidade

| Contrato | Por que é sensível |
|----------|-------------------|
| 1565 | Único SP2 — lógica completamente diferente |
| 0908 | Memória de cálculo complexa — fórmulas frágeis |
| Qualquer | Mudança em `word_utils.py` afeta TODOS |

### Snapshots Antes de Mudanças Grandes

```powershell
# Antes de refatorar core — salvar snapshot
$data = Get-Date -Format "yyyy-MM-dd"
Compress-Archive -Path "AutoRelatorio_V5\backend\core\" `
  -DestinationPath "_workspace\snapshots\backups\$data-core-backup.zip"
```

---

## 6. COMO REUTILIZAR CÓDIGO EXISTENTE

### Funções Canônicas do V4 (referenciar antes de reimplementar)

| Função | Arquivo V4 | Propósito |
|--------|-----------|-----------|
| `parse_medidas_arquivo()` | `utils_sp.py` | Parser de medidas no nome do arquivo |
| `formatar_descricao_tecnica()` | `utils_sp.py` | Formata descrição de item |
| `parse_medidas_sp2()` | `utils_sp2.py` | Parser específico SP2 |
| `detectar_item_por_pasta()` | `utils_sp2.py` | Detecta item pelo nome da pasta |
| `e_croqui()` | `utils_sp2.py` | Verifica se arquivo é croqui |
| `extract_placeholders()` | `word_utils.py` | Extrai placeholders do .docx |
| `substitute_placeholders()` | `word_utils.py` | Substitui placeholders |
| `analisar_imagem()` | `word_utils.py` | Analisa orientação da imagem |
| `otimizar_layout()` | `word_utils.py` | Otimiza layout da tabela de fotos |

### Scripts das Skills (reuso direto)

```
Meus Plugins e Skills/relatorio-preventivo.skill/scripts/
├── parse_report.py          → parser de .docx
├── gerar_memorial.py        → gera memorial Word
├── fix_xml.py               → normaliza XML do .docx
├── verificar_divergencias.py → cross-check dados
├── extrair_itens.py         → extrai para Excel
└── verificar_legendas.py    → valida sequência de legendas
```

---

## 7. COMO VALIDAR AUTOMAÇÕES

### Pipeline de Validação

```
1. Criar fixture mínima (2-3 fotos)
   └── em: _workspace/testes/fixtures/

2. Rodar automação com fixture
   └── registrar saída em: _workspace/testes/resultados/

3. Comparar com saída esperada (snapshot)
   └── salvar em: _workspace/testes/snapshots/

4. Se aprovado → mover para automacoes/
   └── atualizar MAPA_AUTOMACOES.md

5. Se falhar → registrar em logs/erros/
   └── analisar causa-raiz
```

### Critérios de Aprovação

- [ ] Output estruturalmente igual ao exemplo de referência
- [ ] Sem erros em console/log
- [ ] Performance aceitável (< 30s para 100 fotos)
- [ ] Sort de fotos correto
- [ ] Placeholders todos substituídos
- [ ] Imagens corretamente inseridas (orientação, tamanho)

---

## 8. COMO TRABALHAR COM O AUTORELATÓRIO V5

### Regras de Ouro (RNs — NUNCA VIOLAR)

```
RN-01: Contrato 1565 = ÚNICO SP2
RN-02: Sort = Vista ampla → Numérico → Alfabético → Detalhes
RN-03: Altura imagem = 10cm (Tradicional e SP). 7cm exclusivo c1565 (SP2)
RN-04: conteudo[] = ÚNICO contrato de dados scanner↔builder
RN-05: "Faces 2" no nome = área × 2
RN-06: Placeholders fixos (8 no total, listados em PADROES_TECNICOS.md)
RN-07: 1 contrato = 1 módulo Python isolado
RN-08: Nunca mudar core para acomodar contrato específico
```

### Como Adicionar Um Novo Contrato

```
1. Criar pasta: backend/contracts/cXXXX/
2. Implementar engine.py (herda ContractEngine ABC)
3. Criar scanner_*.py: scan() → conteudo[]
4. Criar word_builder_*.py: build_word() → .docx
5. Criar items/items.json
6. Linkar template/MODELO-XXXX.docx
7. Registrar em backend/core/registry.py
8. Criar fixture de teste em _workspace/testes/fixtures/cXXXX/
9. Documentar spec em _workspace/docs/specs/contrato-XXXX.md
```

### Debug de Contrato Específico

```python
# Testar scanner isolado
from backend.contracts.c0908.engine.engine import C0908Engine

engine = C0908Engine()
conteudo = engine.scan("/caminho/para/pasta/de/fotos")
print(f"Itens no conteudo[]: {len(conteudo)}")
for item in conteudo[:5]:
    print(type(item), item if isinstance(item, str) else list(item.keys()))
```

---

## 9. COMO CONSUMIR AS SKILLS EXISTENTES

### Skills Claude Code Disponíveis

```
# Ativar skill de relatório preventivo
/relatorio-preventivo

# Ativar TM-Automatizando (SP2 completo)
/tm-automatizando

# Ativar testes Playwright
/tm-testes

# Ativar manipulação de DOCX
/docx-manipulation

# Ativar brainstorming antes de feature nova
/brainstorming
```

### Como Verificar se Skill Já Cobre o Caso

```
1. Ler _workspace/MAPA_AUTOMACOES.md — existe automação ativa?
2. Verificar Meus Plugins e Skills/ — existe .skill para o caso?
3. Se sim → usar skill existente
4. Se não → criar nova automação (seguir fluxo de criação)
```

---

## 10. INTEGRAÇÃO COM SISTEMAS EXTERNOS

### Playwright (tm-testes)
```javascript
// Configuração base
const config = {
  testDir: '_workspace/testes/',
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'on',
    trace: 'on-first-retry',
  }
}
```

### Claude API (para automações com Vision)
```python
import anthropic
client = anthropic.Anthropic()

# Análise de imagem para detectar tipo de item
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_b64}},
            {"type": "text", "text": "Identifique o tipo de serviço nesta foto de manutenção predial."}
        ]
    }]
)
```

---

## 11. PROTOCOLO DE ENCERRAMENTO DE SESSÃO

```
Antes de encerrar SEMPRE:
1. Atualizar ROADMAP.md com o que foi feito
2. Registrar descobertas em memoria/descobertas/
3. Verificar se há arquivos temporários para limpar
4. Confirmar que nenhum arquivo de produção foi modificado sem backup
5. Summarizar para o operador: O que foi feito | O que ficou pendente | Próximo passo
```

---

*Este guia é o ponto de entrada para qualquer agente IA que trabalhar neste projeto.*  
*Mantenha-o atualizado sempre que novas regras ou padrões forem estabelecidos.*
