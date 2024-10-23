import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import AutoImport from 'unplugin-auto-import/vite';
import Components from 'unplugin-vue-components/vite';
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers';

export default defineConfig({
  server: {
    port: 80,
    proxy: {
      '^/api|accounts/.*': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    },
    historyApiFallback: true,
  },
  plugins: [
    vue(),
    AutoImport({
      resolvers: [NaiveUiResolver()],
      dts: true
    }),
    Components({
      resolvers: [NaiveUiResolver()],
      dts: true
    }),
  ],
})
