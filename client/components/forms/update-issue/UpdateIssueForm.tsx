"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useForm, Controller } from "react-hook-form";
import Select from "react-select";
import dynamic from "next/dynamic";
import { toast } from "react-toastify";

import Spinner from "@/components/shared/Spinner";
import { Button } from "@/components/ui/button";
import { statusOptions } from "@/constants";
import {
  useGetSingleIssueQuery,
  useUpdateIssueMutation,
} from "@/lib/redux/features/issues/IssueApiSlice";
import { TIssueUpdateSchema } from "@/lib/validationSchemas";
import { extractErrorMessage } from "@/utils";
import customStyles from "../selectStyles";

const ClientOnly = dynamic<{ children: React.ReactNode }>(
  () => Promise.resolve(({ children }) => <>{children}</>),
  { ssr: false }
);

interface UpdateParamsProps {
  params: {
    id: string;
  };
}

export default function UpdateIssueForm({ params }: UpdateParamsProps) {
  const issueId = params.id;

  const { data: issueResponse, isLoading: isLoadingIssue } =
    useGetSingleIssueQuery(issueId);
  const [updateIssue, { isLoading: isUpdating }] = useUpdateIssueMutation();
  const router = useRouter();

  const {
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm<TIssueUpdateSchema>();

  // Populate the form with the current status once the issue loads
  useEffect(() => {
    const currentStatus = issueResponse?.status;
    if (currentStatus) {
      reset({ status: currentStatus });
    }
  }, [issueResponse, reset]);

  const onSubmit = async (formValues: TIssueUpdateSchema) => {
    if (!issueId) return;

    try {
      await updateIssue({ ...formValues, issueId }).unwrap();
      toast.success(
        "The Issue assigned to you has been updated. A confirmation email has been sent to the tenant"
      );
      reset();
      router.push("/profile");
    } catch (error) {
      const errorMessage = extractErrorMessage(error);
      toast.error(errorMessage || "An error occurred");
    }
  };

  if (isLoadingIssue) {
    return (
      <div className="flex justify-center p-6">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <main>
      <form
        noValidate
        onSubmit={handleSubmit(onSubmit)}
        className="flex w-full max-w-md flex-col gap-4 dark:text-black"
      >
        <div>
          <label htmlFor="status" className="h4-semibold dark:text-babyPowder">
            Status
          </label>
          <div className="mt-1 flex items-center space-x-3 text-sm">
            <ClientOnly>
              <Controller
                name="status"
                control={control}
                render={({ field: { onChange, onBlur, value } }) => (
                  <Select
                    className="mt-1 w-full"
                    options={statusOptions}
                    value={
                      statusOptions.find((option) => option.value === value) ??
                      null
                    }
                    onChange={(val) => onChange(val?.value)}
                    onBlur={onBlur}
                    placeholder="Update the Issue Status"
                    instanceId="issue-status-select"
                    styles={customStyles}
                  />
                )}
              />
            </ClientOnly>
          </div>
          {errors.status && (
            <p className="mt-2 text-sm text-red-500">{errors.status.message}</p>
          )}
        </div>

        <Button
          type="submit"
          className="h4-semibold bg-eerieBlack dark:bg-pumpkin mt-2 w-full text-white"
          disabled={isUpdating}
        >
          {isUpdating ? <Spinner size="sm" /> : `Update Status`}
        </Button>
      </form>
    </main>
  );
}