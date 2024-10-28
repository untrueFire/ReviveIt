<template>
    <nav class="top-menu">
        <h1>ReviveIt</h1>
        <n-menu mode="horizontal" responsive :options="menuOptions" />
    </nav>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import NotificationButton from './NotificationButton.vue'
import { useStore } from '../stores'
import { h, computed } from 'vue'
import { useMessage } from 'naive-ui'
import SwitchTheme from './SwitchTheme.vue'
const store = useStore()
window.$message = useMessage()
const menuOptions = computed(() => [
    {
        label: () =>
            h(
                RouterLink,
                {
                    to: {
                        name: 'Home',
                    },
                },
                { default: () => '广场' },
            ),
        key: 'home',
    },
    {
        label: () =>
            h(
                RouterLink,
                {
                    to: {
                        name: 'Auth',
                    },
                },
                { default: () => '登录/注册' },
            ),
        key: 'auth',
        show: !store.isLoggedIn,
    },
    {
        label: () =>
            h(
                RouterLink,
                {
                    to: {
                        name: 'User',
                    },
                },
                { default: () => '我的' },
            ),
        key: 'user',
        show: store.isLoggedIn,
    },
    {
        label: () => h(NotificationButton),
        key: 'notification',
        show: store.isLoggedIn,
    },
    {
        label: () =>
            h(
                RouterLink,
                {
                    to: {
                        name: 'Logout',
                    },
                },
                { default: () => '登出' },
            ),
        key: 'logout',
        show: store.isLoggedIn,
    },
    {
        label: () =>
            h(
                RouterLink,
                {
                    to: {
                        name: 'AddItem',
                    },
                },
                { default: () => '添加物品' },
            ),
        key: 'addItem',
        show: store.isLoggedIn,
    },
    {
        label: () =>
            h(
                RouterLink,
                {
                    to: {
                        name: 'WoodenFish',
                    },
                },
                { default: () => '木鱼' },
            ),
        key: 'woodenFish',
        show: store.isLoggedIn,
    },
    {
        label: () => h(SwitchTheme),
        key: 'switchTheme',
    },
])
</script>

<style scoped>
.top-menu {
    margin: 10px;
    display: flex;
}

.top-menu a {
    font-size: 16px;
}

:global(.v-overflow) {
  justify-content: flex-end;
}
</style>
