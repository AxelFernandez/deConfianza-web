import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { loadEnv } from 'vite'
import { resolve } from 'path'

export default defineConfig(({ mode }) => {
  // Cargar variables de entorno según el modo
  const env = loadEnv(mode, process.cwd(), '');
  
  return {
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    host: true,
    port: 5173,
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      'test.deconfianza.com.ar',
      'deconfianza.com.ar',
      'www.deconfianza.com.ar'
    ],
    watch: {
      usePolling: true
    }
  }
  };
})
