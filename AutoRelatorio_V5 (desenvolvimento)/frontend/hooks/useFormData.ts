'use client';

import { useState, useCallback } from 'react';
import type { IFormData } from '@/lib/types';

const initialData: IFormData = {
  nr_os: '',
  ag_cod: '',
  ag_nome: '',
  dt_atend: new Date().toISOString().split('T')[0],
  endereco: '',
  responsavel_dependencia: '',
  desc: '1',
};

export function useFormData() {
  const [formData, setFormData] = useState<IFormData>(initialData);

  const updateField = useCallback((field: keyof IFormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  }, []);

  const reset = useCallback(() => {
    setFormData(initialData);
  }, []);

  return {
    formData,
    updateField,
    reset,
  };
}
