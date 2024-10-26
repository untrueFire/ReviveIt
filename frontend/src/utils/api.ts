import axios, { AxiosError } from 'axios'
import { useStore } from '../stores'
function getCookie(name: string) {
    const cookies = document.cookie.split(';')
    for (let cookie of cookies) {
        cookie = cookie.trim()
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1)
        }
    }
    return null
}

export async function getCsrftoken() {
    if (!document.cookie.includes('csrftoken')) {
        await get('/accounts/login')
    }
    return getCookie('csrftoken')
}

function errorHandler(error: Error) {
    if (
        error instanceof AxiosError &&
        error.response &&
        error.response.status == 403 &&
        error.response.data &&
        error.response.data.detail == '身份认证信息未提供。'
    ) {
        const store = useStore()
        if (!store.isLoggedIn) {
            return undefined
        }
        store.user = undefined
        const message = window.$message
        message.error('登录失效')
        clearInterval(store.intervalId)
        window.location.href = '/login'
    } else {
        throw error
    }
}

export async function get(url: string) {
    try {
        const response = await axios.get(url, {
            withCredentials: true,
        })
        return response.data
    } catch (error) {
        errorHandler(error as Error)
    }
}

export async function post(url: string, data: string | object | null = null) {
    try {
        const response = await axios.post(url, data, {
            withCredentials: true,
            headers: {
                'X-CSRFToken': await getCsrftoken(),
            },
        })
        return response.data
    } catch (error) {
        errorHandler(error as Error)
    }
}

export const fetchUserInfo = () => get('/api/user/')
export const fetchUserItems = () => get('/api/user/items/')
export const deleteItem = (itemId: number) =>
    post(`/api/items/delete/${itemId}/`, '')
export const fetchItem = (itemId: number) => get(`/api/items/${itemId}/`)
export const updateItem = (itemId: number, itemData: PartialItem) =>
    post(`/api/items/update/${itemId}/`, itemData)
export const fetchUnread = () => get('/api/user/notifications/unread/')
export const fetchRead = () => get('/api/user/notifications/read/')
export const acceptNotification = (notificationId: number) =>
    post(`/api/notification/accept/${notificationId}/`, null)
export const rejectNotification = (notificationId: number) =>
    post(`/api/notification/reject/${notificationId}/`, null)
export const ReviveItem = (itemId: number, data: { price: number }) =>
    post(`/api/items/revive/${itemId}/`, data)
export const search = (query: string | number | boolean) =>
    get(`/api/items/search/?q=${encodeURIComponent(query)}`)
export const addItem = (itemData: PartialItem) =>
    post('/api/items/add/', itemData)
export const setRead = (notificationId: number) =>
    post(`/api/notification/read/${notificationId}/`, null)
export const logout = () => post('/accounts/logout/', null)

export const updateUnread = async () => {
    fetchUnread()
        .then(data => {
            const store = useStore()
            store.unreadNotifications = data
        })
        .catch(() => {})
}

export const updateRead = () => {
    fetchRead()
        .then(data => {
            const store = useStore()
            store.readNotifications = data
        })
        .catch(() => {})
}

export const updateUser = async () => {
    const store = useStore()
    store.user = await fetchUserInfo()
}
