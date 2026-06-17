import { defineConfig } from 'vite'

export default defineConfig({
    server: {
      host: '0.0.0.0',
      port: 5173,
      proxy: {
        '/start': 'http://localhost:8000',
        '/connect': {
          target: 'ws://localhost:8000',
          ws: true,
        }
      }
    }
  })