<template>
    <div class="logout-page">
        <h1>登出</h1>
        <p>你确定要登出吗？</p>
        <button @click="handleLogout">登出</button>
    </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { logout } from "@/utils/api";
import { useStore } from "@/store";
import { useToast } from "vue-toastification";
const store = useStore();
const router = useRouter();
const toast = useToast();
async function handleLogout() {
    try {
        await logout();
        store.user = undefined;
        router.push("/login");
    } catch {
        toast.error("登出失败");
    }
}
</script>

<style scoped src="@/assets/css/styles.css"></style>