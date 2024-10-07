<template>
  <div class="logout-page">
    <h1>注销</h1>
    <p>你确定要注销吗？</p>
    <button @click="handleLogout">注销</button>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import axios from "axios";
import { getCookie } from "@/utils/api";

const router = useRouter();

async function handleLogout() {
  try {
    const csrftoken = getCookie("csrftoken");
    await axios.post("/accounts/logout/", "", {
      withCredentials: true,
      headers: {
        "X-CsrfToken": csrftoken,
      },
    });
    localStorage.removeItem("userId");
    window.dispatchEvent(new Event("storage"));
    router.push("/login");
  } catch (error) {
    console.log("Error during logout:", error);
  }
}
</script>

<style scoped src="@/assets/css/styles.css"></style>