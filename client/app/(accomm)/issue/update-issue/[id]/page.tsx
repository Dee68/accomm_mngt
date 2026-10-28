import React from 'react';
import { Metadata } from 'next';
import { AuthFormHeader } from '@/components/shared/forms/auth';
import UpdateIssueForm from '@/components/forms/update-issue/UpdateIssueForm';

export const metadata: Metadata = {
  title: 'Accommodation Center | Update Issue',
  description: 'Technicians assigned to an issue can update the status of the issue',
};

interface UpdateParamsProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function UpdateIssuePage({ params }: UpdateParamsProps) {
  const resolvedParams = await params;

  return (
    <div>
      <AuthFormHeader
        title="Update Issue"
        staticText="Go back?"
        linkText="Back to Profile"
        linkHref="/profile"
      />
      <div className="mt-7 sm:mx-auto sm:w-full sm:max-w-[480px]">
        <div className="bg-lightGrey dark:bg-deepBlueGrey rounded-xl px-6 py-12 shadow sm:rounded-lg sm:px-12 md:rounded-3xl">
          <UpdateIssueForm params={resolvedParams} />
        </div>
      </div>
    </div>
  );
}
