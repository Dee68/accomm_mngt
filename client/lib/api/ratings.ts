// lib/api/ratings.ts
import { apiPost } from '@/lib/api/client';
import type { RatingData, RatingResponse } from '@/types';

export const ratingsApi = {
  create: (body: RatingData) =>
    apiPost<RatingResponse['data'], RatingData>('/ratings/create/', body),
};