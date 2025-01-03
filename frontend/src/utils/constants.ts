/**
 * Stores common-used functions to reduce duplication
 */
import type { ValidateError } from 'async-validator'
import { NTag, type FormValidationError } from 'naive-ui'
import { h, reactive } from 'vue'
import MarkdownIt from 'markdown-it'
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

export const tagTypes = ['info', 'success', 'warning', 'error'] as const

/**
 * Pick a random element from `arr`.
 * @param arr A readonly array.
 * @returns A random element from `arr`.
 */
export function choice<T>(arr: readonly T[]): T {
    const randomIndex = Math.floor(Math.random() * arr.length)
    return arr[randomIndex]
}

/**
 * A wrapper for the render function for tags
 * using the above functions
 *
 * TODO: Decoupling the model
 * @param model the form model that contains the tags
 * @returns a render function that renders the tags
 */
export function renderTag(model: {
    name: string
    tags: string[]
    description: string
    contactInfo: string
}) {
    function render(tag: string, index: number) {
        return h(
            NTag,
            {
                type: randomTagType(),
                closable: true,
                bordered: false,
                onClose: () => {
                    model.tags.splice(index, 1)
                },
            },
            () => tag,
        )
    }
    return render
}

/**
 * General error handler form `NForm`.
 *
 * Shows each error using `NMessage`
 * @param error `FormValidationError[]`
 */
export function handleFormError(error: FormValidationError[]) {
    const message = window.$message
    error.forEach(field => {
        field.forEach((err: ValidateError) => message.error(`${err.message}`))
    })
}

/**
 * Storing the available tags
 * that hasn't been used recently
 */
let availableTags = [...tagTypes]
/**
 * Get a random tag type with maximum repetition period
 * @returns one of the tag types
 */
export function randomTagType() {
    if (availableTags.length === 0) {
        availableTags = [...tagTypes]
    }
    const randomIndex = Math.floor(Math.random() * availableTags.length)
    const selectedTag = availableTags[randomIndex]
    availableTags.splice(randomIndex, 1)

    return selectedTag
}

/**
 * Default error handler for `md-editor-v3`
 * @param err
 */
export function onError(err: {
    name: 'Cropper' | 'fullscreen' | 'prettier' | 'overlength'
    message: string
}) {
    window.$message.error(err.message)
}

export const groupTable = {
    admin: '管理员',
    user: '正式用户',
    guest: '临时用户',
}

// 提取纯文本的函数
export function removeMd(markdown: string): string {
    const md = new MarkdownIt()
    const html = md.render(markdown)
    const plainText = html.replace(/<[^>]+>/g, '')
    return plainText
}
