import { useAuthStore } from "@/lib/stores/auth-store";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

const useRedirectIfAuthenticated = () => {
  const router = useRouter();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isHydrated = useAuthStore((state) => state.isHydrated);

  console.log('[useRedirectIfAuthenticated]', { isAuthenticated, isHydrated });

  useEffect(() => {
    console.log('[useRedirectIfAuthenticated] effect fired', { isAuthenticated, isHydrated });
    if (isHydrated && isAuthenticated) {
      console.log('[useRedirectIfAuthenticated] REDIRECTING TO /welcome');
      router.replace("/welcome");
    }
  }, [isAuthenticated, isHydrated, router]);
};

export default useRedirectIfAuthenticated;