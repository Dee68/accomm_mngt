"use client";
import { useGetMyIssuesQuery } from '@/lib/redux/features/issues/IssueApiSlice';
import React from 'react'
import Spinner from '../shared/Spinner';
import { TabsContent } from '../ui/tabs';
import IssueCard from '../cards/IssueCard';
import ProtectedRoute from "../shared/ProtectedRoutes";

function IssueContent() {
    const { data,isLoading,error } = useGetMyIssuesQuery();
    const myIssue = data
    //console.log("Issues API response:", data);


    if (isLoading) {
        return (
            <div className='flex-center pt-32'>
                <Spinner size='xl' />
            </div>
        );
    }
  return (
    <TabsContent value='my-issues'>
        <h2 className="h2-semibold flex-center font-robotoSlab dark:text-pumpkin text-xl">Total: {myIssue?.count}</h2>
        <div className="mt-4 grid cursor-pointer grid-cols-1 gap-4 p-1.5 md:grid-cols-2 lg:grid-cols-3">
            {myIssue && myIssue.results.length > 0 ? (
                myIssue.results.map((issue)=>(
                    <IssueCard key={issue.id} issue={issue} />
                ))
            ):(<p className='h2-semibold dark:text-lime-500'>
                You have not raised any issue(s) yet!
            </p>)}
        </div>
    </TabsContent>
  )
}

export default function Issue(){
   return (
     <ProtectedRoute>
        <IssueContent />
    </ProtectedRoute>
   )
}
