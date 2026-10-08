import {
  IssueResponse,
  MyAssignedIssuesResponse,
  MyIssuesResponse,
  ReportIssueData,
  UpdateIssueData,
  UpdateIssueResponse,
} from "@/types";
import { baseApiSlice } from "../api/baseApiSlice";

export const issueApiSlice = baseApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    reportIssue: builder.mutation<IssueResponse["data"], ReportIssueData>({
      query: ({ apartmentId, ...issueData }) => ({
        url: `/issues/create/${apartmentId}/`,
        method: "POST",
        body: issueData,
      }),
      transformResponse: (response: IssueResponse) => response.data,
      invalidatesTags: ["Issue"],
    }),

    getMyIssues: builder.query<MyIssuesResponse["data"], void>({
      query: () => "/issues/me/",
      transformResponse: (response: MyIssuesResponse) => response.data,
      providesTags: ["Issue"],
    }),

    getMyAssignedIssues: builder.query<MyAssignedIssuesResponse["data"], void>({
      query: () => "/issues/assigned/",
      transformResponse: (response: MyAssignedIssuesResponse) => response.data,
      providesTags: ["Issue"],
    }),

    getSingleIssue: builder.query<IssueResponse["data"], string>({
      query: (issueId) => `/issues/${issueId}/`,
      transformResponse: (response: IssueResponse) => response.data,
      providesTags: ["Issue"],
    }),

   updateIssue: builder.mutation<UpdateIssueResponse["data"], UpdateIssueData>({
      query: ({ issueId, ...statusData }) => ({
        url: `/issues/update/${issueId}/`,
        method: "PATCH",
        body: statusData,
      }),
      transformResponse: (response: UpdateIssueResponse) => response.data,
      invalidatesTags: ["Issue"],
    }),

    deleteIssue: builder.mutation<void, string>({
      query: (issueId) => ({
        url: `/issues/delete/${issueId}/`,
        method: "DELETE",
      }),
      invalidatesTags: ["Issue"],
    }),
  }),
});

export const {
  useReportIssueMutation,
  useGetMyIssuesQuery,
  useDeleteIssueMutation,
  useGetMyAssignedIssuesQuery,
  useGetSingleIssueQuery,
  useUpdateIssueMutation,
} = issueApiSlice;