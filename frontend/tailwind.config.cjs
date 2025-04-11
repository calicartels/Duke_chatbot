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
      },
    },
    plugins: [
      // require('@tailwindcss/typography'), // Temporarily removed
    ],
  }