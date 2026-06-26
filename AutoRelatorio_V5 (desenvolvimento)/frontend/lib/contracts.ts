export const CONTRACTS = [
  { id: '0908', name: 'São José dos Campos', short: 'SJC', mode: 'sp' as const, uf: 'SP' },
  { id: '1507', name: 'Cuiabá', short: 'Cuiabá', mode: 'trad' as const, uf: 'MT' },
  { id: '1565', name: 'SJRP / Ribeirão Preto', short: 'SJRP', mode: 'sp2' as const, uf: 'SP' },
  { id: '2056', name: 'Divinópolis', short: 'Divin.', mode: 'trad' as const, uf: 'MG' },
  { id: '2057', name: 'Varginha', short: 'Varginha', mode: 'trad' as const, uf: 'MG' },
  { id: '2626', name: 'Salinas', short: 'Salinas', mode: 'trad' as const, uf: 'MG' },
  { id: '2627', name: 'Gov. Valadares', short: 'Valadares', mode: 'trad' as const, uf: 'MG' },
  { id: '3575', name: 'Tangará da Serra', short: 'Tangará', mode: 'trad' as const, uf: 'MT' },
  { id: '6122', name: 'Mato Grosso do Sul', short: 'MS', mode: 'trad' as const, uf: 'MS' },
];

export type ContractMode = 'sp2' | 'sp' | 'trad';

export interface IContract {
  id: string;
  name: string;
  short: string;
  mode: ContractMode;
  uf: string;
}
