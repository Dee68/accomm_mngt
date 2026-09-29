import React from 'react'
import type { Metadata } from 'next'
import { AuthFormHeader } from '@/components/shared/forms/auth'
import CreateRatingForm from '@/components/forms/add-rating/CreateRatingForm'

export const metadata:Metadata = {
    title:"Accommodation Center | Add Rating",
    description:"Tenants can rate technicians to show their satisfaction or dissatisfaction"
}

export default function AddRatingPage() {
  return (
    <div>
        <AuthFormHeader
        title='Rate a technician'
        staticText='Tell us what you think about the service rendered'
        linkHref='/technicians'
        linkText='Back to Technicians Page'
        />
          <div className="mt-7 sm:mx-auto sm:w-full sm:max-w-[480px]">
            <div className="bg-lightGrey dark:bg-deepBlueGrey rounded-xl px-6 py-12 shadow sm:rounded-lg sm:px-12 md:rounded-3xl">
            <CreateRatingForm />
            </div>
        </div>
    </div>
  )
}
