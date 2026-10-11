export const COUNTRY_NAMES: Record<string, string> = {
  IE: "Ireland",
  GB: "United Kingdom",
  US: "United States",
  NG: "Nigeria",
  PL: "Poland",
  UKR: "Ukraine",
  RUS: "Russia",
  GER: "Germany"
  // ...other ones later
};

export function countryName(code?: string): string {
  if (!code) return "";
  return COUNTRY_NAMES[code.toUpperCase()] ?? code;
}