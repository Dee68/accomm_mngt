import countries from "i18n-iso-countries";
import en from "i18n-iso-countries/langs/en.json";

countries.registerLocale(en);
// export const COUNTRY_NAMES: Record<string, string> = {
//   IE: "Ireland",
//   GB: "United Kingdom",
//   US: "United States",
//   NG: "Nigeria",
//   PL: "Poland",
//   UA: "Ukraine",
//   RU: "Russia",
//   DE: "Germany"
//   // ...other ones later
// };
export const COUNTRY_OPTIONS = Object.entries(
    countries.getNames("en", { select: "official" })
).map(([code, name]) => ({ code, name }))
 .sort((a, b) => a.name.localeCompare(b.name));

export function countryName(code?: string | null): string {
    if (!code) return "";
    return countries.getName(code, "en") ?? code.toUpperCase();
}