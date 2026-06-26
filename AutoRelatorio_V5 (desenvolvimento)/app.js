// ─── DATA ─────────────────────────────────────────────────────────────────
const CONTRACTS = [
  { id:'0908', name:'São José dos Campos', short:'SJC',      mode:'sp',   uf:'SP' },
  { id:'1507', name:'Cuiabá',              short:'Cuiabá',   mode:'trad', uf:'MT' },
  { id:'1565', name:'SJRP / Ribeirão Preto',short:'SJRP',   mode:'sp2',  uf:'SP' },
  { id:'2056', name:'Divinópolis',         short:'Divin.',   mode:'trad', uf:'MG' },
  { id:'2057', name:'Varginha',            short:'Varginha', mode:'trad', uf:'MG' },
  { id:'2626', name:'Salinas',             short:'Salinas',  mode:'trad', uf:'MG' },
  { id:'2627', name:'Gov. Valadares',      short:'Valadares',mode:'trad', uf:'MG' },
  { id:'3575', name:'Tangará da Serra',    short:'Tangará',  mode:'trad', uf:'MT' },
  { id:'6122', name:'Mato Grosso do Sul',  short:'MS',       mode:'trad', uf:'MS' },
];

const DESCS = {
  '1': 'Informamos que foi realizada visita técnica à agência para fins de levantamento preventivo. A atividade contou com o acompanhamento do gerente [Nome do Gerente] – Matrícula [Número da Matrícula], que esteve presente durante todo o procedimento. Durante a vistoria, foram identificadas necessidades de intervenção nos seguintes itens.',
  '2': 'No cumprimento das atividades programadas, nosso técnico realizou uma visita à agência para a execução do levantamento preventivo. O gerente [Nome do Gerente] – Matrícula [Número da Matrícula] acompanhou todas as etapas do procedimento. Após a avaliação, verificou-se a necessidade de intervenção nos seguintes itens.',
  '3': 'Informamos que nosso técnico realizou uma visita à agência para a execução do levantamento preventivo. Durante a visita, o gerente [Nome do Gerente] – Matrícula [Número da Matrícula] esteve presente, acompanhando todo o procedimento.',
  '4': 'Nosso técnico realizou uma visita à agência para a execução do levantamento preventivo. O gerente [Nome do Gerente] – Matrícula [Número da Matrícula] acompanhou todo o processo.'
};

let currentContract = CONTRACTS[2]; // 1565 default
let currentStep = 2;
let zoomScale = 0.9;

// ─── RENDER CONTRACT LIST ─────────────────────────────────────────────────
function renderContractList() {
  const list = document.getElementById('contract-list');
  list.innerHTML = CONTRACTS.map(c => `
    <div class="c-item ${c.id === currentContract.id ? 'active' : ''}" onclick="selectContract('${c.id}')">
      <span class="c-id">${c.id}</span>
      <div class="c-info">
        <div class="c-name">${c.name}</div>
        <div class="c-mode">${c.mode.toUpperCase()} · ${c.uf}</div>
      </div>
      <div class="c-dot"></div>
    </div>
  `).join('');
}

function selectContract(id) {
  currentContract = CONTRACTS.find(c => c.id === id);
  renderContractList();
  updateTopbar();
  updatePreviewFilename();
  setStep(1);
}

function updateTopbar() {
  document.getElementById('top-cid').textContent = currentContract.id;
  document.getElementById('top-cname').textContent = currentContract.name;
  const mode = currentContract.mode;
  const modePill = document.getElementById('top-mode');
  const editorBadge = document.getElementById('editor-mode-badge');
  if (mode === 'sp2') {
    modePill.textContent = 'SP2';
    modePill.className = 'mode-pill mode-sp2';
    editorBadge.textContent = 'SP2';
    editorBadge.className = 'mode-pill mode-sp2';
  } else if (mode === 'sp') {
    modePill.textContent = 'SP';
    modePill.className = 'mode-pill mode-sp';
    editorBadge.textContent = 'SP';
    editorBadge.className = 'mode-pill mode-sp';
  } else {
    modePill.textContent = 'TRADICIONAL';
    modePill.className = 'mode-pill mode-trad';
    editorBadge.textContent = 'TRADICIONAL';
    editorBadge.className = 'mode-pill mode-trad';
  }
}

function updatePreviewFilename() {
  document.getElementById('preview-filename').textContent =
    `RELATÓRIO-${currentContract.id}-${currentContract.short.toUpperCase()}.docx`;
}

// ─── LIVE UPDATE ─────────────────────────────────────────────────────────
function val(id, fallback) {
  const el = document.getElementById(id);
  return el && el.value.trim() ? el.value.trim() : fallback;
}

function liveUpdate() {
  const fields = [
    ['f-nr-os',    'prev-nr-os',    '{{nr_os}}'],
    ['f-ag-cod',   'prev-ag-cod',   '{{ag_cod}}'],
    ['f-ag-nome',  'prev-ag-nome',  '{{ag_nome}}'],
    ['f-dt-atend', 'prev-dt-atend', '{{dt_atend}}'],
    ['f-endereco', 'prev-endereco', '{{endereco}}'],
    ['f-resp',     'prev-resp',     '{{responsavel_dependencia}}'],
  ];
  fields.forEach(([inputId, previewId, placeholder]) => {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    if (!input || !preview) return;
    const v = input.value.trim();
    if (v) {
      preview.textContent = v;
      preview.style.color = '#1A1A1A';
      preview.style.fontStyle = 'normal';
      preview.classList.add('flash');
      setTimeout(() => preview.classList.remove('flash'), 400);
    } else {
      preview.textContent = placeholder;
      preview.style.color = '#C8541C';
      preview.style.fontStyle = 'italic';
    }
  });
  // description
  const descSel = document.getElementById('f-desc');
  const descPrev = document.getElementById('prev-desc');
  if (descSel && descPrev) {
    descPrev.textContent = DESCS[descSel.value] || DESCS['1'];
  }
  // summary
  const os = val('f-nr-os', '—');
  const ag = val('f-ag-nome', '—') + (val('f-ag-cod','') ? ' — ' + val('f-ag-cod','') : '');
  document.getElementById('g-os').textContent = os;
  document.getElementById('g-agencia').textContent = ag;
}

// ─── STEPS ───────────────────────────────────────────────────────────────
function setStep(n) {
  currentStep = n;
  document.getElementById('step-1').style.display = n === 1 ? '' : 'none';
  document.getElementById('step-2').style.display = n === 2 ? '' : 'none';
  document.getElementById('step-3').style.display = n === 3 ? '' : 'none';

  [1,2,3].forEach(i => {
    const btn = document.getElementById('sb'+i);
    if (i < n) { btn.className = 'step-btn done'; btn.querySelector('.step-circle').textContent = '✓'; }
    else if (i === n) { btn.className = 'step-btn active'; btn.querySelector('.step-circle').textContent = i; }
    else { btn.className = 'step-btn'; btn.querySelector('.step-circle').textContent = i; }
  });

  const titles = ['Dados da OS', 'Estrutura de Blocos', 'Pronto para Gerar'];
  document.getElementById('editor-title').textContent = titles[n-1];
  document.getElementById('btn-prev').style.display = n > 1 ? '' : 'none';
  document.getElementById('btn-next').style.display = n < 3 ? '' : 'none';
  document.getElementById('btn-gen').style.display  = n === 3 ? '' : 'none';
  document.getElementById('footer-hint').textContent = `Passo ${n} de 3`;
}

function nextStep() { if (currentStep < 3) setStep(currentStep + 1); }
function prevStep() { if (currentStep > 1) setStep(currentStep - 1); }

// ─── ZOOM ─────────────────────────────────────────────────────────────────
function zoom(delta) {
  zoomScale = Math.min(1.5, Math.max(0.5, zoomScale + delta));
  const pages = document.querySelectorAll('.doc-page');
  pages.forEach(p => { p.style.transform = `scale(${zoomScale})`; p.style.transformOrigin = 'top center'; });
  document.getElementById('zoom-level').textContent = Math.round(zoomScale * 100) + '%';
}

// ─── GENERATE ─────────────────────────────────────────────────────────────
function generateReport() {
  const overlay = document.getElementById('progress-overlay');
  const bar = document.getElementById('prog-bar');
  const sub = document.getElementById('prog-sub');
  overlay.classList.add('show');
  let p = 0;
  const msgs = ['Substituindo placeholders...','Inserindo imagens...','Calculando memória de cálculo...','Gerando tabelas de itens...','Finalizando documento Word...'];
  let mi = 0;
  const iv = setInterval(() => {
    p = Math.min(p + Math.random() * 15 + 5, 100);
    bar.style.width = p + '%';
    if (mi < msgs.length && p > mi * 19) sub.textContent = msgs[mi++];
    if (p >= 100) {
      clearInterval(iv);
      setTimeout(() => {
        overlay.classList.remove('show');
        bar.style.width = '0%';
        showToast(`Relatório gerado: RELATÓRIO-${currentContract.id}.docx`);
      }, 500);
    }
  }, 160);
}

// ─── TOAST ────────────────────────────────────────────────────────────────
function showToast(msg) {
  const area = document.getElementById('toast-area');
  const t = document.createElement('div');
  t.className = 'toast';
  t.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--green)" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg><span>${msg}</span>`;
  area.appendChild(t);
  setTimeout(() => { t.style.opacity='0'; t.style.transition='opacity .3s'; setTimeout(()=>t.remove(),300); }, 3500);
}

// ─── RESIZABLE DIVIDER ────────────────────────────────────────────────────
const divider = document.getElementById('resizable-divider');
const editor = document.querySelector('.editor');
const app = document.querySelector('.app');

let isResizing = false;
let startX = 0;
let startWidth = 380;

divider.addEventListener('mousedown', (e) => {
  isResizing = true;
  startX = e.clientX;
  startWidth = editor.offsetWidth;
  divider.classList.add('active');
  document.body.style.cursor = 'col-resize';
  document.body.style.userSelect = 'none';
});

document.addEventListener('mousemove', (e) => {
  if (!isResizing) return;
  const delta = e.clientX - startX;
  const newWidth = Math.max(300, Math.min(startWidth + delta, app.offsetWidth - 300));
  editor.style.width = newWidth + 'px';
});

document.addEventListener('mouseup', () => {
  isResizing = false;
  divider.classList.remove('active');
  document.body.style.cursor = 'default';
  document.body.style.userSelect = 'auto';
});

// ─── NAV COLLAPSE ────────────────────────────────────────────────────
function toggleNavCollapse() {
  const nav = document.getElementById('nav');
  const toggle = document.getElementById('nav-toggle');
  nav.classList.toggle('collapsed');
  const isCollapsed = nav.classList.contains('collapsed');
  toggle.style.transform = isCollapsed ? 'scaleX(-1)' : '';
}

// ─── DARK MODE TOGGLE ────────────────────────────────
function toggleDarkMode() {
  const html = document.documentElement;
  const isDarkMode = html.classList.contains('light-mode');

  if (isDarkMode) {
    html.classList.remove('light-mode');
    localStorage.setItem('theme', 'dark');
  } else {
    html.classList.add('light-mode');
    localStorage.setItem('theme', 'light');
  }

  updateDarkModeIcon();
}

function updateDarkModeIcon() {
  const icon = document.getElementById('dark-mode-icon');
  const isDarkMode = !document.documentElement.classList.contains('light-mode');

  if (isDarkMode) {
    // Moon icon (showing that clicking will go to light mode)
    icon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>';
  } else {
    // Sun icon (showing that clicking will go to dark mode)
    icon.innerHTML = '<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>';
  }
}

function initDarkMode() {
  const savedTheme = localStorage.getItem('theme') || 'dark';
  const html = document.documentElement;

  if (savedTheme === 'light') {
    html.classList.add('light-mode');
  } else {
    html.classList.remove('light-mode');
  }

  updateDarkModeIcon();
}

// ─── SETTINGS ────────────────────────────────────────
function openSettings() {
  showToast('Painel de configurações em desenvolvimento...');
}

// ─── START BUTTON ─────────────────────────────────────
function iniciarApp() {
  alert(`
🚀 Para iniciar o AutoRelatorio V5:

1. Abra terminal na pasta do projeto:
   C:\\Users\\thiag\\Desktop\\tm-tecnologia\\AutoRelatorio_V5

2. Execute:
   run.bat

3. O servidor abrirá automaticamente no navegador!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Atalho: Double-click em 'run.bat'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  `);
}

// ─── INIT ─────────────────────────────────────────────────────────────────
initDarkMode();
renderContractList();
updateTopbar();
updatePreviewFilename();
setStep(2); // demo starts on step 2 (structure visible)
// Initial placeholder state
liveUpdate();
