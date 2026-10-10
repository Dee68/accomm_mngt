"use client";

import Spinner from '@/components/shared/Spinner'
import { useSocialAuth } from '@/hooks';
import { useSocialAuthenticationMutation } from '@/lib/redux/features/auth/authApiSlice'
import { useSearchParams } from 'next/navigation';
import React, { Suspense } from 'react'




export default function GoogleLoginPage() {
  return (
    <Suspense fallback={
      <div className='flex-center pt-32'>
        <Spinner size='xl'/>
      </div>
    }>
      <GoogleLoginContent />
    </Suspense>
  )
}

function GoogleLoginContent(){
  const [googleAuthenticate] = useSocialAuthenticationMutation();
  const searchParams = useSearchParams();
  const code = searchParams.get("code");
  const state = searchParams.get("state");


  useSocialAuth(googleAuthenticate, "google-oauth2");

  return (
    <div className="flex-center pt-32">
      {code && state ? (<Spinner size="xl" />):(
        <p className="text-lg text-gray-600">Redirecting to Google login...</p>
    )}
   </div>   
  );
}
