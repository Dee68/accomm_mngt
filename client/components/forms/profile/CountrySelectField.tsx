"use client";

import { countryOptions } from "@/constants";
import { TProfileSchema } from "@/lib/validationSchemas";
import Select from "react-select";
import { Map } from "lucide-react";
import dynamic from "next/dynamic";
import React from "react";
import { Control, Controller } from "react-hook-form";
import customStyles from "../selectStyles";

const ClientOnly = dynamic<{ children: React.ReactNode }>(
    () => Promise.resolve(({ children }) => <>{children}</>),
    { ssr: false }
);

interface CountrySelectFieldProps {
    control: Control<TProfileSchema>;
}

export default function CountrySelectField({ control }: CountrySelectFieldProps) {
    return (
        <div>
            <label htmlFor="country_field" className="h4-semibold dark:text-babyPowder">
                Country of Origin
            </label>
            <div className="mt-1 flex items-center space-x-3">
                <Map className="dark:text-babyPowder size-8" />
                <ClientOnly>
                    <Controller
                        control={control}
                        name="country_field"
                        render={({ field }) => (
                            <Select
                                className="mt-1 w-full"
                                {...field}
                                options={countryOptions}
                                value={countryOptions.find(
                                    (option) => option.value === field.value
                                )}
                                onChange={(option) => field.onChange(option?.value)}
                                instanceId="country-select"
                                styles={customStyles}
                            />
                        )}
                    />
                </ClientOnly>
            </div>
        </div>
    );
}