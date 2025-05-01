"use client";

import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useLoginUserMutation } from "@/lib/redux/features/auth/authApiSlice";
import { useRouter } from "next/navigation";
import { useAppDispatch } from "@/lib/redux/hooks/typedHooks";
import { useForm } from "react-hook-form";
import { loginUserSchema, TLoginUserSchema } from "@/lib/validationSchemas";
import { extractErrorMessage } from "@/utils";
import { toast } from "react-toastify";
import { setAuth } from "@/lib/redux/features/auth/authSlice";
import { FormFieldComponent } from "@/components/shared/forms/FormFieldComponent";
import { MailIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import Spinner from "@/components/shared/Spinner";

export default function LoginForm() {
    const [loginUser,{isLoading}] = useLoginUserMutation();
    const router = useRouter();
    const dispatch = useAppDispatch();
    const {register,handleSubmit,reset,formState:{errors}} = useForm<TLoginUserSchema>({
        resolver: zodResolver(loginUserSchema),
        mode: "all",
        defaultValues: {
            email: "",
            password: "",
        }
    });
    const onSubmit = async(values:z.infer<typeof loginUserSchema>)=>{
        try {
            await loginUser(values).unwrap();
            dispatch(setAuth());
            toast.success("Login Successful")
            router.push("/welcome");
            reset();
        } catch (error) {
            const errorMessage = extractErrorMessage(error);
            toast.error(errorMessage || "An error occurred");
        }
    }
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
      <Button className="h4-semibold bg-eerieBlack dark:bg-pumpkin text-white w-full" type="submit" disabled={isLoading}>
        {isLoading ? <Spinner size="sm" /> :`Sign In`}
      </Button>

      </form>
    </main>
  )
}
