<template>
    <n-virtual-list
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
                    action: 'soft'
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
                <ItemPreview :markdownContent="item.description" @click="handleViewItem(item.id)"/>
                <template #footer> 联系方式：{{ item.contactInfo }} </template>
                <template #action>
                    <slot :item="(item as Item)" @click.stop></slot>
                </template>
            </n-card>
            <br/><br/><br/>
        </template>
    </n-virtual-list>
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
