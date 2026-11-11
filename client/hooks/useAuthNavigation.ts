// hooks/useAuthNavigation.ts
import { leftNavLinks } from '@/constants';
import { useMe, useLogout } from '@/lib/query/use-auth';
import { useAuthStore } from '@/lib/stores/auth-store';
import { extractErrorMessage } from '@/utils';
import { useRouter } from 'next/navigation';
import { toast } from 'react-toastify';

const TECHNICIAN_OCCUPATIONS = [
  'mason', 'plumber', 'painter', 'roofer',
  'electrician', 'carpenter', 'hvac',
] as const;

export function useAuthNavigation() {
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const { data: user } = useMe();
  const logoutMutation = useLogout();

  const occupation = user?.occupation;
  const isTechnician =
    isAuthenticated &&
    typeof occupation === 'string' &&
    (TECHNICIAN_OCCUPATIONS as readonly string[]).includes(occupation);

  const handleLogout = async () => {
    try {
      await logoutMutation.mutateAsync();
      router.push('/login');
      toast.success('Logged out');
    } catch (e) {
      const errorMessage = extractErrorMessage(e);
      toast.error(errorMessage || 'An error occurred');
    }
  };

  const filteredNavLinks = leftNavLinks.filter((link) => {
    if (
      link.path === '/profile' ||
      link.path === '/tenants' ||
      link.path === '/bookmark' ||
      link.path === '/report-issue' ||
      link.path === '/report-tenant' ||
      link.path === '/technicians' ||
      link.path === '/add-post'
    ) {
      return isAuthenticated;
    }

    if (link.path === '/assigned-issues') {
      return isTechnician;
    }

    return true;
  });

  return { handleLogout, filteredNavLinks, isAuthenticated, isTechnician, occupation };
}
