// lib/api/auth.ts
import { apiGet, apiPost, apiPostWithConfig } from '@/lib/api/client';
import type {
  ActivateUserData,
  LoginResponse,
  LoginUserData,
  RegisterUserData,
  RegisterUserResponse,
  ResetPasswordConfirmData,
  ResetPasswordData,
  SocialAuthArgs,
  SocialAuthResponse,
  User,
} from '@/types';

export const authApi = {
  me: () => apiGet<User>('/auth/users/me/').then((u) => u ?? Promise.reject(new Error('no user'))),

  login: (body: LoginUserData) => apiPost<LoginResponse, LoginUserData>('/auth/login/', body),

  logout: () => apiPost<void>('/auth/logout/'),

  register: (body: RegisterUserData) =>
    apiPost<RegisterUserResponse, RegisterUserData>('/auth/users/', body),

  activate: (body: ActivateUserData) =>
    apiPost<void, ActivateUserData>('/auth/users/activation/', body),

  resetPasswordRequest: (body: ResetPasswordData) =>
    apiPost<void, ResetPasswordData>('/auth/users/reset_password/', body),

  resetPasswordConfirm: (body: ResetPasswordConfirmData) =>
    apiPost<void, ResetPasswordConfirmData>('/auth/users/reset_password_confirm/', body),

  socialAuth: ({ provider, state, code }: SocialAuthArgs) => {
    const url = `/auth/o/${provider}/?state=${encodeURIComponent(state)}&code=${encodeURIComponent(code)}`;
    return apiPostWithConfig<SocialAuthResponse>(
      url,
      new URLSearchParams(),
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } },
    );
  },
};