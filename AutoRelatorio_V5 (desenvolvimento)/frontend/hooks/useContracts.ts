'use client';

// Zustand global store — garante que TopBar, Sidebar e EditorPanel
// compartilhem o mesmo contrato selecionado (fix: estado isolado por componente).
import { useContractStore } from '@/store/contractStore';

export function useContracts() {
  return useContractStore();
}
