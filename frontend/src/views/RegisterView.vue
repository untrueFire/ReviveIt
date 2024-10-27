<template>
    <div class="register-form">
        <h1>注册</h1>
        <n-form ref="formRef" :model="model" :rules="rules" class="form-group">
            <n-form-item path="username" label="用户名">
                <n-input
                    v-model:value="model.username"
                    placeholder="请输入用户名"
                    :input-props="{ autocomplete: 'username' }"
                />
            </n-form-item>
            <n-form-item path="password1" label="密码" class="form-group">
                <n-input
                    v-model:value="model.password1"
                    type="password"
                    placeholder="请输入密码"
                    :input-props="{ autocomplete: 'new-password' }"
                />
            </n-form-item>
            <n-form-item
                path="password2"
                label="确认密码"
                ref="password2Ref"
                first
                class="form-group"
            >
                <n-input
                    v-model:value="model.password2"
                    type="password"
                    placeholder="请确认密码"
                    :input-props="{ autocomplete: 'new-password' }"
                />
            </n-form-item>
            <n-button attr-type="submit" round @click="handleRegister">
                注册
            </n-button>
        </n-form>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { post } from '../utils/api'
import { useStore } from '../stores'
import { useMessage, type FormInst, type FormItemRule } from 'naive-ui'
import { handleFormError } from '@/utils/constants'
const store = useStore()
const router = useRouter()
const message = useMessage()
const model = ref({
    username: '',
    password1: '',
    password2: '',
})
const formRef = ref<FormInst | null>(null)
const password2Ref = ref(null)
const rules = {
    username: [
        {
            required: true,
            message: '请输入用户名',
            trigger: ['blur'],
        },
    ],
    password1: [
        {
            required: true,
            message: '请输入密码',
            trigger: 'blur',
        },
        {
            min: 6,
            message: '密码长度不能少于6个字符',
            trigger: 'blur',
        },
    ],
    password2: [
        {
            required: true,
            message: '请确认密码',
            trigger: 'blur',
        },
        {
            validator: (_rule: FormItemRule, value: string) =>
                value === model.value.password1,
            message: '两次密码输入不一致',
            trigger: ['blur', 'password-input'],
        },
    ],
}
const handleRegister = (event: MouseEvent) => {
    event.preventDefault()
    formRef.value
        ?.validate()
        .then(() => {
            try {
                post(
                    '/accounts/signup/',
                    new URLSearchParams({
                        username: model.value.username,
                        password1: model.value.password1,
                        password2: model.value.password2,
                    }),
                ).then(data => {
                    if (data.id) {
                        store.user = data
                        message.success('注册成功')
                        router.push('/user')
                    } else {
                        const errorList = data.match(
                            /<ul class="errorlist(.*?)<\/ul>/s,
                        )
                        if (errorList) {
                            const errors = errorList[1]
                                .match(/<li>(.*?)<\/li>/g)
                                .map((error: string) =>
                                    error.replace(/<\/?li>/g, ''),
                                )
                            errors.forEach((error: string) =>
                                message.error(error),
                            )
                        }
                    }
                })
            } catch (error) {
                console.log('Error during registration:', error)
                message.error('注册失败')
            }
        })
        .catch(handleFormError)
}

onMounted(() => {
    if (store.isLoggedIn) {
        message.info('已登录')
        router.push('/user')
    }
})
</script>
