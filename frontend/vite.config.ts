import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // Recharts es una librería grande, el aviso de tamaño no aplica para este proyecto
    chunkSizeWarningLimit: 1000,
  },
})
