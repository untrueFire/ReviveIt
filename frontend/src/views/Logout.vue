<template>
  <div class="logout-page">
    <h1>注销</h1>
    <p>你确定要注销吗？</p>
    <button @click="handleLogout">注销</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

async function handleLogout() {
  try {
    await axios.post('http://localhost:8000/accounts/logout/', '',{
      withCredentials: true
    });
    localStorage.removeItem('isLoggedIn');
	window.dispatchEvent(new Event('storage'));
    router.push('/login');
  } catch (error) {
    console.log('Error during logout:', error);
  }
}
</script>

<style scoped src="@/assets/css/styles.css"></style>