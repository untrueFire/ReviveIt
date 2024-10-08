<template>
    <div class="add-item-form">
        <h1>添加物品</h1>
        <form @submit.prevent="HandleAddItem">
            <div class="form-group">
                <label for="name">物品名称</label>
                <input id="name" v-model="name" placeholder="物品名称" required />
            </div>
            <div class="form-group">
                <label for="description">物品描述</label>
                <input id="description" v-model="description" placeholder="物品描述" required />
            </div>
            <div class="form-group">
                <label for="contactInfo">联系方式</label>
                <input id="contactInfo" v-model="contactInfo" placeholder="联系方式" required />
            </div>
            <button type="submit">添加</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useToast } from "vue-toastification";
import { useRouter } from "vue-router";
import { addItem } from "@/utils/api";
const name = ref("");
const description = ref("");
const contactInfo = ref("");
const toast = useToast();
const router = useRouter();

const HandleAddItem = async () => {
    try {
        const data = {
            name: name.value,
            description: description.value,
            contact_info: contactInfo.value,
        };
        await addItem(data);
        toast.success("物品添加成功");
        router.push("/user");
    } catch (error) {
        toast.error("物品添加失败");
    }
};
</script>

<style scoped src="@/assets/css/styles.css"></style>