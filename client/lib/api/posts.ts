import { api, apiGet, apiPatch, apiPost } from '@/lib/api/client';
import type {
  BookmarkedPostsResponse,
  BookmarkResponse,
  MyPostsResponse,
  PopularTagResponse,
  PostData,
  PostQueryParams,
  PostResponse,
  PostsByTagResponse,
  PostsResponse,
  ReplyData,
  ReplyPostData,
  ReplyResponse,
  TopPostsResponse,
  UpdatePostData,
  UpvoteDownvoteResponse,
} from '@/types';

export const postsApi = {
  // Queries
  allPosts: (params: PostQueryParams = {}) =>
    apiGet<PostsResponse['data']>('/posts/', { page: params.page }),

  myPosts: () => apiGet<MyPostsResponse['data']>('/posts/my-posts/'),

  singlePost: (slug: string) => apiGet<PostResponse['data']>(`/posts/${slug}/`),

  postsByTag: (tagSlug: string) => apiGet<PostsByTagResponse['data']>(`/posts/tags/${tagSlug}/`),

  replies: (postId: string) => apiGet<PostsByTagResponse['data']>(`/posts/${postId}/replies/`),

  bookmarkedPosts: () => apiGet<BookmarkedPostsResponse['data']>('/posts/bookmarked/posts/'),

  topPosts: () => apiGet<TopPostsResponse['data']>('/posts/top-posts/'),

  popularTags: () => apiGet<PopularTagResponse['data']>('/posts/popular-tags/'),

  // Mutations
  create: (body: PostData) => apiPost<PostResponse['data'], PostData>('/posts/create/', body),

  update: ({ postSlug, ...body }: UpdatePostData) =>
    apiPatch<PostResponse['data']>(`/posts/${postSlug}/update/`, body),

  upvote: (postId: string) =>
    apiPatch<UpvoteDownvoteResponse>(`/posts/${postId}/upvote/`),

  downvote: (postId: string) =>
    apiPatch<UpvoteDownvoteResponse>(`/posts/${postId}/downvote/`),

  bookmark: (postSlug: string) =>
    apiPatch<BookmarkResponse>(`/posts/${postSlug}/bookmark/`),

  unbookmark: (postSlug: string) =>
    apiPatch<BookmarkResponse>(`/posts/${postSlug}/unbookmark/`),

  reply: ({ postId, ...body }: ReplyPostData) =>
    apiPost<ReplyResponse['data']>(`/posts/${postId}/reply/`, body),
};