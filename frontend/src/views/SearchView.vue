<template>
    <div style="text-align: left">
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
            @click="$router.push('/search')"
            style="float: right"
            >高级搜索</n-button
        >
        <ItemGrid :items="reactive(items)" v-slot="{ item }">
            <n-button
                :strong="true"
                :tertiary="true"
                size="small"
                v-if="store.user && item.owner.id != store.user.id"
                :onclick="() => handleReviveItem(item.id)"
            >
                复活
            </n-button>
        </ItemGrid>
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
import { h, ref, onMounted, reactive } from 'vue'
import { search, ReviveItem, updateUser } from '@/utils/api.js'
import { useStore } from '@/stores/index.js'
import { useMessage, NButton, NIcon, NIconWrapper } from 'naive-ui'
import { QuestionMarkRound } from '@vicons/material'
import type { Item, User } from '@/types/Api'
import ItemGrid from '@/components/ItemGrid.vue'
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
