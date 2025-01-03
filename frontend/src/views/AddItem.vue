<template>
    <ItemForm
        title="添加物品"
        :model="model"
        @formSubmitted="HandleAddItem"
    />
</template>

<script setup lang="ts">
import { reactive, type Reactive, type Ref } from 'vue'
import { useRouter } from 'vue-router'
import { addItem } from '@/utils/api'
import { useMessage, type FormInst } from 'naive-ui'
import { handleFormError } from '@/utils/constants'
import ItemForm from '@/components/ItemForm.vue'
const message = useMessage()
const router = useRouter()
const model = reactive<{
    name: string
    tags: string[]
    description: string
    contactInfo: string
}>({
    name: '',
    tags: [],
    description: '',
    contactInfo: '',
})
const HandleAddItem = (
    formRef: Ref<FormInst | null>,
    model: Reactive<{
        name: string
        tags: string[]
        description: string
        contactInfo: string
    }>,
) => {
    formRef.value
        ?.validate()
        .then(() => {
            addItem({
                name: model.name,
                tags: model.tags,
                description: model.description,
                contactInfo: model.contactInfo,
            })
                .then(() => {
                    message.success('物品添加成功')
                    router.push('/user')
                })
                .catch(() => message.error('物品添加失败'))
        })
        .catch(handleFormError)
}
</script>
