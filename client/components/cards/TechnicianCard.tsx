"use client";

import { useGetAllTechniciansQuery } from "@/lib/redux/features/users/usersApiSlice";
import { useAppSelector } from "@/lib/redux/hooks/typedHooks";
//import { UserState } from "@/types";
import { useTheme } from "next-themes";
import Spinner from "../shared/Spinner";
import UsersSearch from "../shared/search/UsersSearch";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../ui/card";
import { Avatar, AvatarImage } from "../ui/avatar";
import { BrickWall } from "lucide-react";
import TechnicianCardDetails from "./TechnicianCardDetails";
import PaginationSection from "../shared/PaginationSection";
import { Button } from "../ui/button";
import Link from "next/link";

export default function TechnicianCard() {
    const {theme} = useTheme();
    const searchTerm = useAppSelector((state)=>state.user.searchTerm);
    const page = useAppSelector((state)=>state.user.page);
    const {data, isLoading} = useGetAllTechniciansQuery({searchTerm, page});
    const technicians = data?.non_tenant_profiles;
    const totalCount = technicians?.count || 0;
    const totalPages = Math.ceil(totalCount / 9);
    console.log("FULL API RESPONSE:", data);
    console.log("NON-TENANT PROFILES:", data?.non_tenant_profiles);
    if (isLoading) {
        return (
            <div className="flex-center pt-32">
             <Spinner size="xl"/>
            </div>
        );
        
    }

    return (
       
        <div>
            <UsersSearch />
            <h1 className="flex-center font-robotoSlab dark:text-pumpkin text-4xl sm:text-5xl">All technicians - ({technicians?.results.length})</h1>
              <div className='mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 cursor-pointer'>
                {technicians && technicians.results.length > 0 ? (
                    technicians.results.map((technician)=>(
                        <Card key={technician.id}>
                            <CardContent className='rounded-lg p-4'>
                                <CardHeader className='flex-col-center text-center w-full'>
                                    <Avatar className='border-pumpkin mx-auto size-28 overflow-hidden rounded-full border-4 object-cover'>
                                     <AvatarImage 
                                     alt='User profile avatar' 
                                     src={technician.avatar || (theme==='dark'? '/assets/icons/user-profile-circle.svg':'/assets/icons/user-profile-light-circle.svg')}
                                     />
                                    </Avatar>
                                    <CardTitle className="flex-center h2-semibold font-robotoSlab dark:text-pumpkin">
                                    {technician.full_name}
                                    </CardTitle>
                                </CardHeader>
                                
                                <CardTitle className='flex-center'>
                                    <p className='h4-semibold dark:text-lime-500'>@{technician.username}</p>
                                </CardTitle>
                                <CardDescription className='mt-4 space-y-2 border-b-0'>
                                
                                        <TechnicianCardDetails 
                                            country_of_origin = {technician.country_of_origin}
                                            occupation = {technician.occupation}
                                            date_joined = {technician.date_joined}
                                            average_rating = {technician.average_rating}
                                        />
                                       
                                    
                                </CardDescription>
                                <div className="flex-center">
                                <Link href={`/add-rating?username=${technician.username}`}>
                                 <Button size="sm" className="electricIndigo-gradient text-babyPowder mt-3">
                                 Give me a rating
                                 </Button>
                                </Link>
                                </div>
                            </CardContent>
                        </Card>
                    ))
                ):(<p className="h2-semibold dark:text-lime-500">No technician(s) found!</p>)}
            </div>
            <PaginationSection totalPages={totalPages} entityType='user'/>

        </div>
        
    );
}
