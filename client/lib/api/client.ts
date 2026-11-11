// lib/api/client.ts
import axios, { AxiosError, AxiosRequestConfig, InternalAxiosRequestConfig } from 'axios';
import { Mutex } from 'async-mutex';

const mutex = new Mutex();

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true,
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

// ── Typed helpers. All DRF responses are { data: … }; unwrap once here. ──
export async function apiGet<T>(url: string, params?: Record<string, unknown>): Promise<T> {
  const { data } = await api.get<{ data: T }>(url, { params });
  return data.data;
}

export async function apiPost<T, B = unknown>(url: string, body?: B): Promise<T> {
  const { data } = await api.post<{ data: T }>(url, body);
  return data.data;
}

// For endpoints needing custom headers (e.g. social auth → form-urlencoded).
export async function apiPostWithConfig<T, B = unknown>(
  url: string,
  body: B | undefined,
  config: AxiosRequestConfig,
): Promise<T> {
  const { data } = await api.post<{ data: T }>(url, body, config);
  return data.data;
}

export async function apiPatch<T, B = unknown>(url: string, body?: B): Promise<T> {
  const { data } = await api.patch<{ data: T }>(url, body);
  return data.data;
}

export async function apiDelete<T>(url: string): Promise<T> {
  const { data } = await api.delete<{ data: T }>(url);
  return data.data;
}