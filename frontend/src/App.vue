<template>
    <n-config-provider :theme="store.theme" :locale="zhCN" :date-locale="dateZhCN">
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

<script setup>
import { zhCN, dateZhCN, useOsTheme, darkTheme } from 'naive-ui';
import { useStore } from './store';
const osThemeRef = useOsTheme();
const store = useStore();
store.theme = osThemeRef.value === 'dark' ? darkTheme : null;
</script>
