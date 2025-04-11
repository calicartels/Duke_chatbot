module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'duke-blue': '#00539B',
        'duke-navy': '#012169',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      boxShadow: {
        'inner-xl': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
      },
      animation: {
        'bounce-slow': 'bounce 3s infinite',
      },
      // Add explicit max-width configuration
      maxWidth: {
        '3xl': '48rem', // This is the default for max-w-3xl in Tailwind v3
        'none': 'none',
        'xs': '20rem',
        'sm': '24rem',
        'md': '28rem',
        'lg': '32rem',
        'xl': '36rem',
        '2xl': '42rem',
        '4xl': '56rem',
        '5xl': '64rem',
        '6xl': '72rem',
        '7xl': '80rem',
        'full': '100%',
        'min': 'min-content',
        'max': 'max-content',
        'prose': '65ch',
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}