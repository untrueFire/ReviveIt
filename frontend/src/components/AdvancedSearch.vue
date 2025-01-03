<template>
    <div>
        <h1>高级搜索</h1>
        <n-input
            type="text"
            v-model:value="query"
            @input="handleInput"
            placeholder="搜索名称或描述..."
            style="text-align: center"
        />
        <n-button
            type="info"
            ghost
            @click="$router.push('/')"
            style="float: right"
            >返回首页</n-button
        >
        <n-data-table
            v-if="items.length"
            :columns="columns"
            :data="items"
            :pagination="pagination"
            striped
        />
        <n-empty
            v-else
            size="huge"
            description="什么也没有找到"
            style="margin-top: 50px"
        ></n-empty>
        <n-modal
            v-model:show="showModal"
            class="modal-content"
            preset="dialog"
            title="你愿意消耗多少功德复活这件物品？"
            positiveText="确认"
            negativeText="取消"
            @positive-click="SendReviveItem"
            @negative-click="showModal = false"
            :icon="render"
        >
            <n-input-number
                v-model:value="price"
                :input-props="{ type: 'number' }"
                placeholder="请输入一个非负整数..."
                :min="0"
                :max="(store.user as User).balance"
            />
            <n-slider
                v-model:value="price"
                :step="1"
                :max="(store.user as User).balance"
            />
            当前可用功德：{{ (store.user as User).balance }}
        </n-modal>
    </div>
</template>

<script setup lang="ts">
import { h, ref, onMounted, computed } from 'vue'
import { pagination, randomTagType } from '../utils/constants'
import { search, ReviveItem, updateUser } from '../utils/api.js'
import { useStore } from '../stores/index.js'
import {
    useMessage,
    NButton,
    NFlex,
    NIcon,
    NIconWrapper,
    type DataTableColumn,
    NTag,
} from 'naive-ui'
import { useRouter } from 'vue-router'
import { QuestionMarkRound } from '@vicons/material'
import removeMarkdown from 'remove-markdown'
import type { Item, User } from '@/types/Api'
const router = useRouter()
const store = useStore()
const query = ref('')
const items = ref<Item[]>([])
const message = useMessage()
const selectedItemId = ref(0)
const showModal = ref(false)
const price = ref(0)

const render = () =>
    h(NIconWrapper, { size: 20, 'border-radius': 10 }, () =>
        h(NIcon, { size: 18, component: QuestionMarkRound }),
    )

const handleInput = async () => {
    try {
        items.value = await search(query.value)
    } catch {
        message.error('数据获取失败')
    }
}

const handleReviveItem = async (itemId: number) => {
    await updateUser()
    selectedItemId.value = itemId
    showModal.value = true
}

const SendReviveItem = async () => {
    try {
        price.value = Number(price.value)
        if (
            !(
                Number.isFinite(price.value) &&
                price.value <= (store.user as User).balance &&
                price.value >= 0
            )
        ) {
            message.error('功德不足')
            return
        }
        await ReviveItem(selectedItemId.value, { price: price.value })
        message.success('请求发送成功')
        price.value = 0
        showModal.value = false
    } catch {
        message.error('请求发送失败')
    }
}

function handleViewItem(itemId: number) {
    router.push({ name: 'ViewItem', params: { id: itemId } })
}

const columns = computed(() => {
    const res: DataTableColumn<Item>[] = [
        {
            title: 'ID',
            key: 'id',
            sorter: 'default',
            ellipsis: true,
            resizable: true,
        },
        {
            title: '物品名称',
            key: 'name',
            ellipsis: true,
            resizable: true,
            sorter: 'default',
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
            filterOptions: [
                ...new Set(items.value.flatMap(item => item.tags)),
            ].map(tag => ({ label: tag, value: tag })),
            filter: (value, row) => {
                return Boolean(row.tags.includes(value as string))
            },
        },
        {
            title: '物品描述',
            key: 'description',
            ellipsis: true,
            resizable: true,
            sorter: 'default',
            render: row => h('div', removeMarkdown(row.description)),
        },
        {
            title: '联系方式',
            key: 'contactInfo',
            ellipsis: true,
            resizable: true,
            sorter: 'default',
        },
        {
            title: '持有者',
            key: 'owner.username',
            ellipsis: true,
            resizable: true,
        },
    ]
    if (store.user) {
        res.push({
            title: '操作',
            key: 'actions',
            ellipsis: true,
            resizable: true,
            render(row) {
                const buttons = [
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
                ]
                if (store.user && row.owner.id != store.user.id) {
                    buttons.push(
                        h(
                            NButton,
                            {
                                strong: true,
                                tertiary: true,
                                size: 'small',
                                onClick: () => handleReviveItem(row.id),
                            },
                            { default: () => '复活' },
                        ),
                    )
                }
                return h(NFlex, null, () => buttons)
            },
        })
    }
    return res
})

onMounted(() => {
    handleInput()
})
</script>

<style scoped>
.modal-content {
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
