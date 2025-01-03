import { ref, computed, watchEffect } from 'vue'
import { defineStore } from 'pinia'
import type { Notification, User } from '@/types/Api'
import { darkTheme, lightTheme, useOsTheme } from 'naive-ui'

/**
 * Separate definition for global theme.
 */
export const useThemeStore = defineStore('theme', () => {
    const osThemeRef = useOsTheme()
    const themeName = ref(
        localStorage.getItem('theme') || osThemeRef.value || 'auto',
    )
    const theme = computed(() =>
        themeName.value === 'dark' ? darkTheme : lightTheme,
    )
    watchEffect(() => {
        localStorage.setItem('theme', themeName.value)
    })
    return { themeName, theme }
})

/**
 * Default store for login status and notifications
 */
export const useStore = defineStore('main', () => {
    const unreadNotifications = ref<Notification[]>([])
    const readNotifications = ref<Notification[]>([])
    const unreadCount = computed(() => {
        return unreadNotifications.value.length
    })
    const intervalId = ref<ReturnType<typeof setInterval>>()
    const user = ref<User | undefined>()
    const isLoggedIn = computed(() => user.value !== undefined)
    return {
        unreadNotifications,
        readNotifications,
        unreadCount,
        intervalId,
        user,
        isLoggedIn,
    }
})
