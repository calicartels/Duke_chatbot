import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
// import tailwindcss from '@tailwindcss/postcss'; // Removed
// import autoprefixer from 'autoprefixer'; // Removed

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // css: { // Removed explicit PostCSS config
  //   postcss: {
  //     plugins: [
  //       tailwindcss('./tailwind.config.cjs'),
  //       autoprefixer,
  //     ],
  //   },
  // },
}); 