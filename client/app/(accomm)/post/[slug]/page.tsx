import PostDetails from '@/components/post/PostDetails';
import { Metadata } from 'next';
import React from 'react';

export const metadata: Metadata = {
  title: 'Accommodation Center | Post Details',
  description: 'Authenticated users can see the details of a post',
};

interface ParamsProps {
  params: Promise<{
    slug: string;
  }>;
}

export default async function PostDetailPage({ params }: ParamsProps) {
  const resolvedParams = await params;

  return <PostDetails params={resolvedParams} />;
}
