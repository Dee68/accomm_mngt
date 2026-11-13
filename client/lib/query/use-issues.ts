'use client';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { issuesApi } from '@/lib/api/issues';
import { keys } from '@/lib/query/keys';
import type { ReportIssueData, UpdateIssueData } from '@/types';

export function useMyIssues() {
  return useQuery({
    queryKey: keys.issues.list('me'),
    queryFn: issuesApi.myIssues,
  });
}

export function useMyAssignedIssues() {
  return useQuery({
    queryKey: keys.issues.list('assigned'),
    queryFn: issuesApi.myAssigned,
  });
}

export function useSingleIssue(id: string) {
  return useQuery({
    queryKey: keys.issues.detail(id),
    queryFn: () => issuesApi.single(id),
    enabled: !!id,
  });
}

export function useReportIssue() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ReportIssueData) => issuesApi.report(body),
    onSuccess: () => {
      // RTK invalidates ["Issue"] — mirror that
      qc.invalidateQueries({ queryKey: keys.issues.all });
    },
  });
}

export function useUpdateIssue() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: UpdateIssueData) => issuesApi.update(body),
    onSuccess: (_data, variables) => {
      qc.invalidateQueries({ queryKey: keys.issues.all });
      qc.invalidateQueries({ queryKey: keys.issues.detail(variables.issueId) });
    },
  });
}

export function useDeleteIssue() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => issuesApi.remove(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: keys.issues.all });
    },
  });
}