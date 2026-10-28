
import { Metadata } from 'next';
import IssueDetails from '@/components/issues/IssueDetails';

export const metadata: Metadata = {
  title: 'Accommodation Center | Issue Details',
  description:
    'Authenticated users can get the details of the issue they have raised. They can also delete the issue.',
};

interface ParamsProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function IssueDetailPage({ params }: ParamsProps) {
  const resolvedParams = await params;

  return (
    <div>
      <IssueDetails params={resolvedParams} />
    </div>
  );
}
