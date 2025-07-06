
import CreateReportForm from '@/components/forms/report-tenant/CreateReportForm'
import { AuthFormHeader } from '@/components/shared/forms/auth'
import { Metadata } from 'next'
import React from 'react'

export const metadata:Metadata = {
    title:"Accommodation Center | Report Tenant",
    description:"Tenants can report misconduct or misbehaviour of fellow tenants to the management"
}

export default function ReportTenantPage() {
  return (
    <div>
      <AuthFormHeader 
        title='Report a Tenant' 
        staticText='All reports shall remain anonymous.We shall act accordingly but will not disclose details of who raised the concern'
        linkHref='/profile'
        linkText='Back to Profile' />
        <div className='mt-7 sm:mx-auto sm:w-full sm:max-w-[480px]'>
            <div className='bg-lightGrey dark:bg-deepBlueGrey rounded-xl px-6 py-12 shadow sm:rounded-lg sm:px-12 md:rounded-3xl'>
                <CreateReportForm />
            </div>
        </div>
    </div>
  )
}
