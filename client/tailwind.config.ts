import type { Config } from "tailwindcss";
import animate from "./node_modules/tailwindcss-animate";
import { openSans, robotoSlab } from "./lib/fonts";


const config: Config = {
    darkMode: ["class"],
    content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  prefix: "",
  theme: {
    container: {
			center: true,
			padding: "2rem",
			screens: {
				"2xl": "1400px",
			},
    },
  extend: {
			colors: {
				googleBlue: "#4285F4",
				asparagus: "#60992D",
				deepBlueGrey: "#263238",
				gray: "rgba(125,144,201,0.34)",
				lightGray: "#7B8EC8",
				electricIndigo: "#6610F2",
				richBlack: "#0D1317",
				veryBlack: "#000000",
				babyPowder: "#FBFEF9",
				pumpkin: "#F17105",
				platinum: "#DDE1E4",
				lightGrey: "#EEEEEE",
				pear: "#C2E812",
				eerieBlack: "#171D1C",
				ballonWhite: "#dfe6f6",
			},
    keyframes: {
				"accordion-down": {
					from: { height: "0" },
					to: { height: "var(--radix-accordion-content-height)" },
				},
				"accordion-up": {
					from: { height: "var(--radix-accordion-content-height)" },
					to: { height: "0" },
				},
			},
			animation: {
				"accordion-down": "accordion-down 0.2s ease-out",
				"accordion-up": "accordion-up 0.2s ease-out",
			},
			fontFamily: {
				openSans: ["var(--font-openSans)"],
				robotoSlab: ["var(--font-robotoSlab)"],
			},
		},
	},
  	
  plugins: [animate],
} satisfies Config;
export default config;
