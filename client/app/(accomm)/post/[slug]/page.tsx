import PostDetails from '@/components/post/PostDetails';
import { Metadata } from 'next'
import React from 'react'

export const metadata: Metadata = {
    title: "Accommodation Center | Post Details",
    description: "Authenticated users can see the details of a post"

};


interface ParamsProps {
    params:{
        slug: string;
    };
};

export default function PostDetailPage({params}:ParamsProps) {
  return (
    <>
     <PostDetails params={params} /> 
    </>
  )
}
