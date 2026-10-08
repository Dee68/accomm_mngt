"use client";

import { setAuth, setLogout } from "@/lib/redux/features/auth/authSlice";
import { useAppDispatch } from "@/lib/redux/hooks/typedHooks";
import { useGetUserQuery } from "@/lib/redux/features/auth/authApiSlice";
import { useEffect } from "react";

export default function PersistAuth() {
  const dispatch = useAppDispatch();
  const { data: user, isLoading, isSuccess, isError } = useGetUserQuery();

  useEffect(() => {
    if (isSuccess && user) {
      dispatch(setAuth());
    } else if (!isLoading && (isError || !user)) {
      dispatch(setLogout());
    }
  }, [isSuccess, isLoading, isError, user, dispatch]);

  return null;
}