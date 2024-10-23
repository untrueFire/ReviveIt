<template>
    <div class="login-form">
        <h1>登录</h1>
        <n-form ref="formRef" :model="model" :rules="rules" class="form-group">
            <n-form-item path="username" label="用户名">
                <n-input v-model:value="model.username" placeholder="请输入用户名"
                    :input-props="{ autocomplete: 'username' }" />
            </n-form-item>
            <n-form-item path="password" label="密码" class="form-group">
                <n-input v-model:value="model.password" type="password" placeholder="请输入密码"
                    :input-props="{ autocomplete: 'current-password' }" />
            </n-form-item>
            <n-button attr-type="submit" round @click="handleLogin">登录</n-button>
        </n-form>
    </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useMessage } from "naive-ui";
import { post } from "../utils/api";
import { useStore } from "../store";
const router = useRouter();
const store = useStore();
const message = useMessage();
const formRef = ref(null);
const model = ref({
    username: "",
    password: "",
});
const rules = {
    username: [
        {
            required: true,
            message: "请输入用户名",
            trigger: "blur",
        },
    ],
    password: [
        {
            required: true,
            message: "请输入密码",
            trigger: "blur",
        },
    ]
};
const handleLogin = (event) => {
    event.preventDefault();
    formRef.value
        ?.validate()
        .then(() => {
            post("/accounts/login/", new URLSearchParams({
                login: model.value.username,
                password: model.value.password
            })).then(data => {
                if (data.id) {
                    store.user = data;
                    message.success("登录成功");
                    router.push("/user");
                } else {
                    const errorList = data.match(/<ul class="errorlist(.*?)<\/ul>/s);
                    if (errorList) {
                        const errors = errorList[1]
                            .match(/<li>(.*?)<\/li>/g)
                            .map((error) => error.replace(/<\/?li>/g, ""));
                        errors.forEach((error) => message.error(error));
                    }
                }
            }).catch(error => {
                console.warn("Error logging in:", error);
                message.error("登录失败");
            })
        })
        .catch(error => {
            Object.keys(error).forEach((field) => {
                error[field].forEach((err) => message.error(`${err.message}`));
            });
        });
};
onMounted(() => {
    if (store.isLoggedIn) {
        message.info("已登录");
        router.push("/user");
    }
});
</script>
