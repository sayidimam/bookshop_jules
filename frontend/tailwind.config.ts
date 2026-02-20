import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#006A4E", // Deep Emerald
          foreground: "#FFFFFF",
        },
        secondary: {
          DEFAULT: "#F4F4F5",
          foreground: "#18181B",
        },
        accent: {
          DEFAULT: "#FF6B6B", // Red for Sale
          foreground: "#FFFFFF",
        }
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'sans-serif'],
        bengali: ['var(--font-hind)', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
export default config;
