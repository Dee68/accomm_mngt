// lib/query/use-auth.ts
'use client';

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { authApi } from '@/lib/api/auth'
import { keys } from '@/lib/query/keys';
import { useAuthStore } from '@/lib/stores/auth-store';
import type {
  ActivateUserData,
  LoginUserData,
  RegisterUserData,
  ResetPasswordConfirmData,
  ResetPasswordData,
} from '@/types';

// ── Query: current user ──
// Mirrors RTK's useGetUserQuery(). The store mirror happens in PersistAuth,
// NOT here — a query hook must not have side effects, or React Strict Mode
// (double-mount) will fire setAuth twice on every page.
export function useMe() {
  return useQuery({
    queryKey: keys.user.me(),
    queryFn: authApi.me,
    retry: false,          // don't retry 401 — the axios mutex handles reauth once
    staleTime: 5 * 60_000, // 5 min — matches RTK's default keepUnusedDataFor feel
  });
}

// ── Mutations ──
// Each mirrors the RTK endpoint's invalidatesTags behaviour:
//   - invalidatesTags: ["User"] → invalidate keys.user.all
//   - no invalidatesTags        → no invalidation

export function useLogin() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: LoginUserData) => authApi.login(body),
    onSuccess: async () => {
      // RTK did invalidatesTags: ["User"] → /me refetched. Mirror exactly.
      await qc.invalidateQueries({ queryKey: keys.user.all });
    },
  });
}

export function useLogout() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: authApi.logout,
    onSuccess: () => {
      // RTK did invalidatesTags: ["User"]. We do better: drop the cache entirely
      // (don't leave a stale /me for the next login to seed from) and clear the store.
      qc.cancelQueries({ queryKey: keys.user.all });
      qc.removeQueries({ queryKey: keys.user.all });
      useAuthStore.getState().setLogout();
    },
  });
}

export function useRegister() {
  return useMutation({ mutationFn: (body: RegisterUserData) => authApi.register(body) });
}

export function useActivate() {
  return useMutation({ mutationFn: (body: ActivateUserData) => authApi.activate(body) });
}

export function useResetPasswordRequest() {
  return useMutation({ mutationFn: (body: ResetPasswordData) => authApi.resetPasswordRequest(body) });
}

export function useResetPasswordConfirm() {
  return useMutation({ mutationFn: (body: ResetPasswordConfirmData) => authApi.resetPasswordConfirm(body) });
}

export function useSocialAuth() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: authApi.socialAuth,
    onSuccess: async () => {
      // Social auth returns a session cookie → /me is now valid. Refetch.
      await qc.invalidateQueries({ queryKey: keys.user.all });
    },
  });
}