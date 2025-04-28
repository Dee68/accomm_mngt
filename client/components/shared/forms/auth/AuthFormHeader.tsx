import { HomeModernIcon } from "@heroicons/react/24/solid";

import React from 'react';
import Link from "next/link";
import { strict } from "assert";

type FormHeaderProps = {
    title?: string,
    staticText?: string,
    linkText?: string,
    linkHref?: string
}

export default function AuthFormHeader({title,staticText,linkText,linkHref}:FormHeaderProps) {
  return (
    <div className="px-4 sm:mx-auto sm:w-full sm:max-w-md sm:px-6 lg:px-8">
      <HomeModernIcon className="mx-auto size-16 dark:text-lime-500" />
      <h2 className="text-baby_richBlack font-robotoSlab h2-bold dark:text-pumpkin mt-3 text-center">{title}</h2>
      {(staticText || linkText) && linkHref && (
        <p className="dark:text-platinum text-center mt-4 text-lg">
            {staticText && <span>{staticText}</span>}
            {linkText && (
                <Link href={linkHref} className="font-semibold text-indigo-600 hover:text-indigo-500 dark:text-lime-500 dark:hover:text-indigo-500 ml-1">
                    {linkText}
                </Link>
            )}
        </p>
      )}
    </div>
  )
}
