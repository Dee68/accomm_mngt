// lib/query/keys.ts
// Mirrors tagTypes: ["User","Apartment","Issue","Report","Post","Rating"]
export const keys = {
  user: {
    all: ['user'] as const,
    me: () => [...keys.user.all, 'me'] as const,
    detail: (id: string) => [...keys.user.all, 'detail', id] as const,
  },
  apartments: {
    all: ['apartments'] as const,
    lists: () => [...keys.apartments.all, 'list'] as const,
    list: (filters?: Record<string, unknown>) =>
      [...keys.apartments.lists(), filters ?? {}] as const,
    details: () => [...keys.apartments.all, 'detail'] as const,
    detail: (id: string) => [...keys.apartments.details(), id] as const,
  },
  issues: {
    all: ['issues'] as const,
    lists: () => [...keys.issues.all, 'list'] as const,
    list: (scope: 'me' | 'assigned' = 'me', filters?: Record<string, unknown>) =>
      [...keys.issues.lists(), scope, filters ?? {}] as const,
    details: () => [...keys.issues.all, 'detail'] as const,
    detail: (id: string) => [...keys.issues.details(), id] as const,
  },
  posts: {
    all: ['posts'] as const,
    lists: () => [...keys.posts.all, 'list'] as const,
    list: (filters?: Record<string, unknown>) =>
      [...keys.posts.lists(), filters ?? {}] as const,
    details: () => [...keys.posts.all, 'detail'] as const,
    detail: (slug: string) => [...keys.posts.details(), slug] as const,
    bookmarks: () => [...keys.posts.all, 'bookmarks'] as const,
  },
  ratings: {
    all: ['ratings'] as const,
    lists: () => [...keys.ratings.all, 'list'] as const,
    list: (filters?: Record<string, unknown>) =>
      [...keys.ratings.lists(), filters ?? {}] as const,
  },
  reports: {
    all: ['reports'] as const,
    lists: () => [...keys.reports.all, 'list'] as const,
    list: (filters?: Record<string, unknown>) =>
      [...keys.reports.lists(), filters ?? {}] as const,
    detail: (id: string) => [...keys.reports.all, 'detail', id] as const,
  },
};