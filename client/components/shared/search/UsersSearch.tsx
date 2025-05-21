"use client";

import { Input } from "@/components/ui/input";
import { useAppDispatch, useAppSelector } from "@/lib/redux/hooks/typedHooks";
import Image from "next/image";
//import { setSearchTerm } from "@/lib/redux/features/users/usersApiSlice";

const UsersSearch = ()=>{
    const dispatch = useAppDispatch();
    //const searchTerm = useAppSelector((state)=>state.user.searchTerm)
    return (
        <div className="flex min-h-[56px] bg-gray dark:bg-eerieBlack mb-3 w-full grow rounded-full">
            <Image 
                src="/assets/icons/search.svg"
                alt="Search" 
                width={24} 
                height={24} 
                className="mx-3"
            />
            <Input 
                placeholder="Search by username, first or last name" 
                type="search" 
                value='' 
                className="search-text no-focus dark:text-babyPowder border-none bg-transparent shadow-none outline-none"
            />

        </div>
    );
};

export default UsersSearch;