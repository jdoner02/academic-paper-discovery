/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Academic research color palette
        'research-blue': '#1e40af',
        'concept-purple': '#7c3aed',
        'evidence-green': '#059669',
        'paper-gray': '#6b7280',
      },
      fontFamily: {
        'academic': ['Georgia', 'serif'],
        'interface': ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

