<template>
    <n-data-table
        v-if="items.length"
        :columns="columns"
        :data="items"
        :pagination="pagination"
        :bordered="false"
        striped
    />
    <n-empty
        v-else
        size="huge"
        description="什么也没有，快来添加你的第一个物品吧！"
        style="margin-top: 50px"
    />
    <n-flex justify="center">
        <n-button @click="router.push({name: 'AddItem'})" style="align-items: center;">
            添加物品
        </n-button>
    </n-flex>
</template>

<script setup lang="ts">
import { h, ref, onMounted, computed, type ComputedRef } from 'vue'
import { pagination, randomTagType } from '@/utils/constants'
import { removeMd } from '@/utils/constants'
import { useRouter } from 'vue-router'
import { fetchUserItems, deleteItem } from '@/utils/api'
import { useStore } from '@/stores'
import {
    useMessage,
    NButton,
    NFlex,
    NTag,
    type DataTableColumn,
} from 'naive-ui'
import type { Item } from '@/types/Api'
const message = useMessage()
const router = useRouter()
const items = ref<Item[]>([])
const store = useStore()

function handleViewItem(itemId: number) {
    router.push({ name: 'ViewItem', params: { id: itemId } })
}

function handleEditItem(itemId: number) {
    router.push({ name: 'EditItem', params: { id: itemId } })
}

async function handleDeleteItem(itemId: number) {
    try {
        await deleteItem(itemId)
        items.value = items.value.filter(item => item.id !== itemId)
        message.success('物品删除成功')
    } catch {
        message.error('删除物品失败')
    }
}

const columns: ComputedRef<DataTableColumn<Item>[]> = computed(() => [
    {
        title: 'ID',
        key: 'id',
        sorter: 'default',
        resizable: true,
    },
    {
        title: '物品名称',
        key: 'name',
        ellipsis: true,
        sorter: 'default',
        resizable: true,
    },
    {
        title: '标签',
        key: 'tags',
        ellipsis: true,
        resizable: true,
        render: row =>
            h(NFlex, () =>
                row.tags.map(tag =>
                    h(
                        NTag,
                        {
                            round: true,
                            bordered: false,
                            type: randomTagType(),
                        },
                        () => tag,
                    ),
                ),
            ),
        filterOptions: [...new Set(items.value.flatMap(item => item.tags))].map(
            tag => ({ label: tag, value: tag }),
        ),
        filter: (value, row) => {
            return Boolean(row.tags.includes(value as string))
        },
    },
    {
        title: '物品描述',
        key: 'description',
        ellipsis: true,
        sorter: 'default',
        resizable: true,
        render: row => h('div', removeMd(row.description)),
    },
    {
        title: '联系方式',
        key: 'contactInfo',
        ellipsis: true,
        sorter: 'default',
        resizable: true,
    },
    {
        title: '操作',
        key: 'actions',
        resizable: true,
        render(row: Item) {
            return h(NFlex, null, () => [
                h(
                    NButton,
                    {
                        strong: true,
                        tertiary: true,
                        size: 'small',
                        onClick: () => handleViewItem(row.id as number),
                    },
                    { default: () => '详情' },
                ),
                h(
                    NButton,
                    {
                        strong: true,
                        tertiary: true,
                        size: 'small',
                        onClick: () => handleEditItem(row.id as number),
                    },
                    { default: () => '编辑' },
                ),
                h(
                    NButton,
                    {
                        strong: true,
                        tertiary: true,
                        size: 'small',
                        onClick: () => handleDeleteItem(row.id as number),
                    },
                    { default: () => '删除' },
                ),
            ])
        },
    },
])

onMounted(async () => {
    fetchUserItems()
        .then(data => {
            items.value = data
        })
        .catch(error => message.error('加载用户信息和物品失败:', error))
})
</script>

<style scoped>
.user-profile {
    max-width: 70%;
    margin: auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.user-profile h1,
.user-profile h2 {
    text-align: center;
    margin-bottom: 20px;
}
</style>
