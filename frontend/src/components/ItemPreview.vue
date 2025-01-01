<template>
    <div>
        <n-ellipsis style="max-width: 80%" :tooltip="false" :line-clamp="5">
            <template #tooltip></template>
            {{ remove_markdown(props.markdownContent).slice(0, 400) }}
        </n-ellipsis>
        <n-image-group show-toolbar-tooltip>
            <n-grid
                :x-gap="16"
                :y-gap="16"
                :cols="gridCols"
                style="width: 90%; margin: auto"
                @click.stop
            >
                <template v-for="(url, index) in displayedImages" :key="index">
                    <n-gi>
                        <div
                            class="image-container"
                            :class="{
                                'has-more': index === 8 && images.length > 9,
                            }"
                        >
                            <n-image
                                :src="url"
                                alt="图片"
                                show-toolbar-tooltip
                                object-fit="cover"
                                width="100%"
                                class="image"
                                ref="imgRef"
                            />
                            <div
                                v-if="index === 8 && images.length > 9"
                                class="overlay"
                                @click="imgRef?.slice(-1)[0].click();"
                            >
                                <span class="plus"
                                    >+{{ images.length - 9 }}</span
                                >
                            </div>
                        </div>
                    </n-gi>
                </template>
            </n-grid>
        </n-image-group>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import markdownIt from 'markdown-it'
import remove_markdown from 'remove-markdown'
import type Token from 'markdown-it/lib/token.mjs'
const imgRef = ref<HTMLImageElement[] | null>(null);
const props = defineProps({
    markdownContent: {
        type: String,
        required: true,
    },
})

const md = markdownIt()

// 递归遍历 tokens
function findImages(tokens: Token[]): string[] {
    const images: string[] = []

    for (const token of tokens) {
        if (token.type === 'image') {
            // 找到图片 token，提取 src
            const src = token.attrGet('src')
            if (src) {
                images.push(src)
            }
        }

        // 如果 token 有子 tokens，递归遍历
        if (token.children) {
            images.push(...findImages(token.children))
        }
    }

    return images
}

// 提取图片 URL
const images = computed(() => {
    const tokens = md.parse(props.markdownContent, {})
    const urls = findImages(tokens)
    return urls
})

// 动态计算列数
const gridCols = computed(() => {
    const count = images.value.length
    if (count == 1) return 1
    if (count == 4) return 2
    return 3
})

// 只显示前 9 张图片
const displayedImages = computed(() => images.value.slice(0, 9))
</script>

<style scoped>
.image-container {
    width: 100%;
    aspect-ratio: 1 / 1;
    overflow: hidden;
    border-radius: 8px;
    position: relative;
    display: inline-block;
}

.image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5); /* 半透明黑色背景 */
    display: flex;
    align-items: center;
    justify-content: center;
}

.plus {
    color: white;
    font-size: 24px;
    font-weight: bold;
}
</style>
