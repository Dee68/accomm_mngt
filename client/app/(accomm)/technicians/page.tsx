import React from 'react'
import type { Metadata } from 'next'
import TechnicianCard from '@/components/cards/TechnicianCard'

export const metadata:Metadata = {
    title:"Accommodation Center | Technicians",
    description:"Authenticated user can see technicians,what they are specialize in and their ratings"
}

export default function TechniciansPage() {
  return (
    <>
     <TechnicianCard /> 
    </>
  )
}
