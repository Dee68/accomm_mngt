

import Spinner from '@/components/shared/Spinner';
import ProtectedRoute from '@/components/shared/ProtectedRoutes';
import type { Metadata } from 'next';
import Header from '@/components/profile/Header';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import About from '@/components/profile/About';
import Post from '@/components/profile/Post';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import Issue from '@/components/profile/Issue';
import AssignedIssues from '@/components/profile/AssignedIssues';
import Reports from '@/components/profile/Reports';
import ProfilePageContent from '@/components/profile/ProfilePageContent';

export const metadata:Metadata = {
  title:"Accommodation Center | User Profile",
  description:"Signed in user can view their profile information"
}




export default function ProfilePage(){
  return (
    <ProtectedRoute>
      <ProfilePageContent />
    </ProtectedRoute>
  )
}



