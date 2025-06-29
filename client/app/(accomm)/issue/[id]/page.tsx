import { Metadata } from 'next'
import IssueDetails from '@/components/issues/IssueDetails';


export const metadata:Metadata = {
    title:"Accommodation Center | Issue Details",
    description:"Authenticated uses can get the details of the issue they have raised. They can also delete the issue"
};

interface ParamsProps {
    params:{
        id:string;
    };
}

export default function IssueDetailPage({params}:ParamsProps) {
  return (
    <div>
      <IssueDetails params={params} />
    </div>
  )
}
