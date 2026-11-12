// lib/api/users.ts
import { api, apiGet, apiPatch } from '@/lib/api/client';
import type {
  NonTenantResponse,
  ProfileData,
  ProfilesResponse,
  ProfileResponse,
  QueryParams,
} from '@/types';

export const usersApi = {
  allUsers: (params: QueryParams = {}) =>
    apiGet<ProfilesResponse['data']>('/profiles/all/', {
      page: params.page,
      search: params.searchTerm,
    }),

  allTechnicians: (params: QueryParams = {}) =>
    apiGet<NonTenantResponse['data']>('/profiles/non-tenant-profiles/', {
      page: params.page,
      search: params.searchTerm,
    }),

  myProfile: () => apiGet<ProfileResponse['data']>('/profiles/user/my-profile/'),

  updateProfile: (body: ProfileData) =>
    apiPatch<ProfileData>('/profiles/user/update/', body),

  uploadAvatar: async (formData: FormData) => {
    // Multipart — don't set Content-Type; axios/browser handles the boundary.
    const { data } = await api.patch<{ data: { message: string } }>(
      '/profiles/user/avatar/',
      formData,
    );
    return data.data;
  },
};