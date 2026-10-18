import React from 'react';
import { useAuth } from '../../context/AuthContext';

export const Toast = () => {
  const { toastMessage } = useAuth();

  if (!toastMessage) return null;

  return (
    <div
      role="status"
      aria-live="polite"
      className="fixed bottom-6 right-6 z-50 flex items-center gap-2 px-4 py-3 bg-primary text-on-primary rounded-xl shadow-2xl border border-secondary/20 transition-all duration-300 animate-bounce"
    >
      <span className="material-symbols-outlined text-secondary text-[20px]">verified</span>
      <span className="font-body-sm text-body-sm font-medium">{toastMessage}</span>
    </div>
  );
};

export default Toast;
