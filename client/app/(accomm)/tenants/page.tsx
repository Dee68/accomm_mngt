import ProtectedRoute from '@/components/shared/ProtectedRoutes';
import Spinner from '@/components/shared/Spinner';
import { useGetAllUsersQuery } from '@/lib/redux/features/users/usersApiSlice'
import React from 'react'
import { Metadata } from 'next';
import TenantCard from '@/components/cards/TenantCard';

export const metadata: Metadata = {
  title:"Accommodation Center | Tenants",
  description: "Authenticated users can view basic info of other tenants within the property. Tenants can also search for other tenants."
}

function TenantsPageContent(){
  return (
    <div>
      <TenantCard />
    </div>
  )
}

export default function TenantsPage(){
  return (
    <ProtectedRoute>
      <TenantsPageContent />
    </ProtectedRoute>
  )
}
