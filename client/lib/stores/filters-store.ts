// lib/stores/filters-store.ts
import { create } from 'zustand';

// ── userSlice replacement ──
// Original: { searchTerm: string, page: number }
// Consumers: PaginationSection (page), UsersSearch (searchTerm),
//            TenantCard / TechnicianCard (searchTerm, page)
type UserFiltersState = {
  searchTerm: string;
  page: number;
  setSearchTerm: (term: string) => void;
  setCurrentPage: (page: number) => void;
};

export const useUserFiltersStore = create<UserFiltersState>()((set) => ({
  searchTerm: '',
  page: 1,
  setSearchTerm: (searchTerm) => set({ searchTerm }),
  setCurrentPage: (page) => set({ page }),
}));

// ── postSlice replacement ──
// Original: { page: number }
// Consumers: PaginationSection (page), PostList (page)
type PostFiltersState = {
  page: number;
  setCurrentPage: (page: number) => void;
};

export const usePostFiltersStore = create<PostFiltersState>()((set) => ({
  page: 1,
  setCurrentPage: (page) => set({ page }),
}));