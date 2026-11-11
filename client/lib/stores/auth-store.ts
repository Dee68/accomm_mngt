// lib/stores/auth-store.ts
import { create } from 'zustand';
import type { User } from '@/types';

type AuthState = {
  isAuthenticated: boolean;
  user: User | null;
  isHydrated: boolean;
  setAuth: (user: User) => void;
  setLogout: () => void;
  setHydrated: () => void;
  clear: () => void;
};

export const useAuthStore = create<AuthState>()((set) => ({
  isAuthenticated: false,
  user: null,
  isHydrated: false,
  setAuth: (user) => set({ isAuthenticated: true, user, isHydrated: true }),
  setLogout: () => set({ isAuthenticated: false, user: null, isHydrated: true }),
  setHydrated: () => set({ isHydrated: true }),
  clear: () => set({ isAuthenticated: false, user: null, isHydrated: true }),
}));

// Selectors — narrow, discrete. Zustand v5 re-renders only on the selected slice.
export const useIsAuthenticated = () => useAuthStore((s) => s.isAuthenticated);
export const useAuthUser = () => useAuthStore((s) => s.user);
export const useAuthHydrated = () => useAuthStore((s) => s.isHydrated);