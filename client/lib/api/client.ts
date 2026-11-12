// lib/api/client.ts
import axios, { AxiosError, AxiosRequestConfig, InternalAxiosRequestConfig } from 'axios';
import { Mutex } from 'async-mutex';

const mutex = new Mutex();

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  },
});

// ── Reauth interceptor — mirrors baseQueryWithReauth from baseApiSlice.ts ──
// Single-flight: when N concurrent requests get a 401, only one calls /auth/refresh/;
// the rest wait on the mutex, then retry. If refresh fails, clear the store.
api.interceptors.response.use(
  (res) => res,
  async (error: AxiosError) => {
    const original = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status !== 401 || original._retry) {
      return Promise.reject(error);
    }

    // Don't loop on the refresh endpoint itself.
    if (original.url?.includes('/auth/refresh/')) {
      const { useAuthStore } = await import('@/lib/stores/auth-store');
      useAuthStore.getState().clear();
      return Promise.reject(error);
    }

    await mutex.waitForUnlock();
    original._retry = true;

    if (!mutex.isLocked()) {
      const release = await mutex.acquire();
      try {
        await api.post('/auth/refresh/');
        return api(original);
      } catch (refreshErr) {
        const { useAuthStore } = await import('@/lib/stores/auth-store');
        useAuthStore.getState().clear();
        return Promise.reject(refreshErr);
      } finally {
        release();
      }
    }

    // Another request is already refreshing; wait, then retry.
    await mutex.waitForUnlock();
    return api(original);
  },
);

// Safely handles both { data: T } and flat T responses.
function unwrap<T>(data: any): T {
  if (data && typeof data === 'object' && 'data' in data) {
    return data.data as T;
  }
  return data as T;
}

export async function apiGet<T>(url: string, params?: Record<string, unknown>): Promise<T> {
  const { data } = await api.get(url, { params });
  return unwrap<T>(data);
}

export async function apiPost<T, B = unknown>(url: string, body?: B): Promise<T> {
  const { data } = await api.post(url, body);
  return unwrap<T>(data);
}

export async function apiPostWithConfig<T, B = unknown>(
  url: string,
  body: B | undefined,
  config: AxiosRequestConfig,
): Promise<T> {
  const { data } = await api.post(url, body, config);
  return unwrap<T>(data);
}

export async function apiPatch<T, B = unknown>(url: string, body?: B): Promise<T> {
  const { data } = await api.patch(url, body);
  return unwrap<T>(data);
}

export async function apiDelete<T>(url: string): Promise<T> {
  const { data } = await api.delete(url);
  return unwrap<T>(data);
}