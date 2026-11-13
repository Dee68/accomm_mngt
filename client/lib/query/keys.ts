// lib/query/keys.ts
export const keys = {
  user: {
    all: ['user'] as const,
    lists: () => [...keys.user.all, 'list'] as const,
    list: (filters?: Record<string, unknown>) => [...keys.user.lists(), filters ?? {}] as const,
    me: () => [...keys.user.all, 'me'] as const,
    profile: () => [...keys.user.all, 'profile'] as const,
    details: () => [...keys.user.all, 'detail'] as const,
    detail: (id: string) => [...keys.user.details(), id] as const,
  },
  apartments: {
    all: ['apartments'] as const,
    lists: () => [...keys.apartments.all, 'list'] as const,
    list: (filters?: Record<string, unknown>) => [...keys.apartments.lists(), filters ?? {}] as const,
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
    list: (filters?: Record<string, unknown>) => [...keys.posts.lists(), filters ?? {}] as const,
    details: () => [...keys.posts.all, 'detail'] as const,
    detail: (slug: string) => [...keys.posts.details(), slug] as const,
    byTag: (tagSlug: string) => [...keys.posts.all, 'tag', tagSlug] as const,
    replies: (postId: string) => [...keys.posts.all, 'replies', postId] as const,
    bookmarks: () => [...keys.posts.all, 'bookmarks'] as const,
    top: () => [...keys.posts.all, 'top'] as const,
    popularTags: () => [...keys.posts.all, 'popularTags'] as const,
    mine: () => [...keys.posts.all, 'mine'] as const,
  },
  ratings: {
    all: ['ratings'] as const,
    lists: () => [...keys.ratings.all, 'list'] as const,
    list: (filters?: Record<string, unknown>) => [...keys.ratings.lists(), filters ?? {}] as const,
  },
  reports: {
    all: ['reports'] as const,
    lists: () => [...keys.reports.all, 'list'] as const,
    list: (filters?: Record<string, unknown>) => [...keys.reports.lists(), filters ?? {}] as const,
    detail: (id: string) => [...keys.reports.all, 'detail', id] as const,
  },
};