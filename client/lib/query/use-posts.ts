// lib/query/use-posts.ts
'use client';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { postsApi } from '@/lib/api/posts';
import { keys } from '@/lib/query/keys';
import type {
  PostData,
  PostQueryParams,
  Post,
  UpdatePostData,
  ReplyPostData,
} from '@/types';

// ── Queries ──

export function useAllPosts(params: PostQueryParams = {}) {
  return useQuery({
    queryKey: keys.posts.list({ page: params.page }),
    queryFn: () => postsApi.allPosts(params),
  });
}

export function useMyPosts() {
  return useQuery({
    queryKey: keys.posts.mine(),
    queryFn: postsApi.myPosts,
  });
}

export function useSinglePost(slug: string) {
  return useQuery({
    queryKey: keys.posts.detail(slug),
    queryFn: () => postsApi.singlePost(slug),
    enabled: !!slug,
  });
}

export function usePostsByTag(tagSlug: string) {
  return useQuery({
    queryKey: keys.posts.byTag(tagSlug),
    queryFn: () => postsApi.postsByTag(tagSlug),
    enabled: !!tagSlug,
  });
}

export function useReplies(postId: string) {
  return useQuery({
    queryKey: keys.posts.replies(postId),
    queryFn: () => postsApi.replies(postId),
    enabled: !!postId,
  });
}

export function useBookmarkedPosts() {
  return useQuery({
    queryKey: keys.posts.bookmarks(),
    queryFn: postsApi.bookmarkedPosts,
  });
}

export function useTopPosts() {
  return useQuery({
    queryKey: keys.posts.top(),
    queryFn: postsApi.topPosts,
  });
}

export function usePopularTags() {
  return useQuery({
    queryKey: keys.posts.popularTags(),
    queryFn: postsApi.popularTags,
  });
}

// ── Mutations (refetch) ──

export function useCreatePost() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: PostData) => postsApi.create(body),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.posts.all }),
  });
}

export function useUpdatePost() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: UpdatePostData) => postsApi.update(body),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.posts.all }),
  });
}

export function useReplyToPost() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ReplyPostData) => postsApi.reply(body),
    onSuccess: (_data, variables) => {
      if (!variables.postId) return;
      qc.invalidateQueries({ queryKey: keys.posts.detail(variables.postId) });
      qc.invalidateQueries({ queryKey: keys.posts.replies(variables.postId) });
    },
  });
}

// ── Mutations (optimistic) ──

export function useUpvotePost() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (postId: string) => postsApi.upvote(postId),
    onMutate: async (postId) => {
      await qc.cancelQueries({ queryKey: keys.posts.all });
      const snapshot = qc.getQueriesData<Post>({ queryKey: keys.posts.details() });
      qc.setQueriesData<Post>({ queryKey: keys.posts.details() }, (old) => {
        if (!old || old.id !== postId) return old;
        return {
          ...old,
          upvotes: old.is_upvoted ? old.upvotes : old.upvotes + 1,
          is_upvoted: true,
        };
      });
      return { snapshot };
    },
    onError: (_err, _postId, ctx) => {
      if (ctx?.snapshot) {
        ctx.snapshot.forEach(([key, data]) => qc.setQueryData(key, data));
      }
    },
    onSettled: () => {
      qc.invalidateQueries({ queryKey: keys.posts.all });
    },
  });
}

export function useDownvotePost() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (postId: string) => postsApi.downvote(postId),
    onMutate: async (postId) => {
      await qc.cancelQueries({ queryKey: keys.posts.all });
      const snapshot = qc.getQueriesData<Post>({ queryKey: keys.posts.details() });
      qc.setQueriesData<Post>({ queryKey: keys.posts.details() }, (old) => {
        if (!old || old.id !== postId) return old;
        return { ...old, downvotes: old.downvotes + 1 };
      });
      return { snapshot };
    },
    onError: (_err, _postId, ctx) => {
      if (ctx?.snapshot) {
        ctx.snapshot.forEach(([key, data]) => qc.setQueryData(key, data));
      }
    },
    onSettled: () => {
      qc.invalidateQueries({ queryKey: keys.posts.all });
    },
  });
}

export function useBookmarkPost() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ postSlug, bookmarked }: { postSlug: string; bookmarked: boolean }) =>
      bookmarked ? postsApi.unbookmark(postSlug) : postsApi.bookmark(postSlug),
    onMutate: async ({ postSlug, bookmarked }) => {
      await qc.cancelQueries({ queryKey: keys.posts.all });
      const snapshot = qc.getQueryData<Post>(keys.posts.detail(postSlug));
      if (snapshot) {
        qc.setQueryData<Post>(keys.posts.detail(postSlug), {
          ...snapshot,
          is_bookmarked: !bookmarked,
        });
      }
      return { snapshot };
    },
    onError: (_err, { postSlug }, ctx) => {
      if (ctx?.snapshot) {
        qc.setQueryData(keys.posts.detail(postSlug), ctx.snapshot);
      }
    },
    onSettled: () => {
      qc.invalidateQueries({ queryKey: keys.posts.all });
    },
  });
}