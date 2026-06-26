-- Migração: adicionar campos elaborador e tecnico separados
-- Contexto: planilha TM tem "ELABORAÇÃO RELATÓRIO" (quem escreve) e "TÉCNICO" (quem executa)
-- O campo responsavel continua existindo como fallback/genérico

ALTER TABLE ordens_servico
  ADD COLUMN IF NOT EXISTS elaborador TEXT,
  ADD COLUMN IF NOT EXISTS tecnico    TEXT;

-- Popular elaborador e tecnico a partir de responsavel (para OS já importadas)
-- Opcional: só faça isso se a reimportação não for feita
-- UPDATE ordens_servico SET elaborador = responsavel WHERE elaborador IS NULL;
