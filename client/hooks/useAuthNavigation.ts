import { leftNavLinks } from "@/constants";
import { useGetUserQuery, useLogoutUserMutation } from "@/lib/redux/features/auth/authApiSlice";
import { setLogout } from "@/lib/redux/features/auth/authSlice";
import { useAppDispatch, useAppSelector } from "@/lib/redux/hooks/typedHooks";
import { extractErrorMessage } from "@/utils";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";

export function useAuthNavigation() {
  const dispatch = useAppDispatch();
  const [logoutUser] = useLogoutUserMutation();
  const { isAuthenticated } = useAppSelector((state) => state.auth);
  const { data: userResponse } = useGetUserQuery(undefined, {
    skip: !isAuthenticated,
  });
  const router = useRouter();

  //const user = userData?.data;
  const occupation = userResponse?.occupation

  const handleLogout = async () => {
    try {
      await logoutUser().unwrap();
      dispatch(setLogout());
      router.push("/login");
      toast.success("Logged out");
    } catch (e) {
      const errorMessage = extractErrorMessage(e);
      toast.error(errorMessage || "An error occurred");
    }
  };

  const filteredNavLinks = leftNavLinks.filter((link) => {
    // Authenticated-only links
    if (
      link.path === "/profile" ||
      link.path === "/tenants" ||
      link.path === "/bookmark" ||
      link.path === "/report-issue" ||
      link.path === "/report-tenant" ||
      link.path === "/technicians" ||
      link.path === "/add-post"
    ) {
      return isAuthenticated;
    }

    // Assigned issues — authenticated non-tenants only
    if (link.path === "/assigned-issues") {
      return isAuthenticated && occupation !== "tenant";
    }

    return true;
  });

  return { handleLogout, filteredNavLinks, isAuthenticated };
}