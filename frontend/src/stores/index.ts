import { ref, computed, type Ref } from 'vue'
import { defineStore, type StoreDefinition } from 'pinia'
import type { BuiltInGlobalTheme } from 'naive-ui/es/themes/interface'
import type { Notification, User } from '../types/Api'

/**
 * Separate definition for global theme.
 *
 * Because its type is too long,
 * we must manually annotate it
 */
type themeRef = Ref<BuiltInGlobalTheme | null, BuiltInGlobalTheme | null>
export const useThemeStore: StoreDefinition<
    'theme',
    Pick<{ theme: themeRef }, 'theme'>
> = defineStore('theme', () => {
    const theme = ref<BuiltInGlobalTheme | null>(null)
    return { theme }
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
