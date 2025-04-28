"use client";

import * as z from "zod";
import {zodResolver} from "@hookform/resolvers/zod";
import {Contact2Icon,MailIcon,UserCheck2} from "lucide-react";
import { useRegisterUserMutation } from "@/lib/redux/features/auth/authApiSlice";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { registerUserSchema, TRegisterUserSchema } from "@/lib/validationSchemas";
import { extractErrorMessage } from "@/utils";
import { toast } from "react-toastify";
import { FormFieldComponent } from "@/components/shared/forms/FormFieldComponent";
import { Button } from "@/components/ui/button";
import Spinner from "../../Spinner";



export default function RegisterForm() {
    const [registerUser, {isLoading}] = useRegisterUserMutation();
    const router = useRouter();
    const {register,handleSubmit,formState:{errors},reset} = useForm<TRegisterUserSchema>({
        resolver: zodResolver(registerUserSchema),
        mode:"all",
        defaultValues:{
          username:"",
          first_name:"",
          last_name:"",
          email:"",
          password:"",
          re_password:""
        }
    })
    const onSubmit = async(values: z.infer<typeof registerUserSchema>)=>{
      try {
        await registerUser(values).unwrap();
        toast.success("An email with an activation link has been sent to your email address.Please check your email and activate your account.");
        router.push("/login");
        reset();
      } catch (e) {
        const errorMessage = extractErrorMessage(e);
        toast.error(errorMessage || "An error occurred")
      }
    }
  return (
    <main>
      <form noValidate onSubmit={handleSubmit(onSubmit)} className="flex w-full max-w-md flex-col gap-4">
      <FormFieldComponent 
        label="Username" 
        name="username" 
        register={register} 
        startIcon={<UserCheck2 className="dark:text-babyPowder size-8" />} 
        errors={errors} 
        placeholder="Username" 
      />
      <FormFieldComponent 
        label="First Name" 
        name="first_name" 
        register={register} 
        startIcon={<Contact2Icon className="dark:text-babyPowder size-8" />} 
        errors={errors} 
        placeholder="First Name" 
      />
      <FormFieldComponent 
        label="Last Name" 
        name="last_name" 
        register={register} 
        startIcon={<Contact2Icon className="dark:text-babyPowder size-8" />} 
        errors={errors} 
        placeholder="Last Name" 
      />
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
      />
      <FormFieldComponent 
        label="Confirm Password" 
        name="re_password" 
        register={register} 
        isPassword={true} 
        errors={errors} 
        placeholder="Confirm Password" 
      />
      <Button 
      type="submit" 
      className="h4-semibold bg-eerieBlack dark:bg-pumpkin text-white w-full" disabled={isLoading}>
        {isLoading ? <Spinner size="sm" /> : `Submit`}
        </Button>

    </form>
    </main>
  )
}
