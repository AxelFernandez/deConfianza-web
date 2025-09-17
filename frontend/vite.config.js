import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { loadEnv } from 'vite'

export default defineConfig(({ mode }) => {
  // Cargar variables de entorno según el modo
  const env = loadEnv(mode, process.cwd(), '');
  
  return {
  plugins: [vue()],
  server: {
    host: true,
    port: 5173,
    watch: {
      usePolling: true
    }
  }
  };
})
