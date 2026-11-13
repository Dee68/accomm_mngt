'use client';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apartmentsApi } from '@/lib/api/apartments';
import { keys } from '@/lib/query/keys';
import type { ApartmentData } from '@/types';

export function useMyApartment() {
  return useQuery({
    queryKey: keys.apartments.detail('me'),
    queryFn: apartmentsApi.myApartment,
    // The backend returns 404 when the user has no apartment yet.
    // That's a valid state, not an error — callers check `isError` to render "no apartment yet".
    retry: false,
  });
}

export function useCreateApartment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ApartmentData) => apartmentsApi.create(body),
    onSuccess: () => {
      // Refresh the apartment query + user profile (profile shows apartment building/floor)
      qc.invalidateQueries({ queryKey: keys.apartments.all });
      qc.invalidateQueries({ queryKey: keys.user.all });
    },
  });
}