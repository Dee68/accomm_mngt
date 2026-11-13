import { api } from '@/lib/api/client';
import type { ApartmentData, ApartmentResponse } from '@/types';

export const apartmentsApi = {
  // Returns the full ApartmentResponse envelope — consumers access .data.{...}
  create: async (body: ApartmentData): Promise<ApartmentResponse> => {
    const { data } = await api.post<ApartmentResponse>('/apartments/add/', body);
    return data;
  },

  myApartment: async (): Promise<ApartmentResponse> => {
    const { data } = await api.get<ApartmentResponse>('/apartments/my-apartment/');
    return data;
  },
};