'use client';

import { useState } from 'react';

export function useSteps() {
  const [currentStep, setStep] = useState(2); // Default: step 2

  const nextStep = () => {
    if (currentStep < 3) setStep(currentStep + 1);
  };

  const prevStep = () => {
    if (currentStep > 1) setStep(currentStep - 1);
  };

  return {
    currentStep,
    setStep,
    nextStep,
    prevStep,
  };
}
