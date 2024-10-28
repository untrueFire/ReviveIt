<template>
    <n-icon @click="toggleTheme">
        <LightModeFilled v-if="store.themeName === 'dark'" />
        <DarkModeFilled v-else />
    </n-icon>
</template>

<script setup lang="ts">
import { useThemeStore } from '../stores'
import { LightModeFilled, DarkModeFilled } from '@vicons/material'
const store = useThemeStore()
const toggleTheme = () => {
    if (store.themeName !== 'dark') {
        store.themeName = 'dark'
    } else {
        store.themeName = 'light'
    }
}
</script>
