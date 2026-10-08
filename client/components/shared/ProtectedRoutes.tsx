"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAppSelector } from "@/lib/redux/hooks/typedHooks";
import { useGetUserQuery } from "@/lib/redux/features/auth/authApiSlice";
import Spinner from "@/components/shared/Spinner";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { isAuthenticated } = useAppSelector((state) => state.auth);
  const { isLoading, isError } = useGetUserQuery();

  useEffect(() => {
    if (!isLoading && isError) {
      router.push("/login");
    }
  }, [isLoading, isError, router]);

  if (isLoading) {
    return (
      <div className="flex-center pt-32">
        <Spinner size="xl" />
      </div>
    );
  }

  if (!isAuthenticated) return null;

  return <>{children}</>;
}

export default ProtectedRoute;