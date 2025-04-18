import type { Config } from "tailwindcss";
//import animate from 'tailwindcss-animate'
import animate from "./node_modules/tailwindcss-animate";
import { openSans, robotoSlab } from "./lib/fonts";


const config: Config = {
    darkMode: ["class"],
    content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
  	extend: {
  		backgroundImage: {
  			'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
  			'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))'
  		},
  		borderRadius: {},
  		colors: {},
      fontFamily: {
        openSans: ["var(--font-openSans)"],
        robotoSlab: ["var(--font-robotoSlab)"]
      }
		
  	}
  },
  plugins: [animate],
} satisfies Config;
export default config;
