// lib/query/use-ratings.ts
'use client';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { ratingsApi } from '@/lib/api/ratings';
import { keys } from '@/lib/query/keys';
import type { RatingData } from '@/types';

export function useAddRating() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: RatingData) => ratingsApi.create(body),
    onSuccess: () => {
      // RTK invalidated ["Rating", "User"] — the User tag refreshes the
      // technician's average_rating shown in TechnicianCard
      qc.invalidateQueries({ queryKey: keys.ratings.all });
      qc.invalidateQueries({ queryKey: keys.user.all });
    },
  });
}