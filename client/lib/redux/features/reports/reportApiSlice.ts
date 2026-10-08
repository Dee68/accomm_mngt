import { MyReportsResponse, ReportTenantData, ReportTenantResponse } from "@/types";
import { baseApiSlice } from "../api/baseApiSlice";


export const reportApiSlice = baseApiSlice.injectEndpoints({
    endpoints:(builder)=>({
        reportTenant:builder.mutation<ReportTenantResponse,ReportTenantData>({
            query:(reportData)=>({
                url:"/reports/create/",
                method:"POST",
                body:reportData
            }),
            invalidatesTags:["Report"]
        }),
        // getMyReports:builder.query<MyReportsResponse,void>({
        //     query:()=> "/reports/me/",
        //     providesTags:["Report"],
        // }),
        getMyReports: builder.query<MyReportsResponse["data"], void>({
            query: () => "/reports/me/",
            transformResponse: (response: MyReportsResponse) => response.data,
            providesTags: ["Report"],
            }),

    }),
});

export const {useReportTenantMutation,useGetMyReportsQuery} = reportApiSlice;