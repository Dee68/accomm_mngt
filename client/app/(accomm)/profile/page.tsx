"use client";

import { useGetUserProfileQuery } from '@/lib/redux/features/users/usersApiSlice';
import Spinner from '@/components/shared/Spinner';
import ProtectedRoute from '@/components/shared/ProtectedRoutes';

function ProfilePageContent() {
    const {data, isLoading} = useGetUserProfileQuery({});
    console.log('User profile data:', data);

    if (isLoading) {
        return (
            <div className='flex-center pt-32'>
                <Spinner size='xl' />
            </div>
        )
    }
    if (!data?.profile) {
        return <div className='pt-32 text-center'>No profile data available.</div>;
    }
  return (
    <div>
      <h1>{data?.profile.username}&apos;s Profile</h1>
    </div>
  )
}


export default function ProfilePage(){
  return (
    <ProtectedRoute>
      <ProfilePageContent />
    </ProtectedRoute>
  )
}



