import pluginVue from 'eslint-plugin-vue'
import vueTsEslintConfig from '@vue/eslint-config-typescript'
import pluginVitest from '@vitest/eslint-plugin'
import skipFormatting from '@vue/eslint-config-prettier/skip-formatting'

import { readFile } from "node:fs/promises";

const autoImportFile = new URL("./.eslintrc-auto-import.json", import.meta.url);
const autoImportGlobals = JSON.parse(await readFile(autoImportFile, "utf8"));

export default [
    {
        name: 'app/files-to-lint',
        files: ['**/*.{ts,mts,tsx,vue}'],
    },

    {
        name: 'app/files-to-ignore',
        ignores: ['**/dist/**', '**/dist-ssr/**', '**/coverage/**'],
    },

    ...pluginVue.configs['flat/essential'],
    ...vueTsEslintConfig(),

    {
        ...pluginVitest.configs.recommended,
        files: ['src/**/__tests__/*'],
    },
    skipFormatting,
    {
        languageOptions: {
            globals: {
                ...autoImportGlobals.globals,
            },
        },
    },
]
