// lib/api/reports.ts
import { apiGet, apiPost } from '@/lib/api/client';
import type { MyReportsResponse, ReportTenantData, ReportTenantResponse } from '@/types';

export const reportsApi = {
  reportTenant: (body: ReportTenantData) =>
    apiPost<ReportTenantResponse['data'], ReportTenantData>('/reports/create/', body),

  myReports: () => apiGet<MyReportsResponse['data']>('/reports/me/'),
};