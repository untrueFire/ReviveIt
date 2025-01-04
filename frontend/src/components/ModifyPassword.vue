<template>
    <n-flex vertical>
        <n-h4>修改密码</n-h4>
        <n-form
            ref="formRef"
            label-placement="left"
            label-width="auto"
            :model="formData"
            :rules="rules"
            @submit.prevent="handleSubmit"
        >
            <n-form-item label="当前密码" path="oldPassword">
                <n-input
                    v-model:value="formData.oldPassword"
                    type="password"
                    placeholder="请输入当前密码"
                />
            </n-form-item>
            <n-form-item label="新密码" path="newPassword1">
                <n-input
                    v-model:value="formData.newPassword1"
                    type="password"
                    placeholder="请输入新密码"
                />
            </n-form-item>
            <n-form-item label="确认新密码" path="newPassword2">
                <n-input
                    v-model:value="formData.newPassword2"
                    type="password"
                    placeholder="请再次输入新密码"
                />
            </n-form-item>
            <n-form-item>
                <n-button type="primary" attr-type="submit">更新密码</n-button>
            </n-form-item>
        </n-form>
    </n-flex>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useMessage } from 'naive-ui'
import type { FormInst, FormRules } from 'naive-ui'
import { post } from '@/utils/api'
import { handleFormError } from '@/utils/constants'

const formRef = ref<FormInst | null>(null)
const message = useMessage()

const formData = ref({
    oldPassword: '',
    newPassword1: '',
    newPassword2: '',
})

const rules: FormRules = {
    oldPassword: {
        required: true,
        message: '请输入当前密码',
        trigger: 'blur',
    },
    newPassword1: {
        required: true,
        message: '请输入新密码',
        trigger: 'blur',
    },
    newPassword2: {
        required: true,
        validator: (_rule, value) => {
            if (value !== formData.value.newPassword1) {
                return new Error('两次输入的密码不一致')
            }
            return true
        },
        trigger: 'blur',
    },
}

const handleSubmit = () => {
    formRef.value
        ?.validate()
        .then(() => {
            post('/accounts/password/change/', new URLSearchParams({
                oldpassword: formData.value.oldPassword,
                password1: formData.value.newPassword1,
                password2: formData.value.newPassword2,
            }))
                .then(() => {
                    message.success('密码修改成功')
                    formData.value.oldPassword = ''
                    formData.value.newPassword1 = ''
                    formData.value.newPassword2 = ''
                })
                .catch((error) => {
                    message.error(`密码修改失败：${error}`)
                })
        })
        .catch(handleFormError)
}
</script>
