import React from 'react'
import type { Metadata } from 'next'

export const metadata:Metadata = {
    title: "Accommodation Center | Welcome",
    description: "Welcome to the accommodation center website. This webapp allows users who are tenants to signup, create their profiles, report any issues with their apartments, report any tenant,post  anything of relevance for other tenants to see or respond."
}

export default function WelcomePage() {
  return (
    <div>
      <h1 className='dark:text-pumpkin text-6xl'>Welcome</h1>
    </div>
  )
}
