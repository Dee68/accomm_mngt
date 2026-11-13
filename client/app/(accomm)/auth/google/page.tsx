"use client";

import Spinner from '@/components/shared/Spinner';
import { useSocialAuth } from '@/lib/query/use-auth';
import { useSearchParams, useRouter } from 'next/navigation';
import React, { Suspense, useEffect, useRef } from 'react';
import { toast } from 'react-toastify';
import { extractErrorMessage } from '@/utils';

export default function GoogleLoginPage() {
  return (
    <Suspense
      fallback={
        <div className='flex-center pt-32'>
          <Spinner size='xl' />
        </div>
      }
    >
      <GoogleLoginContent />
    </Suspense>
  );
}

function GoogleLoginContent() {
  const socialAuth = useSocialAuth();
  const searchParams = useSearchParams();
  const router = useRouter();
  const hasFired = useRef(false);

  const code = searchParams.get('code');
  const state = searchParams.get('state');

  // Fire once when both code and state are present.
  useEffect(() => {
    if (!code || !state || hasFired.current) return;
    hasFired.current = true;

    socialAuth
      .mutateAsync({ provider: 'google-oauth2', state, code })
      .then(async () => {
        toast.success('Logged in with Google');
        router.push('/welcome');
      })
      .catch((err) => {
        toast.error(extractErrorMessage(err) || 'Google login failed');
        router.push('/login');
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [code, state]);

  return (
    <div className="flex-center pt-32">
      {code && state ? (
        <Spinner size="xl" />
      ) : (
        <p className="text-lg text-gray-600">Redirecting to Google login...</p>
      )}
    </div>
  );
}
