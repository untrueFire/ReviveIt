/**
 * Stores api-related functions
 */
import axios, { AxiosError, type AxiosRequestConfig } from 'axios'
import { useStore } from '@/stores'

/**
 * Retrieve the value of a cookie from `document.cookie` string
 * @param name name of the cookie to get
 * @returns value of the cookie if found, `null` if not found
 */
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

/**
 * Get csrf token in cookie,
 * fetch it first if not found
 * @returns `csrftoken` in cookie
 */
export async function getCsrftoken() {
    if (!document.cookie.includes('csrftoken')) {
        await get('/accounts/login')
    }
    return getCookie('csrftoken')
}

/**
 * Error handler for expired login status
 *
 * Redirect to login page when visiting
 * pages that require login without login status
 * @param error
 */
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
            return
        }
        store.user = undefined
        const message = window.$message
        message.error('登录失效')
        clearInterval(store.intervalId)
        window.location.href = '/auth'
    } else {
        throw error
    }
}

/**
 * Wrapper for `axios.get` function
 * using `withCredentials: true` to
 * handle cross region
 * @param url the url to visit
 * @returns `response.data`
 */
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

/**
 * Wrapper function for `axios.post`
 * with the `X-CSRFToken` header from cookie
 * @param url the url to visit
 * @param data the data to post
 * @returns `response.data`
 */
export async function post(
    url: string,
    data: string | object | null = null,
    config?: AxiosRequestConfig<string | object | null> | undefined,
) {
    const basicConfig = {
        withCredentials: true,
        headers: {
            'X-CSRFToken': await getCsrftoken(),
        },
    }
    config = {
        ...config,
        ...basicConfig,
        headers: {
            ...config?.headers,
            ...basicConfig.headers,
        },
    }
    try {
        const response = await axios.post(url, data, config)
        return response.data
    } catch (error) {
        errorHandler(error as Error)
    }
}

export async function uploadFiles(file: File): Promise<string> {
    const form = new FormData()
    form.append('file', file)
    return post('/api/file/upload/', form, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    }).then(data => data.url)
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

/**
 * Fetch and set unread notifications
 */
export const updateUnread = () => {
    fetchUnread()
        .then(data => {
            const store = useStore()
            store.unreadNotifications = data
        })
        .catch(() => {})
}

/**
 * Fetch and set read notifications
 */
export const updateRead = () => {
    fetchRead()
        .then(data => {
            const store = useStore()
            store.readNotifications = data
        })
        .catch(() => {})
}

/**
 * Fetch and set user info
 */
export const updateUser = async () => {
    const store = useStore()
    store.user = await fetchUserInfo()
}
