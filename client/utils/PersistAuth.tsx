// utils/PersistAuth.tsx
'use client';

import { useEffect } from 'react';
import { authApi } from '@/lib/api/auth';
import { useAuthStore } from '@/lib/stores/auth-store';
import { useQueryClient } from '@tanstack/react-query';

export default function PersistAuth() {
  const setAuth = useAuthStore((s) => s.setAuth);
  const setLogout = useAuthStore((s) => s.setLogout);
  const setHydrated = useAuthStore((s) => s.setHydrated);
  const qc = useQueryClient();

  useEffect(() => {
    let mounted = true;

    authApi.me()
      .then((user) => {
        if (!mounted) return;
        console.log('[PersistAuth] SUCCESS! Setting Auth for:', user.email);
        setAuth(user);
        // Sync with TanStack cache for any component using useMe()
        qc.setQueryData(['user', 'me'], user);
      })
      .catch((error) => {
        if (!mounted) return;
        console.log('[PersistAuth] FAILED. Status:', error.response?.status);
        console.log('[PersistAuth] ERROR BODY:', error.response?.data);
        setLogout();
        qc.removeQueries({ queryKey: ['user', 'me'] });
      })
      .finally(() => {
        if (mounted) setHydrated();
      });

    return () => {
      mounted = false;
    };
  }, [setAuth, setLogout, setHydrated, qc]);

  return null;
}