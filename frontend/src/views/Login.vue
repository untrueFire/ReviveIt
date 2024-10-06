<template>
  <div class="login-form">
    <h1>登录</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username">用户名</label>
        <input type="text" id="username" v-model="username" placeholder="请输入用户名" autocomplete="username" />
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input type="password" id="password" v-model="password" placeholder="请输入密码" autocomplete="current-password" />
      </div>
      <button type="submit">登录</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useToast } from 'vue-toastification';
const username = ref('');
const password = ref('');
const csrfmiddlewaretoken = ref('');
const router = useRouter();
const toast = useToast();
onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/accounts/login/');
    const csrfTokenElement = extractCsrfToken(response.data);
    csrfmiddlewaretoken.value = csrfTokenElement.value;
  } catch (error) {
    console.log('Error fetching CSRF token:', error);
  }
});

const handleSubmit = async () => {
  try {
    const params = new URLSearchParams();
    params.append('csrfmiddlewaretoken', csrfmiddlewaretoken.value)
    params.append('login', username.value);
    params.append('password', password.value);
    params.append('next', '/api/user/');
    const response = await axios.post('http://localhost:8000/accounts/login/', params,{withCredentials: true});
    // console.log(response.data);
    if (response.data.username) {
      localStorage.setItem('isLoggedIn', 'true');
      window.dispatchEvent(new Event('storage'));
      toast.success('登录成功');
      router.push('/user');
    } else {
      const errorList = response.data.match(/<ul class="errorlist(.*?)<\/ul>/s);
        if (errorList) {
          const errors = errorList[1].match(/<li>(.*?)<\/li>/g).map(error => error.replace(/<\/?li>/g, ''));
          errors.forEach(error => useToast().error(error));
        }

    }
  } catch (error) {
    console.log('Error logging in:', error);
    toast.error('登录失败');
  }
};

function extractCsrfToken(html) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');
  const csrfTokenElement = doc.querySelector('input[name="csrfmiddlewaretoken"]');
  return csrfTokenElement;
}
</script>

<style scoped src="@/assets/css/styles.css"></style>