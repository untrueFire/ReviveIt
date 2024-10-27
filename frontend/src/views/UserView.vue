<template>
    <div class="user-profile">
        <h1>用户信息</h1>
        <div v-if="store.user">
            <p><strong>用户名:</strong> {{ store.user.username }}</p>
            <p><strong>功德:</strong> {{ store.user.balance }}</p>
        </div>
        <div v-else>
            <p>加载中...</p>
        </div>

        <h2>添加的物品</h2>
        <n-data-table
            v-if="items.length"
            :columns="columns"
            :data="items"
            :pagination="pagination"
            :bordered="false"
            striped
        />
        <div v-else>
            <p>没有添加的物品</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { h, ref, onMounted } from 'vue'
import { pagination, randomTagType } from '../utils/constants'
import { useRouter } from 'vue-router'
import { fetchUserItems, deleteItem } from '../utils/api'
import { useStore } from '../stores'
import { useMessage, NButton, NFlex, NTag } from 'naive-ui'
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

const columns = [
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
        render: (row: Item) =>
            h(NFlex, () =>
                row.tags.map((tag: string) =>
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
    },
    {
        title: '物品描述',
        key: 'description',
        ellipsis: true,
        sorter: 'default',
        resizable: true,
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
]

onMounted(async () => {
    fetchUserItems()
        .then(data => {
            items.value = data
        })
        .catch(error => message.error('加载用户信息和物品失败:', error))
})
</script>
