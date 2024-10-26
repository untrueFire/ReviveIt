import { reactive } from 'vue'
/**
 * Default pager used in this project
 */
export const pagination = reactive({
    page: 1,
    pageSize: 20,
    showSizePicker: true,
    pageSizes: [10, 20, 50, 100],
    onChange: (page: number) => {
        pagination.page = page
    },
    onUpdatePageSize: (pageSize: number) => {
        pagination.pageSize = pageSize
        pagination.page = 1
    },
})

export const tagTypes = [
    'default',
    'primary',
    'info',
    'success',
    'warning',
    'error',
] as const

/**
 * Pick a random element from `arr`.
 * @param arr A readonly array.
 * @returns A random element from `arr`.
 */
export function choice<T>(arr: readonly T[]): T {
    const randomIndex = Math.floor(Math.random() * arr.length)
    return arr[randomIndex]
}
