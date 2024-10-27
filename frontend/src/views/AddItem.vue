<template>
    <div class="add-item-form">
        <h1>添加物品</h1>
        <n-form ref="formRef" :model="model" :rules="rules" class="form-group">
            <n-form-item path="name" label="物品名称">
                <n-input
                    id="name"
                    v-model:value="model.name"
                    placeholder="物品名称"
                    required
                />
            </n-form-item>
            <n-form-item path="tags" label="标签">
                <n-dynamic-tags
                    v-model:value="model.tags"
                    :render-tag="render"
                />
            </n-form-item>
            <n-form-item path="description" label="物品描述">
                <n-input
                    type="textarea"
                    id="description"
                    v-model:value="model.description"
                    placeholder="物品描述"
                    required
                />
            </n-form-item>
            <n-form-item path="contactInfo" label="联系方式">
                <n-input
                    id="contactInfo"
                    v-model:value="model.contactInfo"
                    placeholder="联系方式"
                    required
                />
            </n-form-item>
            <n-button attr-type="submit" @click="HandleAddItem">添加</n-button>
        </n-form>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { addItem } from '../utils/api'
import { useMessage, type FormInst } from 'naive-ui'
import { handleFormError, renderTag } from '@/utils/constants'
const message = useMessage()
const router = useRouter()
const formRef = ref<FormInst | null>(null)
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
const render = renderTag(model)
const rules = {
    name: [
        {
            required: true,
            message: '请输入物品名称',
            trigger: 'blur',
        },
    ],
    description: [
        {
            required: true,
            message: '请输入物品描述',
            trigger: 'blur',
        },
    ],
    contactInfo: [
        {
            required: true,
            message: '请输入联系方式',
            trigger: 'blur',
        },
    ],
}
const HandleAddItem = async (event: MouseEvent) => {
    event.preventDefault()
    formRef.value
        ?.validate()
        .then(() => {
            addItem({
                name: model.name,
                tags: model.tags,
                description: model.description,
                contact_info: model.contactInfo,
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

<style scoped>
.add-item-form {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.add-item-form h1 {
    text-align: center;
    margin-bottom: 20px;
}

.add-item-form button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
</style>
