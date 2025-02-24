import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import path from "path"
import frappeui from "frappe-ui/vite"

export default defineConfig({
  plugins: [vue(), frappeui()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  build: {
    outDir: '../trg_marketing/public/frontend',
    emptyOutDir: true,
    sourcemap: true,
    target: 'esnext',
  },
  optimizeDeps: {
    include: ['frappe-ui', 'feather-icons']
  }
})