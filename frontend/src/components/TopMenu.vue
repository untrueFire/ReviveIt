<template>
    <nav class="top-menu">
        <h1 @click="router.push('/')">ReviveIt</h1>
        <n-menu mode="horizontal" responsive :options="menuOptions" />
    </nav>
</template>

<script setup lang="ts">
import { useRouter, RouterLink } from 'vue-router'
import NotificationButton from './NotificationButton.vue'
import { useStore } from '../stores'
import { logout } from '../utils/api'
import { h, computed } from 'vue'
import { NButton, useMessage } from 'naive-ui'
import SwitchTheme from './SwitchTheme.vue'

const router = useRouter()
const store = useStore()
const message = useMessage()
window.$message = message

function handleLogout() {
    logout()
        .then(() => {
            store.user = undefined
            router.push({ name: 'Auth' })
        })
        .catch(() => message.error('登出失败'))
}
const menuOptions = computed(() => [
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
                        name: 'Admin',
                    },
                },
                { default: () => '管理' },
            ),
        key: 'admin',
        show: store.isLoggedIn && store.user?.group === 'admin',
    },
    {
        label: () =>
            h(
                NButton,
                {
                    onclick: handleLogout,
                    text: true,
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
