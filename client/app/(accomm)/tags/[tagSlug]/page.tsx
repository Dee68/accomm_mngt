import PostTagCard from "@/components/cards/PostTagCard";
import { Metadata } from "next"

export const metadata: Metadata = {
    title:"Accommodation Center | Post tags",
    description: "Authenticated users can see the tag details of a post"
}

interface SlugParamsProps {
    params:{
        tagSlug: string;
    }
}

export default function TagPostsPage({params}: SlugParamsProps) {
  return (
    <>
      <PostTagCard  params={params}/>
    </>
  )
}
