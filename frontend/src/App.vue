<template>
    <n-config-provider
        :theme="store.theme"
        :locale="zhCN"
        :date-locale="dateZhCN"
    >
        <n-global-style />
        <n-notification-provider>
            <n-message-provider>
                <n-loading-bar-provider>
                    <TopMenu />
                    <router-view />
                    <n-back-top />
                </n-loading-bar-provider>
            </n-message-provider>
        </n-notification-provider>
    </n-config-provider>
</template>

<script setup lang="ts">
import { zhCN, dateZhCN } from 'naive-ui'
import { useThemeStore } from './stores'
const store = useThemeStore()
</script>
