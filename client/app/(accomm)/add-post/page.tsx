import CreatePostForm from "@/components/forms/add-post/CreatePostForm";
import { AuthFormHeader } from "@/components/shared/forms/auth";
import type { Metadata } from "next";


export const metadata: Metadata = {
	title: "Accommodation Center | Create post",
	description: "Authenticated user can add a post",
};

export default function AddPostpage() {
  return (
    <div>
        <AuthFormHeader 
            title="Create a Post"
            staticText="Ask Questions, Share thoughts or information with everyone!" 
            linkHref="/welcome" 
            linkText="Back To HomePage"
        />
        <div className="mt-7 sm:mx-auto sm:w-full sm:max-w-[480px]">
            <div className="bg-lightGrey dark:bg-deepBlueGrey rounded-xl px-6 py-12 shadow sm:rounded-lg sm:px-12 md:rounded-3xl">
            <CreatePostForm />
            </div>
        </div>
      
    </div>
  )
}
