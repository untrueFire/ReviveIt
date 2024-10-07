<template>
  <nav class="top-menu">
    <ul>
      <li><NotificationButton v-if="isLoggedIn"/></li>
      <li><router-link to="/">广场</router-link></li>
      <li v-if="!isLoggedIn"><router-link to="/login">登录</router-link></li>
      <li v-if="!isLoggedIn"><router-link to="/register">注册</router-link></li>
      <li v-if="isLoggedIn"><router-link to="/user">我的</router-link></li>
      <li v-if="isLoggedIn"><router-link to="/logout">登出</router-link></li>
      <li v-if="isLoggedIn"><router-link to="/additem">添加物品</router-link></li>
    </ul>
  </nav>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { ref, onMounted, onUnmounted } from 'vue';
import NotificationButton from './NotificationButton.vue';
import { getUserId } from "@/utils/user";
const userId = ref(getUserId());
const isLoggedIn = ref(userId.value !== null);


const handleStorageChange = () => {
  userId.value = getUserId();
  isLoggedIn.value = userId.value !== null;
};

onMounted(() => {
  window.addEventListener('storage', handleStorageChange);
});

onUnmounted(() => {
  window.removeEventListener('storage', handleStorageChange);
});
</script>

<style scoped src="@/assets/css/styles.css"></style>