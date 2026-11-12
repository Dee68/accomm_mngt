// hooks/useRedirectIfAuthenticated.ts
import { useAuthStore } from "@/lib/stores/auth-store";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

const useRedirectIfAuthenticated = () => {
  const router = useRouter();
  // Read from our new Zustand store instead of Redux
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  useEffect(() => {
    if (isAuthenticated) {
      router.push("/welcome");
    }
  }, [isAuthenticated, router]);
};

export default useRedirectIfAuthenticated;