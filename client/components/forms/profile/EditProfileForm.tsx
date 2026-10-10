"use client";
import { useGetUserProfileQuery, useUpdateUserProfileMutation, useUploadAvatarMutation } from '@/lib/redux/features/users/usersApiSlice';
import { TProfileSchema } from '@/lib/validationSchemas';
import { useRouter } from 'next/navigation';
import React, { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form';
import * as z from "zod";
import { profileSchema } from '@/lib/validationSchemas/ProfileSchema';

import { extractErrorMessage } from '@/utils';
import { toast } from 'react-toastify';
import { FormFieldComponent } from '@/components/shared/forms/FormFieldComponent';
import { Contact2Icon, Map, MapPinnedIcon } from 'lucide-react';
import GenderSelectField from './GenderSelectField';
import OccupationSelectField from './OccupationSelectField';
import Spinner from '@/components/shared/Spinner';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function EditProfileForm() {
    const {data} = useGetUserProfileQuery();
    const profile = data
    const [uploading,setUploading] = useState(false);
    const [updateUserProfile,{isLoading}] = useUpdateUserProfileMutation();
    const [uploadAvatar, { isLoading: isUploadingAvatar }] = useUploadAvatarMutation();
    const router = useRouter();

    const {register,handleSubmit,control,setValue,reset,formState:{errors},} = useForm<TProfileSchema>();

    useEffect(() => {
		if (profile) {
			reset({ ...profile });
		}
	}, [profile, reset]);

    const uploadFileHandler = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;
    const file = e.target.files[0];

    const formData = new FormData();
    formData.append("avatar", file);   // matches serializer field name

    setUploading(true);
    try {
        await uploadAvatar(formData).unwrap();
        // The view returns 202 + {"message": "Avatar upload started"}
        // The actual avatar URL is set later by Celery — refetch after a beat.
        toast.success("Avatar upload started");
    } catch (error) {
        const errorMessage = extractErrorMessage(error);
        toast.error(errorMessage || "Failed to upload avatar");
    } finally {
        setUploading(false);
    }
    };

    const onSubmit = async(values:z.infer<typeof profileSchema>)=>{
        try {
           await updateUserProfile(values).unwrap();
           toast.success("Update successful");
           router.push("/profile");
        } catch (error) {
            const errorMessage = extractErrorMessage(error);
            toast.error(errorMessage || "An error occurred");
        }
    }

  return (
    <main>
      <form noValidate className='flex w-full flex-col max-w-md gap-4' onSubmit={handleSubmit(onSubmit)}>
        <FormFieldComponent 
            label='Username' 
            name='username' 
            register={register} 
            errors={errors} 
            placeholder='Username'
            startIcon={<Contact2Icon className='dark:text-babyPowder size-8' />}
            />
            <FormFieldComponent 
                label='First Name' 
                name='first_name' 
                register={register} 
                errors={errors} 
                placeholder='First Name'
                startIcon={<Contact2Icon className='dark:text-babyPowder size-8' />}
            />
            <FormFieldComponent 
                label='Last Name' 
                name='last_name' 
                register={register} 
                errors={errors} 
                placeholder='Last Name'
                startIcon={<Contact2Icon className='dark:text-babyPowder size-8' />}
            />
            <GenderSelectField setValue={setValue} control={control} />
            <OccupationSelectField setValue={setValue} control={control} />
            <FormFieldComponent 
                label='Country of Origin' 
                name='country_of_origin' 
                register={register} 
                errors={errors} 
                placeholder='What Country?'
                startIcon={<Map className='dark:text-babyPowder size-8' />}
            />
            <FormFieldComponent 
                label='City of Origin' 
                name='city_of_origin' 
                register={register} 
                errors={errors} 
                placeholder='What City'
                startIcon={<MapPinnedIcon className='dark:text-babyPowder size-8' />}
            />
            <FormFieldComponent 
                label='Bio' 
                name='bio' 
                register={register} 
                errors={errors} 
                placeholder='Bio'
                isTextArea
            />
            <label className='h4-semibold dark:text-babyPowder' htmlFor='avatar'>Avatar</label>
            <div className='flex w-full cursor-pointer items-center'>
                <div className='grow' style={{ maxWidth: "90%" }}>
                   <Input 
                   className='file:bg-eerieBlack dark:border-platinum dark:text-platinum cursor-pointer file:mr-3 file:rounded-md file:text-lime-500'
                   accept='image/*'
                   id='avatar'
                   name='avatar'
                   type='file'
                   onChange={uploadFileHandler} 
                   />
                </div>
                {uploading && (
                        <div className='shrink-0' style={{ width: "10%" }}>
                            <Spinner size='sm'/>
                        </div>
                    )}
            </div>
            <Button 
            className='h4-semibold bg-eerieBlack dark:bg-pumpkin mt-2 w-full text-white' type='submit' disabled={isLoading}>{isLoading ? <Spinner size="sm" /> : `Update Profile`}</Button>
      </form>
    </main>
  )
}

