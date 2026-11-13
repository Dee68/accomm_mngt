'use client';

import { useSinglePost, useUpdatePost } from '@/lib/query/use-posts';
import { postUpdateSchema, TPostUpdateSchema } from '@/lib/validationSchemas';
import { extractErrorMessage } from '@/utils';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';
import { z } from 'zod';
import { FormFieldComponent } from '../FormFieldComponents';
import { Text } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Spinner from '@/components/shared/Spinner';

interface UpdateParamsProps {
  params: {
    slug: string;
  };
}

export default function UpdatePostForm({ params }: UpdateParamsProps) {
  const postSlug = params.slug;
  const { data: post } = useSinglePost(postSlug || '');
  const updatePost = useUpdatePost();

  const router = useRouter();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<TPostUpdateSchema>({
    resolver: zodResolver(postUpdateSchema),
  });

  useEffect(() => {
    if (post) {
      reset({ ...post });
    }
  }, [post, reset]);

  const onSubmit = async (formValues: z.infer<typeof postUpdateSchema>) => {
    try {
      await updatePost.mutateAsync({ postSlug, ...formValues });
      toast.success('Post updated successfully');
      router.push(`/post/${postSlug}`);
    } catch (error) {
      toast.error(extractErrorMessage(error) || 'Failed to update post');
    }
  };

  return (
    <main>
      <form noValidate onSubmit={handleSubmit(onSubmit)} className="flex w-full max-w-md flex-col gap-4 dark:text-black">
        <FormFieldComponent
          label="Title"
          name="title"
          register={register}
          errors={errors}
          startIcon={<Text className="dark:text-babyPowder size-8" />}
        />
        <FormFieldComponent
          label="Content"
          name="body"
          register={register}
          errors={errors}
          isTextArea
        />
        <Button
          type="submit"
          className="h4-semibold bg-eerieBlack dark:bg-pumpkin w-full text-white"
          disabled={updatePost.isPending}
        >
          {updatePost.isPending ? <Spinner size="sm" /> : `Update Your Post`}
        </Button>
      </form>
    </main>
  );
}