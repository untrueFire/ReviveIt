<template>
    <nav class="top-menu">
        <ul>
            <li>
                <NotificationButton v-if="store.isLoggedIn" />
            </li>
            <li><router-link to="/">广场</router-link></li>
            <li v-if="!store.isLoggedIn"><router-link to="/login">登录</router-link></li>
            <li v-if="!store.isLoggedIn"><router-link to="/register">注册</router-link></li>
            <li v-if="store.isLoggedIn"><router-link to="/user">我的</router-link></li>
            <li v-if="store.isLoggedIn"><router-link to="/logout">登出</router-link></li>
            <li v-if="store.isLoggedIn"><router-link to="/additem">添加物品</router-link></li>
        </ul>
    </nav>
</template>

<script setup>
import { RouterLink } from "vue-router";
import NotificationButton from './NotificationButton.vue';
import { useStore } from "@/store";
import { onMounted } from "vue";
import { updateUser } from "@/utils/api";
const store = useStore();
onMounted(() => updateUser());
</script>

<style scoped src="@/assets/css/styles.css"></style>