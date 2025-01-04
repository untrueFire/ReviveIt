<template>
    <n-flex vertical>
        <n-form
            ref="formRef"
            inline
            label-placement="left"
            label-width="auto"
            :model="formData"
            :rules="rules"
            :show-require-mark="false"
            @submit.prevent="handleSubmit"
        >
            <n-form-item label="修改用户名" path="username">
                <n-input
                    v-model:value="formData.username"
                    type="text"
                    :placeholder="store.user?.username"
                />
            </n-form-item>
            <n-form-item>
                <n-button type="primary" attr-type="submit">更新</n-button>
            </n-form-item>
        </n-form>
    </n-flex>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useStore } from '@/stores'
import { changeUsername, updateUser } from '@/utils/api'
import { useMessage } from 'naive-ui'
import type { FormInst, FormRules } from 'naive-ui'

const store = useStore()
const message = useMessage()
const formRef = ref<FormInst | null>(null)
const formData = ref({
    username: '',
})

const rules: FormRules = {
    username: {
        required: true,
        message: '用户名不能为空',
        trigger: 'blur',
    },
}

const handleSubmit = () => {
    formRef.value?.validate(errors => {
        if (!errors) {
            updateUsername(formData.value.username)
        } else {
            message.error('请输入用户名')
        }
    })
}

const updateUsername = (username: string) => {
    changeUsername(username)
        .then(() => {
            updateUser()
            message.success('更新成功')
            formData.value.username = ''
        })
        .catch(() => {
            message.error('更新失败')
        })
}
</script>