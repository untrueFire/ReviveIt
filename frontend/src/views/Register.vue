<template>
    <div class="register-form">
        <h1>注册</h1>
        <form @submit.prevent="handleRegister">
            <div class="form-group">
                <label for="username">用户名</label>
                <input type="text" id="username" v-model="username" placeholder="请输入用户名" autocomplete="username"
                    required />
            </div>
            <div class="form-group">
                <label for="password1">密码</label>
                <input type="password" id="password1" v-model="password1" placeholder="请输入密码"
                    autocomplete="new-password" required />
            </div>
            <div class="form-group">
                <label for="password2">确认密码</label>
                <input type="password" id="password2" v-model="password2" placeholder="请确认密码"
                    autocomplete="new-password" required />
            </div>
            <button type="submit">注册</button>
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { useToast } from "vue-toastification";
import { getCsrftoken, updateUser } from "@/utils/api";
import { useStore } from "@/store";
const store = useStore();
const username = ref("");
const password1 = ref("");
const password2 = ref("");
const router = useRouter();
const toast = useToast();

const handleRegister = async () => {
    if (password1.value !== password2.value) {
        toast.error("密码和确认密码不一致");
        return;
    }
    try {
        const csrftoken = await getCsrftoken();
        const params = new URLSearchParams();
        params.append("username", username.value);
        params.append("email", "");
        params.append("password1", password1.value);
        params.append("password2", password2.value);
        const response = await axios.post("/accounts/signup/", params, {
            withCredentials: true,
            headers: {
                "X-CsrfToken": csrftoken,
            },
        });
        if (response.data.id) {
            store.user = response.data;
            toast.success("注册成功");
            router.push("/user");
        } else {
            const errorList = response.data.match(/<ul class="errorlist(.*?)<\/ul>/s);
            if (errorList) {
                const errors = errorList[1]
                    .match(/<li>(.*?)<\/li>/g)
                    .map((error) => error.replace(/<\/?li>/g, ""));
                errors.forEach((error) => useToast().error(error));
            }
        }
    } catch (error) {
        console.log("Error during registration:", error);
        toast.error("注册失败");
    }
};

onMounted(() => {
    if (store.isLoggedIn) {
        toast.info("已登录");
        router.push("/user");
    }
});
</script>

<style scoped src="@/assets/css/styles.css"></style>