<template>
    <nav class="top-menu">
        <ul>
            <li>
                <NotificationButton v-if="store.isLoggedIn" />
            </li>
            <li><router-link to="/">广场</router-link></li>
            <template v-if="!store.isLoggedIn">
                <li><router-link to="/login">登录</router-link></li>
                <li><router-link to="/register">注册</router-link></li>
            </template>
            <template v-else>
                <li><router-link to="/user">我的</router-link></li>
                <li><router-link to="/logout">登出</router-link></li>
                <li><router-link to="/additem">添加物品</router-link></li>
                <li><router-link to="/woodenfish">木鱼</router-link></li>
            </template>
        </ul>
    </nav>
</template>

<script setup>
import { RouterLink } from "vue-router";
import NotificationButton from '@/components/NotificationButton.vue';
import { useStore } from "@/store";
import { onMounted } from "vue";
import { updateUser } from "@/utils/api";
const store = useStore();
onMounted(() => updateUser());
</script>

<style scoped src="@/assets/css/styles.css"></style>