// lib/query/use-reports.ts
'use client';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { reportsApi } from '@/lib/api/reports';
import { keys } from '@/lib/query/keys';
import type { ReportTenantData } from '@/types';

export function useMyReports() {
  return useQuery({
    queryKey: keys.reports.list(),
    queryFn: reportsApi.myReports,
  });
}

export function useReportTenant() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ReportTenantData) => reportsApi.reportTenant(body),
    onSuccess: () => {
      // RTK invalidated ["Report"] — refresh the my-reports list
      qc.invalidateQueries({ queryKey: keys.reports.all });
    },
  });
}