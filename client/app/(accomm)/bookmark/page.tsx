import BookmarkedPostCard from '@/components/cards/BookmarkedPostCard'
import { Metadata } from 'next'
import React from 'react'

export const metadata: Metadata = {
    title:"Accommodation Center | Bookmarks",
    description: "Authenticated users can view the posts they have bookmarked"
}

export default function BookmarkedPostsPage() {
  return (
    <>
      <BookmarkedPostCard />
    </>
  )
}
