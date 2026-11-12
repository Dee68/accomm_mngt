'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/stores/auth-store';
import Spinner from '@/components/shared/Spinner';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const isHydrated = useAuthStore((s) => s.isHydrated);

  useEffect(() => {
    // Only redirect if we have checked the auth state (hydrated) and we are NOT logged in.
    if (isHydrated && !isAuthenticated) {
      router.replace('/login');
    }
  }, [isHydrated, isAuthenticated, router]);

  // While PersistAuth is fetching /me, show a spinner
  if (!isHydrated) {
    return (
      <div className="flex-center pt-32">
        <Spinner size="xl" />
      </div>
    );
  }

  // If hydrated and not authenticated, show nothing while the redirect happens
  if (!isAuthenticated) {
    return null;
  }

  // If hydrated and authenticated, render the page
  return <>{children}</>;
}

export default ProtectedRoute;
