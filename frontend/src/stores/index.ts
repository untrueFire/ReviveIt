import { ref, computed, type Ref } from 'vue'
import { defineStore, type StoreDefinition } from 'pinia'
import type { BuiltInGlobalTheme } from 'naive-ui/es/themes/interface'
import type { Notification, User } from '../types/Api'

export const useThemeStore: StoreDefinition<
    'theme',
    Pick<
        {
            theme: Ref<BuiltInGlobalTheme | null, BuiltInGlobalTheme | null>
        },
        'theme'
    >,
    Pick<
        {
            theme: Ref<BuiltInGlobalTheme | null, BuiltInGlobalTheme | null>
        },
        never
    >,
    Pick<
        {
            theme: Ref<BuiltInGlobalTheme | null, BuiltInGlobalTheme | null>
        },
        never
    >
> = defineStore('theme', () => {
    const theme = ref<BuiltInGlobalTheme | null>(null)
    return {
        theme,
    }
})

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
