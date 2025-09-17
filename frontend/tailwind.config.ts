import type { Config } from "tailwindcss";
export default {
    content: ["./index.html", "./src/**/*.{ts,tsx}"],
    theme: {
        extend: {
            colors: { primary: { DEFAULT: "#1e40af" } },
            borderRadius: { card: "0.75rem" }
        }
    },
    plugins: []
} satisfies Config;