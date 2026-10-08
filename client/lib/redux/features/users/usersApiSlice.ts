import { baseApiSlice } from "@/lib/redux/features/api/baseApiSlice";
import {
  NonTenantResponse,
  ProfileData,
  ProfilesResponse,
  ProfileResponse,
  QueryParams,
} from "@/types";

export const usersApiSlice = baseApiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getAllUsers: builder.query<ProfilesResponse["data"], QueryParams>({
      query: (params = {}) => {
        const queryString = new URLSearchParams();
        if (params.page) {
          queryString.append("page", params.page.toString());
        }
        if (params.searchTerm) {
          queryString.append("search", params.searchTerm);
        }
        return `/profiles/all/?${queryString.toString()}`;
      },
      transformResponse: (response: ProfilesResponse) => response.data,
      providesTags: ["User"],
    }),

    getAllTechnicians: builder.query<NonTenantResponse["data"], QueryParams>({
      query: (params = {}) => {
        const queryString = new URLSearchParams();
        if (params.page) {
          queryString.append("page", params.page.toString());
        }
        if (params.searchTerm) {
          queryString.append("search", params.searchTerm);
        }
        return `/profiles/non-tenant-profiles/?${queryString.toString()}`;
      },
      transformResponse: (response: NonTenantResponse) => response.data,
      providesTags: ["User"],
    }),

    getUserProfile: builder.query<ProfileResponse["data"], void>({
      query: () => "/profiles/user/my-profile/",
      transformResponse: (response: ProfileResponse) => response.data,
      providesTags: ["User"],
    }),

    updateUserProfile: builder.mutation<ProfileData, ProfileData>({
      query: (formData) => ({
        url: "/profiles/user/update/",
        method: "PATCH",
        body: formData,
      }),
      invalidatesTags: ["User"],
    }),
  }),
});

export const {
  useGetAllUsersQuery,
  useGetAllTechniciansQuery,
  useUpdateUserProfileMutation,
  useGetUserProfileQuery,
} = usersApiSlice;