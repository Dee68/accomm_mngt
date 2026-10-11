"use client";

import { Control, Controller } from "react-hook-form";
import { TProfileSchema } from "@/lib/validationSchemas";
import { COUNTRY_OPTIONS } from "@/lib/countries";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

interface CountrySelectFieldProps {
    control: Control<TProfileSchema>;
}

export default function CountrySelectField({ control }: CountrySelectFieldProps) {
    return (
        <div className="flex flex-col gap-1">
            <label className="h4-semibold dark:text-babyPowder">
                Country of Origin
            </label>
            <Controller
                name="country_field"
                control={control}
                render={({ field }) => (
                    <Select
                        value={field.value ?? ""}
                        onValueChange={field.onChange}
                    >
                        <SelectTrigger className="dark:border-platinum">
                            <SelectValue placeholder="Select a country" />
                        </SelectTrigger>
                        <SelectContent className="max-h-64">
                            {COUNTRY_OPTIONS.map(({ code, name }) => (
                                <SelectItem key={code} value={code}>
                                    {name}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                )}
            />
        </div>
    );
}