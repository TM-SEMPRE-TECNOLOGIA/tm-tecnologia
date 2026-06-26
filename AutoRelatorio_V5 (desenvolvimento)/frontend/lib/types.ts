import type { ContractMode } from './contracts';

export interface IContract {
  id: string;
  name: string;
  short: string;
  mode: ContractMode;
  uf: string;
}

export interface IFormData {
  nr_os: string;
  ag_cod: string;
  ag_nome: string;
  dt_atend: string;
  endereco: string;
  responsavel_dependencia: string;
  desc: '1' | '2' | '3' | '4';
}

export interface IPreviewData extends IFormData {
  contrato: string;
  uf: string;
  responsavel_tecnico: string;
}
