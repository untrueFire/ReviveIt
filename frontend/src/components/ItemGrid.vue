<template>
    <n-virtual-list
        v-if="items.length > 0"
        style="max-width: 600px; margin: 0 auto"
        :item-size="42"
        :items="items"
        item-resizable
    >
        <template #default="{ item }">
            <n-card
                :title="item.name"
                embedded
                :segmented="{
                    content: 'soft',
                    footer: 'soft',
                    action: 'soft',
                }"
            >
                <template #header-extra>
                    <n-flex>
                        <n-tag
                            v-for="tag in item.tags"
                            :key="tag"
                            round
                            :bordered="false"
                            :type="randomTagType()"
                        >
                            {{ tag }}
                        </n-tag>
                    </n-flex>
                </template>
                <ItemPreview
                    :markdownContent="item.description"
                    @click="handleViewItem(item.id)"
                />
                <template #footer>
                    <n-flex justify="space-between">
                        <n-flex>
                            <n-avatar
                                :src="
                                    '/api/file/get/' +
                                    item.owner.avatar.filename"
                                fallback-src="/api/file/get/default_avatar.png"
                                round
                                :style="{ width: '24px', height: '24px' }"
                                :img-props="{ width: '24px', height: '24px' }"
                            />
                            <n-text>
                                {{ item.owner.username }}
                            </n-text>
                        </n-flex>
                        <n-text>
                            {{ item.contactInfo }}
                        </n-text>
                    </n-flex>
                </template>
                <template #action>
                    <slot :item="(item as Item)" @click.stop></slot>
                </template>
            </n-card>
        </template>
    </n-virtual-list>
    <n-empty
        v-else
        size="huge"
        description="什么也没有找到"
        style="margin-top: 50px"
    />
</template>

<script lang="ts" setup>
import { randomTagType } from '../utils/constants'
import type { Item } from '@/types/Api'
import ItemPreview from './ItemPreview.vue'
import { useRouter } from 'vue-router'
import type { Reactive } from 'vue'
defineProps<{
    items: Reactive<Item[]>
}>()
const router = useRouter()
function handleViewItem(itemId: number) {
    router.push({ name: 'ViewItem', params: { id: itemId } })
}
</script>
