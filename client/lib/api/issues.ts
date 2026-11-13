import { apiGet, apiPatch, apiPost, apiDelete } from '@/lib/api/client';
import type {
  IssueResponse,
  MyAssignedIssuesResponse,
  MyIssuesResponse,
  ReportIssueData,
  UpdateIssueData,
  UpdateIssueResponse,
} from '@/types';

export const issuesApi = {
  report: ({ apartmentId, ...body }: ReportIssueData) =>
    apiPost<IssueResponse['data']>(`/issues/create/${apartmentId}/`, body),

  myIssues: () => apiGet<MyIssuesResponse['data']>('/issues/me/'),

  myAssigned: () => apiGet<MyAssignedIssuesResponse['data']>('/issues/assigned/'),

  single: (id: string) => apiGet<IssueResponse['data']>(`/issues/${id}/`),

  update: ({ issueId, ...body }: UpdateIssueData) =>
    apiPatch<UpdateIssueResponse['data']>(`/issues/update/${issueId}/`, body),

  remove: (id: string) => apiDelete<void>(`/issues/delete/${id}/`),
};