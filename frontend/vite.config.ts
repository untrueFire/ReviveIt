import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'

// https://vite.dev/config/
export default defineConfig({
    server: {
        port: 80,
        proxy: {
            '^/api|accounts/.*': {
                target: 'http://localhost:8000',
                changeOrigin: true,
            },
        },
    },
    plugins: [
        vue(),
        vueDevTools(),
        AutoImport({
            // targets to transform
            include: [
                /\.[tj]sx?$/, // .ts, .tsx, .js, .jsx
                /\.vue$/,
                /\.vue\?vue/, // .vue
                /\.md$/, // .md
            ],
            imports: [
                'vue',
                'vue-router',
                {
                    'naive-ui': ['useMessage', 'useLoadingBar'],
                    axios: ['axios'],
                },
            ],
            // Enable auto import by filename for default module exports under directories
            defaultExportByFilename: true,
            // Auto import for module exports under directories
            // by default it only scan one level of modules under the directory
            dirs: [],
            // Filepath to generate corresponding .d.ts file.
            // Defaults to './auto-imports.d.ts' when `typescript` is installed locally.
            // Set `false` to disable.
            dts: './auto-imports.d.ts',
            vueTemplate: true,
            // Custom resolvers, compatible with `unplugin-vue-components`
            // see https://github.com/antfu/unplugin-auto-import/pull/23/
            resolvers: [NaiveUiResolver()],

            // Include auto-imported packages in Vite's `optimizeDeps` options
            // Recommend to enable
            viteOptimizeDeps: true,

            // Inject the imports at the end of other imports
            injectAtEnd: true,

            // Generate corresponding .eslintrc-auto-import.json file.
            // eslint globals Docs - https://eslint.org/docs/user-guide/configuring/language-options#specifying-globals
            eslintrc: {
                enabled: false, // Default `false`
                // provide path ending with `.mjs` or `.cjs` to generate the file with the respective format
                filepath: './.eslintrc-auto-import.json', // Default `./.eslintrc-auto-import.json`
                globalsPropValue: true, // Default `true`, (true | false | 'readonly' | 'readable' | 'writable' | 'writeable')
            },
        }),
        Components({
            resolvers: [NaiveUiResolver()],
            dts: true,
        }),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
        },
    },
})
