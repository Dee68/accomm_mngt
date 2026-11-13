"use client";

import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useLogin } from "@/lib/query/use-auth";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { loginUserSchema, TLoginUserSchema } from "@/lib/validationSchemas";
import { extractErrorMessage } from "@/utils";
import { toast } from "react-toastify";
import { FormFieldComponent } from "@/components/shared/forms/FormFieldComponent";
import { MailIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import Spinner from "@/components/shared/Spinner";

export default function LoginForm() {
  const loginMutation = useLogin();
  const router = useRouter();
  const { register, handleSubmit, reset, formState: { errors } } = useForm<TLoginUserSchema>({
    resolver: zodResolver(loginUserSchema),
    mode: "all",
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = async (values: z.infer<typeof loginUserSchema>) => {
  try {
    await loginMutation.mutateAsync(values);
    toast.success("Login Successful");
    reset();
    router.push("/welcome");
    // DO NOT call router.push("/welcome") here. 
    // Let useRedirectIfAuthenticated handle it once isHydrated is true.
  } catch (error) {
    const errorMessage = extractErrorMessage(error);
    toast.error(errorMessage || "An error occurred");
  }
};

  return (
    <main>
      <form noValidate onSubmit={handleSubmit(onSubmit)} className="flex w-full max-w-md gap-4 flex-col">
        <FormFieldComponent
          label="Email Address"
          name="email"
          register={register}
          startIcon={<MailIcon className="dark:text-babyPowder size-8" />}
          errors={errors}
          placeholder="Email Address"
        />
        <FormFieldComponent
          label="Password"
          name="password"
          register={register}
          isPassword={true}
          errors={errors}
          placeholder="Password"
          link={{ linkText: "Forgot Password?", linkUrl: "/forgot-password" }}
        />
        <Button className="h4-semibold bg-eerieBlack dark:bg-pumpkin text-white w-full" type="submit" disabled={loginMutation.isPending}>
          {loginMutation.isPending ? <Spinner size="sm" /> : `Sign In`}
        </Button>
      </form>
    </main>
  );
}