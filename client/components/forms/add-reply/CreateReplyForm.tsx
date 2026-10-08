import { FormFieldComponent } from '@/components/shared/forms/FormFieldComponent';
import Spinner from '@/components/shared/Spinner';
import { Button } from '@/components/ui/button';
import { useGetSinglePostQuery, useReplyToPostMutation } from '@/lib/redux/features/posts/postApiSlice'
import { replyCreateSchema, TReplyCreateSchema } from '@/lib/validationSchemas';
import { extractErrorMessage } from '@/utils';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React from 'react'
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';

interface ReplyFormProps {
    slug:string | undefined;
    postId?: string;
};

export default function CreateReplyForm({slug}:ReplyFormProps) {
    const [replyToPost, {isLoading}] = useReplyToPostMutation();
    const { data } = useGetSinglePostQuery(slug || "");
    const post = data
    const postId = post?.id;
    const router = useRouter();

    const {register,handleSubmit,reset, formState:{errors},} = useForm<TReplyCreateSchema>({
        resolver:zodResolver(replyCreateSchema),
        mode:"all",
        defaultValues: {
            body:"",
        },
    });
    const onSubmit = async (values: TReplyCreateSchema) => {
        try {
            await replyToPost({postId, ...values}).unwrap();
            toast.success("Your reply was created");
            router.push(`/post/${slug}`);
            reset();
        } catch (error) {
            const errorMessage = extractErrorMessage(error);
            toast.error(errorMessage || "An error occurred");
        }
    };

  return (
    <main>
      <form noValidate onSubmit={handleSubmit(onSubmit)} className='flex w-full max-w-md flex-col gap-4'>
        <FormFieldComponent 
            name='body' 
            register={register} 
            errors={errors} 
            placeholder='Add your reply...' 
            isTextArea 
            className='font-semibold' 
        />
        <Button type='submit' disabled={isLoading} className='h4-semibold bg-eerieBlack dark:bg-pumpkin w-full text-white'>
            {isLoading ? <Spinner size='sm' /> : `Add your reply`}
        </Button>
      </form>
    </main>
  )
}
