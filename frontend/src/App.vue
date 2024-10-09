<template>
    <n-config-provider :key="store.theme" :theme="store.theme" :locale="zhCN" :date-locale="dateZhCN">
        <n-notification-provider>
            <n-message-provider>
                <n-loading-bar-provider>
                    <h1>ReviveIt</h1>
                    <TopMenu />
                    <router-view />
                    <SwitchTheme :left="100" :buttom="100"/>
                    <n-back-top :right="100" />
                </n-loading-bar-provider>
            </n-message-provider>
        </n-notification-provider>
    </n-config-provider>
</template>

<script setup>
import { useOsTheme, darkTheme, NMessageProvider, NNotificationProvider, zhCN, dateZhCN } from 'naive-ui';
import { useStore } from '@/store';
import { computed } from 'vue';
import TopMenu from '@/components/TopMenu.vue';
import SwitchTheme from '@/components/SwitchTheme.vue';
const osThemeRef = useOsTheme();
const store = useStore();
// const theme = computed(() => (osThemeRef.value === 'dark' ? darkTheme : null));
store.theme = osThemeRef.value === 'dark' ? darkTheme : null;
</script>

<style scoped src="@/assets/css/styles.css"></style>