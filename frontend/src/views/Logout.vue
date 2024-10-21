<template>
    <div class="logout-page">
        <h1>登出</h1>
        <p>你确定要登出吗？</p>
        <n-button @click="handleLogout" type="primary">登出</n-button>
    </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { logout } from "@/utils/api";
import { useStore } from "@/store";
import { useMessage } from "naive-ui";
const store = useStore();
const router = useRouter();
const message = useMessage();
async function handleLogout() {
    try {
        await logout();
        store.user = undefined;
        router.push({ name: 'Login' });
    } catch {
        message.error("登出失败");
    }
}
</script>

