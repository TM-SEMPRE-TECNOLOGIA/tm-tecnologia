# 🛡️ Guardião do Design System (TM-Testes-Design)
## Capacidades e Regras de Validação de UI/UX

Este documento descreve as capacidades de verificação automatizadas integradas no fluxo de testes do **AutoRelatório V5** (via ferramenta `tm-testes`). Essas validações garantem que a interface Next.js/React siga estritamente a identidade visual da **TM Sempre Tecnologia** e os padrões WCAG/responsividade.

---

### 1. 📐 Validação de TOKENS (Design System)
- **CSS Variables:** Verifica se todos os componentes utilizam variáveis semânticas do `globals.css` (como `--orange`, `--sans`, `--mono`, `--serif`, `--shell-bg`, `--shell-card`, `--shell-panel`, `--error`, `--r-sm`).
- **Inline Styles & Hardcoded Values:** Detecta e reporta o uso inadequado de estilos inline ou cores/fontes hardcoded diretamente no JSX (por exemplo, `style={{ color: '#C8541C' }}` ou botões sem classes de estilização padronizadas).

### 2. 🎨 Análise de CONTRASTE (WCAG 2.1)
- **Cálculo de Luminância:** Avalia a relação de contraste de cor entre o texto e seu plano de fundo (fórmula WCAG).
- **Garantia de Leitura:** 
  - Exige contraste mínimo de **4.5:1** para texto normal.
  - Exige contraste mínimo de **3.0:1** para texto grande (Large text).
  - Valida contrastes específicos como: text/bg, text/card, text/panel, muted/bg, orange/bg, e o contraste do texto de botões e estados light/dark.

### 3. ✏️ Validação de TIPOGRAFIA
- **Importação de Fontes:** Garante que as fontes do Google Fonts (`Inter`, `Roboto Slab`, `JetBrains Mono`) estão declaradas e carregadas corretamente no navegador.
- **Hierarquia:** Verifica se os elementos com texto mono usam `var(--mono)` / `JetBrains Mono` e se elementos gerais usam `var(--sans)` / `Inter`.
- **Aderência dos Componentes:** Sinaliza arquivos que deixam de usar tokens de tipografia (ex: `TopBar.tsx`, `Sidebar.tsx`).

### 4. 🧩 Consistência de COMPONENTES (A11y & Qualidade)
- **Alt Text em Imagens:** Garante que toda imagem (tag `<img>` ou `<Image>`) possua atributo `alt` descritivo.
- **Tipagem de Botões:** Exige que todos os botões (`<button>`) tenham a propriedade `type` explicitamente declarada (`type="button"`, `type="submit"`, etc.) para evitar comportamentos inesperados de formulários.
- **Estruturas de Listas:** Garante que loops `.map()` sempre retornem chaves (`key`) únicas e adequadas.
- **Verificação de Existência:** Confirma se os componentes principais do app (Sidebar, TopBar, EditorPanel, PreviewPanel, Toast, LoadingSpinner, etc.) estão instanciados no projeto.

### 5. 📸 Regressão VISUAL (Screenshots E2E)
- **Baseline Visual:** Captura e armazena imagens de referência (baselines) das páginas em diferentes resoluções.
- **Comparação de Pixels:** Compara o estado atual do layout com as baselines em resoluções padrão:
  - **Desktop:** 1440px de largura
  - **Laptop:** 1280px de largura
  - **Tablet:** 768px de largura

### 6. 📱 RESPONSIVIDADE
- **Overflow Horizontal:** Detecta se há quebras ou barras de rolagem horizontal indesejadas em resoluções de Desktop, Laptop e Tablet.
- **Visibilidade de Elementos-Chave:** Garante que componentes estruturais cruciais, como a `TopBar` e a `Sidebar`, permaneçam visíveis e operantes nas resoluções especificadas.

### 7. 🌙 Gerenciamento de TEMAS (Dark / Light)
- **Variáveis de Tema:** Valida se a cor de fundo (`--shell-bg`) altera de acordo com a seleção de tema (ex: `#111110` para dark mode e `#F8F7F4` para light mode).
- **Aplicação de Classes:** Garante que a alternância aplique a classe apropriada no elemento root (`<html>` ou `<body>`), como `.light-mode` ou `.dark-mode`.

### 8. ⌨️ ACESSIBILIDADE (Acessibilidade por Teclado)
- **Indicador de Foco:** Garante que todos os elementos interativos e focáveis (inputs, links, botões) apresentem um contorno (`outline`) ou indicador de foco visível ao navegar via teclado (`Tab`).

### 9. ⚡ Validação de PERFORMANCE
- **Cumulative Layout Shift (CLS):** Garante estabilidade visual (ideal abaixo de `0.1`).
- **First Contentful Paint (FCP):** Tempo do primeiro render de conteúdo (ideal abaixo de `1800ms`).
- **Time to Interactive (TTI):** Tempo até o app responder a cliques (ideal abaixo de `3000ms`).
