import {
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
} from "@/types";
import { baseApiSlice } from "../api/baseApiSlice";

export const postApiSlice = baseApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    createPost: builder.mutation<PostResponse["data"], PostData>({
      query: (postData) => ({
        url: "/posts/create/",
        method: "POST",
        body: postData,
      }),
      transformResponse: (response: PostResponse) => response.data,
      invalidatesTags: ["Post"],
    }),

    getAllPosts: builder.query<PostsResponse["data"], PostQueryParams>({
      query: (params = {}) => {
        const queryString = new URLSearchParams();
        if (params.page) {
          queryString.append("page", params.page.toString());
        }
        return `/posts/?${queryString.toString()}`;
      },
      transformResponse: (response: PostsResponse) => response.data,
      providesTags: ["Post"],
    }),

    getMyPosts: builder.query<MyPostsResponse["data"], void>({
      query: () => "/posts/my-posts/",
      transformResponse: (response: MyPostsResponse) => response.data,
      providesTags: ["Post"],
    }),

    getSinglePost: builder.query<PostResponse["data"], string>({
      query: (postSlug) => `/posts/${postSlug}/`,
      transformResponse: (response: PostResponse) => response.data,
      providesTags: ["Post"],
    }),

    updatePost: builder.mutation<PostResponse["data"], UpdatePostData>({
      query: ({ postSlug, ...postData }) => ({
        url: `/posts/${postSlug}/update/`,
        method: "PATCH",
        body: postData,
      }),
      transformResponse: (response: PostResponse) => response.data,
      invalidatesTags: ["Post"],
    }),

    upvotePost: builder.mutation<UpvoteDownvoteResponse, string>({
      query: (postId) => ({
        url: `/posts/${postId}/upvote/`,
        method: "PATCH",
      }),
      invalidatesTags: ["Post"],
    }),

    downvotePost: builder.mutation<UpvoteDownvoteResponse, string>({
      query: (postId) => ({
        url: `/posts/${postId}/downvote/`,
        method: "PATCH",
      }),
      invalidatesTags: ["Post"],
    }),

    bookmarkPost: builder.mutation<BookmarkResponse, string>({
      query: (postSlug) => ({
        url: `/posts/${postSlug}/bookmark/`,
        method: "PATCH",
      }),
      invalidatesTags: ["Post"],
    }),

    unBookmarkPost: builder.mutation<BookmarkResponse, string>({
      query: (postSlug) => ({
        url: `/posts/${postSlug}/unbookmark/`,
        method: "PATCH",
      }),
      invalidatesTags: ["Post"],
    }),

    getAllMyBookmarks: builder.query<BookmarkedPostsResponse["data"], void>({
      query: () => "/posts/bookmarked/posts/",
      transformResponse: (response: BookmarkedPostsResponse) => response.data,
      providesTags: ["Post"],
    }),

    getTopPosts: builder.query<TopPostsResponse["data"], void>({
      query: () => "/posts/top-posts/",
      transformResponse: (response: TopPostsResponse) => response.data,
      providesTags: ["Post"],
    }),

    getPopularTags: builder.query<PopularTagResponse["data"], void>({
      query: () => "/posts/popular-tags/",
      transformResponse: (response: PopularTagResponse) => response.data,
      providesTags: ["Post"],
    }),

    getAllReplies: builder.query<PostsByTagResponse["data"], string>({
      query: (postId) => `/posts/${postId}/replies/`,
      transformResponse: (response: PostsByTagResponse) => response.data,
      providesTags: ["Post"],
    }),

    getPostsByTag: builder.query<PostsByTagResponse["data"], string>({
      query: (tagSlug) => `/posts/tags/${tagSlug}/`,
      transformResponse: (response: PostsByTagResponse) => response.data,
      providesTags: ["Post"],
    }),

    replyToPost: builder.mutation<ReplyResponse["data"], ReplyPostData>({
      query: ({ postId, ...replyData }) => ({
        url: `/posts/${postId}/reply/`,
        method: "POST",
        body: replyData,
      }),
      transformResponse: (response: ReplyResponse) => response.data,
      invalidatesTags: ["Post"],
    }),
  }),
});

export const {
  useCreatePostMutation,
  useGetAllPostsQuery,
  useGetAllMyBookmarksQuery,
  useGetPostsByTagQuery,
  useGetPopularTagsQuery,
  useGetSinglePostQuery,
  useGetTopPostsQuery,
  useGetAllRepliesQuery,
  useGetMyPostsQuery,
  useBookmarkPostMutation,
  useDownvotePostMutation,
  useReplyToPostMutation,
  useUnBookmarkPostMutation,
  useUpdatePostMutation,
  useUpvotePostMutation,
} = postApiSlice;