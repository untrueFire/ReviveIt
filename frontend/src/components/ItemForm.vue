<template>
    <div class="item-form">
        <h1>{{ title }}</h1>
        <n-form ref="formRef" :model="model" :rules="rules">
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
                    :max="10"
                />
            </n-form-item>
            <n-form-item path="description" label="物品描述">
                <MdEditor
                    v-model="model.description"
                    :theme="editorTheme"
                    style="text-align: left"
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
            <n-button attr-type="submit" @click="handleSubmit">提交</n-button>
        </n-form>
    </div>
</template>

<script setup lang="ts">
import { renderTag } from '@/utils/constants'
import type { FormInst } from 'naive-ui'
import { computed, reactive, ref, watch, type Ref } from 'vue'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { useThemeStore } from '@/stores'
const store = useThemeStore()
const editorTheme = computed(() =>
    store.themeName === 'dark' ? 'dark' : 'light',
)
interface Props {
    title: string
    model: {
        name: string
        tags: string[]
        description: string
        contactInfo: string
    }
}
const props = defineProps<Props>()
const model = reactive({ ...props.model })
const formRef = ref<FormInst | null>(null)
const render = renderTag(model)
const emit = defineEmits<{
    (
        e: 'formSubmitted',
        formRef: Ref<FormInst | null>,
        model: Props['model'],
    ): void
    (e: 'update:model', value: Props['model']): void
}>()
watch(
    () => props.model,
    newValue => {
        Object.assign(model, newValue)
    },
    { deep: true },
)

function handleSubmit(e: MouseEvent) {
    e.preventDefault()
    emit('formSubmitted', formRef, model)
    emit('update:model', {
        name: '',
        tags: [],
        description: '',
        contactInfo: '',
    })
}
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
</script>

<style scoped>
.item-form {
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.item-form h1 {
    text-align: center;
    margin-bottom: 20px;
}

.item-form button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
</style>
