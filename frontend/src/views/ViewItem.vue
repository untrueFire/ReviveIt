<template>
    <div>
        <h1>物品详情</h1>
        <div class="container">
            <n-card
                embedded
                :title="item.name"
                :segmented="{
                    content: 'soft',
                    footer: 'soft',
                }"
            >
                <template #header-extra>
                    <n-flex>
                        <template v-for="tag in item.tags" :key="tag">
                            <n-tag
                                round
                                :type="randomTagType()"
                                :bordered="false"
                            >
                                {{ tag }}
                            </n-tag>
                        </template>
                    </n-flex>
                </template>
                <MdPreview
                    editorId="preview-only"
                    v-model="item.description"
                    :theme="editorTheme"
                    @onError="onError"
                    style="text-align: left"
                />
                <template #footer> 联系方式：{{ item.contactInfo }} </template>
            </n-card>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchItem } from '../utils/api'
import { useMessage, NTag } from 'naive-ui'
import type { Item } from '@/types/Api'
import { randomTagType, onError } from '@/utils/constants'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { useThemeStore } from '@/stores'

const route = useRoute()
const router = useRouter()
const message = useMessage()
const store = useThemeStore()
const editorTheme = computed(() =>
    store.themeName === 'dark' ? 'dark' : 'light',
)

const itemId = route.params.id
const item = ref<Item>({
    id: 0,
    name: '',
    tags: [],
    description: '',
    contactInfo: '',
    owner: {
        id: 0,
        username: '',
    },
})

onMounted(async () => {
    fetchItem(Number(itemId))
        .then(data => {
            item.value = data
        })
        .catch(error => {
            console.error(error)
            message.error('获取物品信息失败:')
            router.push({ name: 'NotFound' })
        })
})
</script>

<style scoped>
.n-card {
    max-width: 70%;
    margin: auto;
}
</style>
