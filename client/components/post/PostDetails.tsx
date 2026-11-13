"use client";

import { useSinglePost, useUpvotePost, useDownvotePost, useBookmarkPost } from '@/lib/query/use-posts';
import { getRepliesText, sortByDateDescending } from '@/utils';
import React from 'react';
import { toast } from 'react-toastify';
import { Card, CardContent, CardHeader } from '../ui/card';
import { AuthFormHeader } from '../shared/forms/auth';
import PostHeader from './PostHeader';
import PostActions from './PostActions';
import PostBody from './PostBody';
import PostFooter from './PostFooter';
import { MessageCircleMoreIcon } from 'lucide-react';
import RepliesList from './RepliesList';
import ProtectedRoute from '../shared/ProtectedRoutes';
import CreateReplyForm from '../forms/add-reply/CreateReplyForm';
import { Reply } from "@/types";

interface PostDetailProps {
  params: { slug: string };
}

function PostDetailsContent({ params }: PostDetailProps) {
  const slug = params.slug;
  const { data: post, isPending, isError } = useSinglePost(slug);

  const upvote = useUpvotePost();
  const downvote = useDownvotePost();
  const bookmark = useBookmarkPost();

  const sortedReplies: Reply[] = post?.replies ? sortByDateDescending(post.replies, "created_at") : [];

  const handleUpvote = () => {
    if (!post?.id) return;
    upvote.mutate(post.id);
    toast.success("Post Upvoted 😋");
  };
  const handleDownVote = () => {
    if (!post?.id) return;
    downvote.mutate(post.id);
    toast.success("Post Downvoted 🥺");
  };
  const handleBookmarkPost = () => {
    if (!post?.slug) return;
    bookmark.mutate({ postSlug: post.slug, bookmarked: !!post.is_bookmarked });
    toast.success(post.is_bookmarked ? "Bookmark removed" : "This post has been bookmarked");
  };

  if (isPending) return <p>Loading post...</p>;
  if (isError) return <p>Failed to load post</p>;
  if (!post) return <p>No post found.</p>;

  return (
    <Card className='dark:border-gray rounded-xl border border-dashed'>
      <AuthFormHeader title={post.title} linkText='Go back Home' linkHref='/welcome' />
      <CardHeader className='flex-start border-b-eerieBlack dark:border-gray w-full flex-col border-b border-dashed'>
        <div className='flex w-full flex-col justify-between sm:flex-row sm:items-center sm:gap-2'>
          <PostHeader
            title={post.title}
            avatar={post.avatar}
            author_username={post.author_username}
            created_at={post.created_at}
            view_count={post.view_count}
          />
          <PostActions
            upvotes={post.upvotes}
            downvotes={post.downvotes}
            handleUpvote={handleUpvote}
            handleDownVote={handleDownVote}
            handleBookmarkPost={handleBookmarkPost}
            isUpvoteLoading={upvote.isPending}
            isDownvoteLoading={downvote.isPending}
            isBookmarkLoading={bookmark.isPending}
          />
        </div>
      </CardHeader>
      <PostBody body={post.body} slug={post.slug} />
      <PostFooter tags={post.tags} replies_count={post.replies_count} />
      <div className='border-b-eerieBlack dark:border-gray dark:text-platinum ml-4 space-y-4 border-b border-dashed py-4'>
        <span className='font-robotoSlab dark:text-pumpkin flex flex-row items-center text-lg font-semibold'>
          <MessageCircleMoreIcon className='tab-icon text-electricIndigo mr-2' />
          {getRepliesText(post.replies_count)}
        </span>
        {sortedReplies && sortedReplies.length > 0 ? (
          sortedReplies.map((reply) => <RepliesList key={reply.id} reply={reply} />)
        ) : (
          <p className='text-lg'>This Post does not have any replies yet.</p>
        )}
      </div>
      <CardContent className='border-b-eerieBlack dark:border-gray dark:text-platinum border-b border-dashed'>
        <h2 className='h2-semibold dark:text-pumpkin mt-3'>Add your reply here</h2>
        <CreateReplyForm slug={post.slug} />
      </CardContent>
    </Card>
  );
}

export default function PostDetail({ params }: PostDetailProps) {
  return (
    <ProtectedRoute>
      <PostDetailsContent params={params} />
    </ProtectedRoute>
  );
}