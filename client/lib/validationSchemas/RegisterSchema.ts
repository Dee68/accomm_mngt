import *  as z from "zod";

const usernameRegex = /^[a-zA-Z0-9_@+.-]+$/;

export const registerUserSchema = z.object({
    username:z.string().regex(usernameRegex,{
        message:"Usernames can only contain letters(lowercase and uppercase), digits,_, @, +,., and -",  
    }),
    first_name: z.string().trim().min(2,{
        message:"First name must be a minimum of 2 characters long.",
    }).max(50,{
        message:"First name can not be more than 50 characters long."
    }),
    last_name: z.string().trim().min(2,{
        message:"Last name must be a minimum of 2 characters long.",
    }).max(50,{
        message:"Last name can not be more than 50 characters long."
    }),
    email:z.string().trim().email({message:"Please enter a valid email address."}),
    password:z.string().min(8,{message:"Password must be at least 8 characters long."}),
    re_password:z.string().min(8,{message:"Confirm Password must be a minimum of 8 characters."})
}).refine((data)=> data.password === data.re_password,{
    message:"Passwords must match.",
    path:["re_password"]
});

export type TRegisterUserSchema = z.infer<typeof registerUserSchema>;