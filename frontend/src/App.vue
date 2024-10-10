<template>
    <n-config-provider :key="store.theme" :theme="store.theme" :locale="zhCN" :date-locale="dateZhCN">
        <n-notification-provider>
            <n-message-provider>
                <n-loading-bar-provider>
                    <h1>ReviveIt</h1>
                    <!-- <n-affix :top="100">
                        <SwitchTheme style="position: fixed; right: 40px"/>
                    </n-affix> -->
                    <TopMenu />
                    <router-view />
                    <n-back-top />
                </n-loading-bar-provider>
            </n-message-provider>
        </n-notification-provider>
    </n-config-provider>
</template>

<script setup>
import { useOsTheme, darkTheme, NMessageProvider, NNotificationProvider, zhCN, dateZhCN } from 'naive-ui';
import { useStore } from '@/store';
// import { computed } from 'vue';
import TopMenu from '@/components/TopMenu.vue';
import SwitchTheme from '@/components/SwitchTheme.vue';
const osThemeRef = useOsTheme();
const store = useStore();
// store.theme = osThemeRef.value === 'dark' ? darkTheme : null;
</script>

<style scoped src="@/assets/css/styles.css"></style>