<template>
    <n-badge dot :show="store.unreadCount > 0">
        <router-link to="/notifications">消息</router-link>
    </n-badge>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import { useStore } from '../stores'
import { updateUnread } from '../utils/api'
const store = useStore()

onMounted(() => {
    store.intervalId = setInterval(updateUnread, 30000)
    updateUnread()
})

onUnmounted(() => {
    clearInterval(store.intervalId)
})
</script>
