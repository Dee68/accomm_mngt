import Select  from 'react-select';
import { useGetUserProfileQuery } from '@/lib/redux/features/users/usersApiSlice';
import { TProfileSchema } from '@/lib/validationSchemas';
import { UserSearch } from 'lucide-react';
import dynamic from 'next/dynamic'
import React, { useEffect } from 'react'
import { Control, Controller, UseFormSetValue } from 'react-hook-form';
import customStyles from '../selectStyles';


const ClientOnly = dynamic<{children:React.ReactNode}>(
    ()=> Promise.resolve(({children})=><>{children}</>),
    {ssr:false},
);

type Gender = "male" | "female";

function isGender(value:any):value is Gender{
    return ["male","female"].includes(value);
};

const genderOptions = [
    {value:"male",label:"Male"},
    {value:"female",label:"Female"},
];

interface GenderSelectFieldProps {
    setValue:UseFormSetValue<TProfileSchema>,
    control:Control<TProfileSchema>
}

export default function GenderSelectField({setValue,control}:GenderSelectFieldProps) {
    const {data:profileData} = useGetUserProfileQuery();
    const profile = profileData?.profile;

    useEffect(()=>{
        if (profile?.gender) {
            const genderValue = genderOptions.find((option)=>option.value===profile.gender);
            if (genderValue && isGender(genderValue)) {
                setValue("gender",genderValue);
            }
        }
    },[profile,setValue]);

  return (
    <div>
        <label htmlFor='gender' className='h4-semibold dark:text-babyPowder'>Gender</label>
        <div className='mt-1 flex items-center space-x-3'>
            <UserSearch className='dark:text-babyPowder size-8'/>
            <ClientOnly>
                <Controller 
                    control={control} 
                    name='gender' 
                    render={({field})=>(
                        <Select 
                            className='mt-1 w-full' 
                            {...field}
                            options={genderOptions}
                            value={genderOptions.find(
									(option) => option.value === field.value,
								)}
								onChange={(option) => field.onChange(option?.value)}
								instanceId="gender-select"
								styles={customStyles} 
                        />
                    )} 
                />

            </ClientOnly>
        </div>
      
    </div>
  )
}
