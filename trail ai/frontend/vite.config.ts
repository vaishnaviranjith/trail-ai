import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/trip': 'http://127.0.0.1:8000',
      '/trips': 'http://127.0.0.1:8000',
      '/pois': 'http://127.0.0.1:8000',
      '/budget': 'http://127.0.0.1:8000',
      '/destinations': 'http://127.0.0.1:8000',
      '/health': 'http://127.0.0.1:8000',
      '/auth': 'http://127.0.0.1:8000',
      '/places': 'http://127.0.0.1:8000',
    }
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  }
});
