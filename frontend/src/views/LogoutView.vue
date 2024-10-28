<template>
    <div>
        <h1>登出</h1>
        <p>你确定要登出吗？</p>
        <n-button
            @click="handleLogout"
            type="error"
            round
            style="padding: 10px 20px"
            >确定</n-button
        >
    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { logout } from '../utils/api'
import { useStore } from '../stores'
import { useMessage } from 'naive-ui'
const store = useStore()
const router = useRouter()
const message = useMessage()
async function handleLogout() {
    try {
        await logout()
        store.user = undefined
        router.push({ name: 'Auth' })
    } catch {
        message.error('登出失败')
    }
}
</script>
