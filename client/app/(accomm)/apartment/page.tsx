import ApartmentCreateForm from "@/components/forms/apartment/ApartmentCreateForm"
import { AuthFormHeader } from "@/components/shared/forms/auth"
import type { Metadata } from "next"

const metadata:Metadata ={
    title:"Accommodation Center | Create apartment",
    description:"Authenticated user can add apartment details"
}

export default function AddApartmentPage() {
  return (
    <div>
      <AuthFormHeader 
        title="Add Your Apartment" 
        staticText="Want to go back?" 
        linkHref="/profile" 
        linkText="Back To Profile" 
      />
      <div className="mt-7 sm:mx-auto sm:w-full sm:max-w-[480px]">
        <div className="bg-lightGrey dark:bg-deepBlueGrey rounded-xl px-6 py-12 shadow sm:rounded-lg sm:px-12 md:rounded-3xl">
          <ApartmentCreateForm />
        </div>
      </div>
    </div>
  )
}
