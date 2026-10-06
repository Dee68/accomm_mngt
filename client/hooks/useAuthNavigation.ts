import { leftNavLinks } from "@/constants";
import { useGetUserQuery, useLogoutUserMutation } from "@/lib/redux/features/auth/authApiSlice";
import { setLogout } from "@/lib/redux/features/auth/authSlice";
import { useAppDispatch, useAppSelector } from "@/lib/redux/hooks/typedHooks";
import { extractErrorMessage } from "@/utils";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";

const TECHNICIAN_OCCUPATIONS = [
  "mason",
  "plumber",
  "painter",
  "roofer",
  "electrician",
  "carpenter",
  "hvac",
];



export function useAuthNavigation() {
  const dispatch = useAppDispatch();
  const [logoutUser] = useLogoutUserMutation();
  const { isAuthenticated } = useAppSelector((state) => state.auth);
  const { data: user } = useGetUserQuery(undefined, {
    skip: !isAuthenticated,
  });
  const router = useRouter();

  const occupation = user?.occupation;


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

    if (link.path === "/assigned-issues") {
      return (
        isAuthenticated &&
        typeof occupation === "string" &&
        TECHNICIAN_OCCUPATIONS.includes(occupation)
      );
    }
    

    return true;
  });

const isTechnician =
  isAuthenticated &&
  typeof occupation === "string" &&
  TECHNICIAN_OCCUPATIONS.includes(occupation);

return { handleLogout, filteredNavLinks, isAuthenticated, isTechnician, occupation };

  //return { handleLogout, filteredNavLinks, isAuthenticated };
}