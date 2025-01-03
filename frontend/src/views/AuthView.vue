<template>
    <n-card>
        <n-tabs
            class="auth-form"
            default-value="login"
            animated
            size="large"
            justify-content="space-evenly"
        >
            <n-tab-pane name="login" tab="登录">
                <n-form
                    ref="formRef"
                    :model="model"
                    :rules="rules"
                    class="form-group"
                >
                    <n-form-item path="username" label="用户名">
                        <n-input
                            v-model:value="model.username"
                            placeholder="请输入用户名"
                            :input-props="{ autocomplete: 'username' }"
                        />
                    </n-form-item>
                    <n-form-item
                        path="password"
                        label="密码"
                        class="form-group"
                    >
                        <n-input
                            v-model:value="model.password"
                            type="password"
                            placeholder="请输入密码"
                            :input-props="{
                                autocomplete: 'current-password',
                            }"
                        />
                    </n-form-item>
                    <n-button
                        block
                        attr-type="submit"
                        round
                        color="#007bff"
                        @click="handleLogin"
                        >登录</n-button
                    >
                </n-form>
            </n-tab-pane>
            <n-tab-pane name="signup" tab="注册">
                <n-form
                    ref="formRef2"
                    :model="model2"
                    :rules="rules2"
                    class="form-group"
                >
                    <n-form-item path="username" label="用户名">
                        <n-input
                            v-model:value="model2.username"
                            placeholder="请输入用户名"
                            :input-props="{ autocomplete: 'username' }"
                        />
                    </n-form-item>
                    <n-form-item
                        path="password1"
                        label="密码"
                        class="form-group"
                    >
                        <n-input
                            v-model:value="model2.password1"
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
                            v-model:value="model2.password2"
                            type="password"
                            placeholder="请确认密码"
                            :input-props="{ autocomplete: 'new-password' }"
                        />
                    </n-form-item>
                    <n-button
                        block
                        attr-type="submit"
                        round
                        color="#007bff"
                        @click="handleRegister"
                    >
                        注册
                    </n-button>
                </n-form>
            </n-tab-pane>
        </n-tabs>
    </n-card>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage, type FormInst, type FormItemRule } from 'naive-ui'
import { post } from '@/utils/api'
import { useStore } from '@/stores'
import type { User } from '@/types/Api'
import { handleFormError } from '@/utils/constants'
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
                    } else if(typeof data === 'string' && data.includes('账号未激活')) {
                        message.error('该账号未激活，请等待管理员批准')
                    }
                     else {
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
        .catch(handleFormError)
}
const model2 = ref({
    username: '',
    password1: '',
    password2: '',
})
const formRef2 = ref<FormInst | null>(null)
const password2Ref = ref(null)
const rules2 = {
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
                value === model2.value.password1,
            message: '两次密码输入不一致',
            trigger: ['blur', 'password-input'],
        },
    ],
}
const handleRegister = (event: MouseEvent) => {
    event.preventDefault()
    formRef2.value
        ?.validate()
        .then(() => {
            try {
                post(
                    '/accounts/signup/',
                    new URLSearchParams({
                        username: model2.value.username,
                        password1: model2.value.password1,
                        password2: model2.value.password2,
                    }),
                ).then(data => {
                    if (data.id) {
                        store.user = data
                        message.success('注册成功')
                        router.push('/user')
                    }
                    else if (typeof data === 'string' && data.includes('账号未激活')) {
                        message.success('注册成功，请等待管理员批准')
                        router.push('/')
                    }
                     else {
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

<style scoped>
.auth-form {
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    margin: auto;
    max-width: 400px;
    padding: 20px;
}

.form-group {
    margin-bottom: 15px;
}
</style>
