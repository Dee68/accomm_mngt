"use client";
import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import React from 'react'
import { useParams, useRouter } from "next/navigation";
import { useResetPasswordConfirmMutation } from "@/lib/redux/features/auth/authApiSlice";
import { useForm } from "react-hook-form";
import { passwordResetConfirmSchema, TPasswordResetConfirmSchema } from "@/lib/validationSchemas";
import { toast } from "react-toastify";
import { extractErrorMessage } from "@/utils";
import { FormFieldComponent } from "@/components/shared/forms/FormFieldComponent";
import { Button } from "@/components/ui/button";
import Spinner from "@/components/shared/Spinner";

export default function PasswordResetConfirmForm() {
    const router = useRouter();
    const {uid,token} = useParams();
    const [resetPasswordConfirm, {isLoading}] = useResetPasswordConfirmMutation();

    const {register,handleSubmit,reset,formState:{errors}} = useForm<TPasswordResetConfirmSchema>({
        resolver: zodResolver(passwordResetConfirmSchema),
        mode: "all",
        defaultValues:{
            uid: uid as string,
            token: token as string,
            new_password: "",
            re_new_password: ""
        },
    });
    const onSubmit = async (values: z.infer<typeof passwordResetConfirmSchema>) => {
        try {
            await resetPasswordConfirm({...values,uid: uid as string,token: token as string}).unwrap();
            router.push("/login")
            toast.success("Your password was reset successfully.");
            reset();
            
        } catch (e) {
            const errorMessage = extractErrorMessage(e);
            toast.error(errorMessage || "An error occurred.");
        }
    }
  return (
    <main>
        <form 
            noValidate 
            onSubmit={handleSubmit(onSubmit)} 
            className="flex w-full flex-col gap-4 max-w-md">
         <FormFieldComponent 
            label="New Password" 
            name="new_password" 
            register={register} 
            errors={errors} 
            placeholder="New Password"
            isPassword={true}/>

            <FormFieldComponent 
            label="Confirm Password" 
            name="re_new_password" 
            register={register} 
            errors={errors} 
            placeholder="Confirm Password"
            isPassword={true}/>

            <Button 
                type="submit" 
                disabled={isLoading} 
                className="h4-semibold bg-eerieBlack dark:bg-pumpkin w-full text-white">
                {isLoading ? <Spinner size="sm" /> : `Confirm New Password`}
            </Button>
        </form>
      
    </main>
  )
}
