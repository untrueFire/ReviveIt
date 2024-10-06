<template>
  <div class="register-form">
    <h1>注册</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username">用户名</label>
        <input
          type="text"
          id="username"
          v-model="username"
          placeholder="请输入用户名"
          autocomplete="username"
        />
      </div>
      <div class="form-group">
        <label for="password1">密码</label>
        <input
          type="password"
          id="password1"
          v-model="password1"
          placeholder="请输入密码"
          autocomplete="new-password"
        />
      </div>
      <div class="form-group">
        <label for="password2">确认密码</label>
        <input
          type="password"
          id="password2"
          v-model="password2"
          placeholder="请确认密码"
          autocomplete="new-password"
        />
      </div>
      <button type="submit">注册</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from 'vue-router';
import axios from "axios";
import { useToast } from 'vue-toastification';
const username = ref("");
const password1 = ref("");
const password2 = ref("");
const csrfmiddlewaretoken = ref("");
const router = useRouter();
const toast = useToast();
onMounted(async () => {
  try {
    const response = await axios.get("http://localhost:8000/accounts/signup/");
    const csrfTokenElement = extractCsrfToken(response.data);
    csrfmiddlewaretoken.value = csrfTokenElement.value;
  } catch (error) {
    console.log("Error fetching CSRF token:", error);
  }
});

const handleSubmit = async () => {
  if (password1.value !== password2.value) {
    alert("密码和确认密码不一致");
    return;
  }
  try {
    const params = new URLSearchParams();
    params.append("csrfmiddlewaretoken", csrfmiddlewaretoken.value);
    params.append("username", username.value);
    params.append("email", "");
    params.append("password1", password1.value);
    params.append("password2", password2.value);
    const response = await axios.post(
      "http://localhost:8000/accounts/signup/",
      params,
      { withCredentials: true }
    );
    // console.log(response.data);
    if (response.data.username) {
      toast.success('注册成功');
      router.push("/login");
    } else {
      const errorList = response.data.match(/<ul class="errorlist(.*?)<\/ul>/s);
        if (errorList) {
          const errors = errorList[1].match(/<li>(.*?)<\/li>/g).map(error => error.replace(/<\/?li>/g, ''));
          errors.forEach(error => useToast().error(error));
        }
    }

  } catch (error) {
    console.log("Error during registration:", error);
    toast.error("注册失败");
  }
};

function extractCsrfToken(html) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, "text/html");
  const csrfTokenElement = doc.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  );
  return csrfTokenElement;
}
</script>

<style scoped src="@/assets/css/styles.css"></style>