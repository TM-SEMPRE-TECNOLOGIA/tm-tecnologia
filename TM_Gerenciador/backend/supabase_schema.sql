-- TM Gerenciador — Schema Supabase
-- Execute no SQL Editor do Supabase dashboard

-- ── Tecnicos ──────────────────────────────────────────────
create table if not exists tecnicos (
  id            serial primary key,
  nome          text not null,
  email         text,
  especialidade text,
  ativo         boolean default true,
  created_at    timestamptz default now()
);

-- ── Ordens de Serviço ─────────────────────────────────────
create table if not exists ordens_servico (
  id              serial primary key,
  numero_os       text not null,
  titulo          text not null,
  descricao       text,
  status          text default 'aberta' check (status in ('aberta','em_andamento','concluida','atrasada','cancelada')),
  prioridade      text default 'media'  check (prioridade in ('baixa','media','alta','critica')),
  tipo            text default 'corretiva' check (tipo in ('corretiva','preventiva','preditiva','inspecao')),
  contrato_id     text not null,
  local           text,
  agencia         text,
  responsavel     text,
  tecnico_id      int references tecnicos(id),
  data_abertura   date,
  data_prazo      date,
  data_conclusao  date,
  observacoes     text,
  created_at      timestamptz default now(),
  updated_at      timestamptz default now()
);

-- trigger para updated_at
create or replace function update_updated_at()
returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end;
$$;

drop trigger if exists set_updated_at on ordens_servico;
create trigger set_updated_at
  before update on ordens_servico
  for each row execute function update_updated_at();

-- ── Notificacoes ──────────────────────────────────────────
create table if not exists notificacoes (
  id         serial primary key,
  titulo     text not null,
  mensagem   text not null,
  tipo       text default 'info' check (tipo in ('info','warning','error','success')),
  os_id      int references ordens_servico(id) on delete cascade,
  lida       boolean default false,
  created_at timestamptz default now()
);

-- ── Dificuldades ──────────────────────────────────────────
create table if not exists dificuldades (
  id          serial primary key,
  os_id       int not null references ordens_servico(id) on delete cascade,
  descricao   text not null,
  categoria   text,
  resolvida   boolean default false,
  created_at  timestamptz default now()
);

-- ── Indexes ───────────────────────────────────────────────
create index if not exists idx_os_contrato    on ordens_servico(contrato_id);
create index if not exists idx_os_status      on ordens_servico(status);
create index if not exists idx_os_prazo       on ordens_servico(data_prazo);
create index if not exists idx_notif_lida     on notificacoes(lida);

-- ── RLS (Row Level Security) ──────────────────────────────
-- Habilitar após configurar Supabase Auth
-- alter table ordens_servico enable row level security;
-- alter table notificacoes   enable row level security;
-- alter table tecnicos       enable row level security;
-- alter table dificuldades   enable row level security;
