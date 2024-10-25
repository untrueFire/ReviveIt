<template>
    <div class="login-form">
        <h1>登录</h1>
        <n-form ref="formRef" :model="model" :rules="rules" class="form-group">
            <n-form-item path="username" label="用户名">
                <n-input
                    v-model:value="model.username"
                    placeholder="请输入用户名"
                    :input-props="{ autocomplete: 'username' }"
                />
            </n-form-item>
            <n-form-item path="password" label="密码" class="form-group">
                <n-input
                    v-model:value="model.password"
                    type="password"
                    placeholder="请输入密码"
                    :input-props="{ autocomplete: 'current-password' }"
                />
            </n-form-item>
            <n-button attr-type="submit" round @click="handleLogin"
                >登录</n-button
            >
        </n-form>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage, type FormInst, type FormValidationError } from 'naive-ui'
import { type ValidateError } from 'async-validator'
import { post } from '../utils/api'
import { useStore } from '../stores'
import type { User } from '@/types/Api'
const router = useRouter()
const store = useStore()
const message = useMessage()
const formRef = ref<FormInst | null>(null)
const model = ref({
    username: '',
    password: '',
})
const rules = {
    username: [
        {
            required: true,
            message: '请输入用户名',
            trigger: 'blur',
        },
    ],
    password: [
        {
            required: true,
            message: '请输入密码',
            trigger: 'blur',
        },
    ],
}
const handleLogin = (event: MouseEvent) => {
    event.preventDefault()
    formRef.value
        ?.validate()
        .then(() => {
            post(
                '/accounts/login/',
                new URLSearchParams({
                    login: model.value.username,
                    password: model.value.password,
                }),
            )
                .then((data: User | string) => {
                    if ((data as User).id) {
                        store.user = data as User
                        message.success('登录成功')
                        router.push('/user')
                    } else {
                        const errorList = (data as string).match(
                            /<ul class="errorlist(.*?)<\/ul>/s,
                        )
                        if (errorList !== null) {
                            const part = errorList[1].match(/<li>(.*?)<\/li>/g)
                            const errors = (part as RegExpMatchArray).map(
                                (error: string) =>
                                    error.replace(/<\/?li>/g, ''),
                            )
                            errors.forEach((error: string) =>
                                message.error(error),
                            )
                        }
                    }
                })
                .catch(error => {
                    console.warn('Error logging in:', error)
                    message.error('登录失败')
                })
        })
        .catch((error: FormValidationError[]) => {
            error.forEach(field => {
                field.forEach((err: ValidateError) =>
                    message.error(`${err.message}`),
                )
            })
        })
}
onMounted(() => {
    if (store.isLoggedIn) {
        message.info('已登录')
        router.push('/user')
    }
})
</script>
