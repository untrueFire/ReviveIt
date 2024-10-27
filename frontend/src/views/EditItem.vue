<template>
    <ItemForm
        title="编辑物品"
        v-model:model="model"
        @formSubmitted="HandleEditItem"
    />
</template>

<script setup lang="ts">
import { reactive, onMounted, type Reactive, type Ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchItem, updateItem } from '../utils/api'
import { useMessage, type FormInst } from 'naive-ui'
import { handleFormError } from '@/utils/constants'

const route = useRoute()
const router = useRouter()
const message = useMessage()

const itemId = Number(route.params.id)
const model = reactive<{
    name: string
    tags: string[]
    description: string
    contact_info: string
}>({
    name: '',
    tags: [],
    description: '',
    contact_info: '',
})

onMounted(async () => {
    fetchItem(itemId)
        .then(data => {
            Object.assign(model, data)
        })
        .catch(error => {
            console.error(error)
            message.error('获取物品信息失败:')
            router.push({ name: 'NotFound' })
        })
})

const HandleEditItem = (
    formRef: Ref<FormInst | null>,
    model: Reactive<{
        name: string
        tags: string[]
        description: string
        contact_info: string
    }>,
) => {
    formRef.value
        ?.validate()
        .then(() => {
            updateItem(itemId, {
                name: model.name,
                tags: model.tags,
                description: model.description,
                contact_info: model.contact_info,
            })
                .then(() => {
                    message.success('物品更新成功')
                    router.push('/user')
                })
                .catch(() => message.error('物品更新失败'))
        })
        .catch(handleFormError)
}
</script>
