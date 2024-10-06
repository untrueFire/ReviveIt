<template>
  <nav class="top-menu">
    <ul>
      <li><router-link to="/">首页</router-link></li>
      <li v-if="!isLoggedIn"><router-link to="/login">登录</router-link></li>
      <li v-if="!isLoggedIn"><router-link to="/register">注册</router-link></li>
      <li v-if="isLoggedIn"><router-link to="/user">我的</router-link></li>
      <li v-if="isLoggedIn"><router-link to="/logout">注销</router-link></li>
      <li v-if="isLoggedIn"><router-link to="/additem">添加物品</router-link></li>
    </ul>
  </nav>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { ref, onMounted, onUnmounted } from 'vue';

const isLoggedIn = ref(localStorage.getItem('isLoggedIn') === 'true');

const handleStorageChange = () => {
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true';
};

onMounted(() => {
  window.addEventListener('storage', handleStorageChange);
});

onUnmounted(() => {
  window.removeEventListener('storage', handleStorageChange);
});
</script>

<style scoped>
.top-menu {
  background-color: #333;
  padding: 10px 0;
}

.top-menu ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: flex-end;
}

.top-menu li {
  margin-left: 20px;
}

.top-menu a {
  color: white;
  text-decoration: none;
  font-size: 16px;
}

.top-menu a:hover {
  text-decoration: underline;
}
</style>