"use client";
import { useAddRatingMutation } from '@/lib/redux/features/rating/ratingApiSlice';
import { ratingCreateSchema, TRatingCreateSchema } from '@/lib/validationSchemas';
import { extractErrorMessage } from '@/utils';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React, { useEffect, useState } from 'react'
import { Controller, FieldValues, RegisterOptions, useForm, UseFormRegisterReturn } from 'react-hook-form';
import { toast } from 'react-toastify';
import { FormFieldComponent } from '../FormFieldComponents';
import { UserCog } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Spinner from '@/components/shared/Spinner';

export default function CreateRatingForm() {
    const router = useRouter();
    const [addRating, {isLoading}] = useAddRatingMutation();
    const {register,handleSubmit,setValue,control,formState:{errors}} = useForm<TRatingCreateSchema>({
        resolver: zodResolver(ratingCreateSchema),
        mode:"all"
    });
    const [username, setUsername] = useState("");
    // useEffect(() => {
    //     const queryParams = new URLSearchParams(window.location.search);
    //     const ratedUserUsername = queryParams.get("username");
    //     if (ratedUserUsername) {
    //         setValue("rated_user_username",ratedUserUsername);
    //         setUsername(ratedUserUsername);
    //     }
     
    // }, [setValue]);
    useEffect(() => {
      const queryParams = new URLSearchParams(window.location.search);
      const ratedUserUsername = queryParams.get("username");

      if (!ratedUserUsername) {
        toast.error("No technician selected. Redirecting...");
        router.push("/technicians");
        return;
      }

      setValue("rated_user_username", ratedUserUsername);
      setUsername(ratedUserUsername);
    }, [setValue, router]);
    const onSubmit = async(data:TRatingCreateSchema)=>{
        try {
            await addRating(data).unwrap();
            toast.success("Your rating has been added!");
            router.push("/technicians");
        } catch (error) {
            const errorMessage = extractErrorMessage(error);
            toast.error(errorMessage || "An error occurred")
        }
    }
  return (
    <main>
      <form noValidate onSubmit={handleSubmit(onSubmit)} className='flex w-full max-w-md flex-col gap-4'>
        {/* <FormFieldComponent
                  label={`${username}'s username (This is auto filled in)`} 
                  name={'rated_user_username'}
                  register={register}
                  errors={errors}
                  startIcon={<UserCog className='dark:text-babyPowder size-8' />}
                  disabled
         />
         <label htmlFor='rating' className='h2-semibold dark:text-babyPowder'>Rating</label> */}
         <div className='flex items-center gap-3'>
          <UserCog className='dark:text-babyPowder size-8' />
          <div>
            <p className='text-sm text-muted-foreground'>Rating</p>
            <p className='h3-semibold dark:text-babyPowder'>{username}</p>
          </div>
        </div>
         <Controller
         name='rating'
         control={control} 
         render={({field})=>(
           
            <Controller
              name='rating'
              control={control}
              render={({ field }) => (
                <select
                  {...field}
                  id='rating'
                  className='flex h-10 w-full rounded-md border px-3 py-2 text-sm file:border-0 
                      file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none 
                      focus-visible:ring-2 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50'
                  onChange={(e) => field.onChange(Number(e.target.value))}
                >
                  <option value=''>Choose a rating</option>
                  <option value='1'>1 — Very Poor</option>
                  <option value='2'>2 — Poor</option>
                  <option value='3'>3 — Average</option>
                  <option value='4'>4 — Good</option>
                  <option value='5'>5 — Excellent</option>
                </select>
              )}
            />
         )}
         />
         {errors.rating && (
            <p className='text-sm text-red-500'>{errors.rating.message}</p>
         )}
         <FormFieldComponent
         label='Comment'
         name='comment'
         errors={errors}
         register={register} 
         placeholder='Give us your reason for this rating, it will help improve our services.'
         isTextArea
         />
         <Button type='submit' className='h4-semibold bg-eerieBlack dark:bg-pumpkin w-full text-white' disabled={isLoading}>
            {isLoading ? <Spinner size='sm'/> : `Add Rating`}
         </Button>
      </form>
    </main>
  )
}
