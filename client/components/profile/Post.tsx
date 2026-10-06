"use client";

import { TabsContent } from "@/components/ui/tabs";
import { useGetMyPostsQuery } from "@/lib/redux/features/posts/postApiSlice";
import PostCard from "../cards/PostCard";
import Spinner from "@/components/shared/Spinner";

export default function Post() {
  const { data, isLoading, error } = useGetMyPostsQuery();

  // Unwrap the GenericJSONRenderer envelope
  // Response shape: { status_code, object_label, data: { count, results } }
  const posts = data?.data?.results ?? [];

  if (isLoading) {
    return (
      <TabsContent value="posts">
        <div className="flex justify-center p-8">
          <Spinner size="lg" />
        </div>
      </TabsContent>
    );
  }

  if (error) {
    return (
      <TabsContent value="posts">
        <div className="p-4">
          <p className="text-red-500">
            Could not load posts. Please try again later.
          </p>
        </div>
      </TabsContent>
    );
  }

  if (posts.length === 0) {
    return (
      <TabsContent value="posts">
        <div className="p-4">
          <p className="text-muted-foreground">
            You haven&apos;t created any posts yet.
          </p>
        </div>
      </TabsContent>
    );
  }

  return (
    <TabsContent value="posts">
      <div className="grid grid-cols-1 gap-4 p-4 md:grid-cols-2">
        {posts.map((post) => (
          <PostCard
            key={post.id}
            post={post}
          />
        ))}
      </div>
    </TabsContent>
  );
}