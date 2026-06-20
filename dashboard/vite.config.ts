import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/history': 'http://localhost:8000',
      '/quote': 'http://localhost:8000',
      '/info': 'http://localhost:8000',
      '/indicators': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
    },
  },
})
