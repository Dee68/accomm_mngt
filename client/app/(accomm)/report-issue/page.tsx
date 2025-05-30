import CreateIssueForm from "@/components/forms/report-issue/CreateIssueForm";
import { AuthFormHeader } from "@/components/shared/forms/auth";
import { Metadata } from "next";

import React from 'react'

const metadata:Metadata = {
    title:"Accommodation Center | Report Issue",
    description:"Tenants can report an issue to the management with regards to their apartment"
}

export default function ReportIssuePage() {
  return (
    <div>
      <AuthFormHeader title="Report an Issue"/>
      <div className="mt-7 sm:mx-auto sm:w-full sm:max-w-[480px]">
        <div className="bg-lightGrey dark:bg-deepBlueGrey rounded-xl px-6 py-12 shadow sm:rounded-lg sm:px-12 md:rounded-3xl">
          <p className="dark:text-pumpkin text-2xl">
            <CreateIssueForm />
          </p>
            
        </div>
      </div>
    </div>
  )
}
