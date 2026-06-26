import { create } from 'zustand';
import { CONTRACTS, type IContract } from '@/lib/contracts';

interface ContractState {
  currentContract: IContract;
  contracts: IContract[];
  selectContract: (id: string) => void;
}

export const useContractStore = create<ContractState>((set) => ({
  currentContract: CONTRACTS[2], // 1565 default
  contracts: CONTRACTS,
  selectContract: (id: string) => {
    const contract = CONTRACTS.find(c => c.id === id);
    if (contract) set({ currentContract: contract });
  },
}));
