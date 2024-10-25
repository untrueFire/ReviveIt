<template>
    <n-icon @click="toggleTheme">
        <LightModeFilled v-if="store.theme !== null" />
        <DarkModeFilled v-else />
    </n-icon>
</template>

<script setup lang="ts">
import { useThemeStore } from '../stores'
import { LightModeFilled, DarkModeFilled } from '@vicons/material'
import { darkTheme } from 'naive-ui'
const store = useThemeStore()
const toggleTheme = () => {
    if (store.theme !== null) {
        store.theme = null
    } else {
        store.theme = darkTheme
    }
}
</script>
