import PostTagCard from "@/components/cards/PostTagCard";
import { Metadata } from "next"

export const metadata: Metadata = {
    title:"Accommodation Centre | Post tags",
    description: "Authenticated users can see the tag details of a post"
}

interface SlugParamsProps {
    params:Promise<{
        tagSlug: string;
    }>;
}

export default async function TagPostsPage({params}: SlugParamsProps) {
  const resolvedParams = await params;
  return (
    <>
      <PostTagCard  params={resolvedParams}/>
    </>
  )
}
