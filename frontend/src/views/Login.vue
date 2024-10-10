<template>
    <div class="login-form">
        <h1>登录</h1>
        <form @submit.prevent="handleSubmit">
            <div class="form-group">
                <label for="username">用户名</label>
                <input type="text" id="username" v-model="username" placeholder="请输入用户名" autocomplete="username"
                    required />
            </div>
            <div class="form-group">
                <label for="password">密码</label>
                <input type="password" id="password" v-model="password" placeholder="请输入密码"
                    autocomplete="current-password" required />
            </div>
            <button type="submit">登录</button>
        </form>
    </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useMessage } from "naive-ui";
import axios from "axios";
import { getCsrftoken } from "@/utils/api";
import { useStore } from "@/store";
const username = ref("");
const password = ref("");
const router = useRouter();
const store = useStore();
const message = useMessage();
const handleSubmit = async () => {
    try {
        const csrftoken = await getCsrftoken();
        const params = new URLSearchParams();
        params.append("login", username.value);
        params.append("password", password.value);
        params.append("next", "/api/user/");
        const response = await axios.post("/accounts/login/", params, {
            withCredentials: true,
            headers: {
                "X-CsrfToken": csrftoken,
            },
        });
        if (response.data.id) {
            store.user = response.data;
            message.success("登录成功");
            router.push("/user");
        } else {
            const errorList = response.data.match(/<ul class="errorlist(.*?)<\/ul>/s);
            if (errorList) {
                const errors = errorList[1]
                    .match(/<li>(.*?)<\/li>/g)
                    .map((error) => error.replace(/<\/?li>/g, ""));
                errors.forEach((error) => message.error(error));
            }
        }
    } catch (error) {
        console.warn("Error logging in:", error);
        message.error("登录失败");
    }
};
onMounted(() => {
    if (store.isLoggedIn) {
        message.info("已登录");
        router.push("/user");
    }
});
</script>

<style scoped src="@/assets/css/styles.css"></style>
