"use client";

import { useActivateUserMutation } from '@/lib/redux/features/auth/authApiSlice';
import { useRouter } from 'next/navigation';
import React, { useEffect } from 'react'
import { toast } from 'react-toastify';

interface ActivationPros {
  params:{
    uid: string;
    token: string;
  };
}

export default function ActivationPage({params}:ActivationPros) {
  const router = useRouter();
  const [activateUser,{isLoading,isError,error,isSuccess}] = useActivateUserMutation();
  useEffect(()=>{
    const {uid,token} = params;
    activateUser({uid,token});

  },[activateUser,params]);
   useEffect(()=>{
    if (isSuccess) {
      toast.success("Account successfully activated!");
      router.push("/login");
    }else if (isError) {
      console.error("Activation error:", JSON.stringify(error, null, 2));
      toast.error("Failed to activate your account.");
    }

  },[isSuccess,isError,error,router]);
  return (
    <div className='flex min-h-screen items-center justify-center'>
        <div className='text-center'>
            <h3 className='dark:text-platinum text-2xl font-robotoSlab font-bold text-gray-800 sm:text-4xl md:text-5xl'>
            {isLoading ? (
              <div className='flex-center'>
              <span className='mr-2'>
                ⏰
              </span>
              <span>Activating your account .... please wait.</span>
              <span className='ml-2'>🥱</span>
            </div>
            ) : isSuccess ? (
              <div className='flex-center'>
              <span className='mr-2'>
                ✅
              </span>
              <span>Account activated successfully!</span>
              
            </div>
            ):(isError && (
             <div className='flex-center'>
              <span className='mr-2'>
                ❌
              </span>
              <span>Your account has already been activated....</span>
              
            </div> 
            ))}
          </h3>
        </div>
      
    </div>
  )
}
