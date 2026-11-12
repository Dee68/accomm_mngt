// lib/query/use-users.ts
'use client';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { usersApi } from '@/lib/api/users';
import { keys } from '@/lib/query/keys';
import type { ProfileData, QueryParams } from '@/types';

export function useAllUsers(params: QueryParams) {
  return useQuery({
    queryKey: keys.user.list({ ...params, kind: 'all' }),
    queryFn: () => usersApi.allUsers(params),
  });
}

export function useAllTechnicians(params: QueryParams) {
  return useQuery({
    queryKey: keys.user.list({ ...params, kind: 'technicians' }),
    queryFn: () => usersApi.allTechnicians(params),
  });
}

// NOTE: distinct key from useMe() — hits /profiles/user/my-profile/ (full profile),
// not /auth/users/me/ (auth user). Both are needed; they're different shapes.
export function useMyProfile() {
  return useQuery({
    queryKey: keys.user.profile(),
    queryFn: usersApi.myProfile,
    staleTime: 60_000,
  });
}

export function useUpdateProfile() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ProfileData) => usersApi.updateProfile(body),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: keys.user.all });
    },
  });
}

export function useUploadAvatar() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (formData: FormData) => usersApi.uploadAvatar(formData),
    onSuccess: () => {
      // RTK onQueryStarted waited 3s before invalidating — the endpoint returns
      // 202 Accepted and Celery does the Cloudinary upload. Preserve that here.
      setTimeout(() => {
        qc.invalidateQueries({ queryKey: keys.user.all });
      }, 3000);
    },
  });
}