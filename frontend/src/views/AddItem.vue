<template>
  <div class="add-item-form">
    <h1>添加物品</h1>
    <form @submit.prevent="addItem">
      <div class="form-group">
        <label for="name">物品名称</label>
        <input id="name" v-model="name" placeholder="物品名称" />
      </div>
      <div class="form-group">
        <label for="description">物品描述</label>
        <input id="description" v-model="description" placeholder="物品描述" />
      </div>
      <div class="form-group">
        <label for="contactInfo">联系方式</label>
        <input id="contactInfo" v-model="contactInfo" placeholder="联系方式" />
      </div>
      <button type="submit">添加</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useToast } from "vue-toastification";
import { useRouter } from "vue-router";
import { getCookie } from "@/utils/api";
const name = ref("");
const description = ref("");
const contactInfo = ref("");
const toast = useToast();
const router = useRouter();

const addItem = async () => {
  try {
    const csrfToken = getCookie("csrftoken");
    await axios.post(
      "/api/items/add/",
      {
        name: name.value,
        description: description.value,
        contact_info: contactInfo.value,
      },
      {
        withCredentials: true,
        headers: {
          "X-CSRFToken": csrfToken,
        },
      }
    );
    toast.success("物品添加成功");
    router.push("/user");
  } catch (error) {
    toast.error("物品添加失败");
  }
};
</script>

<style scoped src="@/assets/css/styles.css"></style>