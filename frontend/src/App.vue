<template>
    <n-config-provider :key="store.theme" :theme="store.theme" :locale="zhCN" :date-locale="dateZhCN">
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
import { useStore } from './store';
import TopMenu from './components/TopMenu.vue';
// const osThemeRef = useOsTheme();
const store = useStore();
// store.theme = osThemeRef.value === 'dark' ? darkTheme : null;
</script>
