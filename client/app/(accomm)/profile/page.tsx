

import Spinner from '@/components/shared/Spinner';
import ProtectedRoute from '@/components/shared/ProtectedRoutes';
import type { Metadata } from 'next';
import Header from '@/components/profile/Header';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import About from '@/components/profile/About';
import Post from '@/components/profile/Post';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export const metadata:Metadata = {
  title:"Accommodation Center | User Profile",
  description:"Signed in user can view their profile information"
}

function ProfilePageContent() {
    
  return (
   <>
    <div className='grid items-start gap-4 px-4 pb-4 md:gap-6 md:px-6'>
      <Header />
      <div className='w-full'>
      {/* the tabs*/}
      <Tabs className='dark:border-eerieBlack rounded-lg border' defaultValue='about'>
        <TabsList className='bg-baby_rich flex space-x-4'>
          <TabsTrigger value='about' className='h3-semibold tab'>About</TabsTrigger>
          <TabsTrigger value='posts' className='h3-semibold tab'>Posts</TabsTrigger>
          <TabsTrigger value='my-issues' className='h3-semibold tab'>My Issues</TabsTrigger>
          <TabsTrigger value='my-reports' className='h3-semibold tab'>My Reports</TabsTrigger>
          <TabsTrigger value='assigned-issues' className='h3-semibold tab'>Assigned Issues</TabsTrigger>
        </TabsList>
        {/* about tab content */}
        <About />
        {/* post tab content */}
        <Post />
        {/* issue tab content */}
        {/* report tab content */}
        {/* assigned tab content */}
      </Tabs>
      </div>
    </div>
    <div className='flex cursor-pointer flex-row justify-between'>
      <Link href="/profile/edit">
      <Button className='h3-semibold electricIndigo-gradient w-64 text-babyPowder rounded-lg'>Update Profile</Button>
      </Link>
      <Link href="/apartment">
      <Button className='h3-semibold electricIndigo-gradient w-64 text-babyPowder rounded-lg'>Add Apartment</Button>
      </Link>
    </div>
   </>
  )
}


export default function ProfilePage(){
  return (
    <ProtectedRoute>
      <ProfilePageContent />
    </ProtectedRoute>
  )
}



