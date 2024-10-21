<template>
    <div class="edit-item-form">
        <h1>编辑物品</h1>
        <n-form>
            <div class="form-group">
                <label for="name">物品名称</label>
                <n-input id="name" v-model:value="item.name" placeholder="物品名称" required />
            </div>
            <div class="form-group">
                <label for="description">物品描述</label>
                <n-input id="description" v-model:value="item.description" placeholder="物品描述" required />
            </div>
            <div class="form-group">
                <label for="contact_info">联系方式</label>
                <n-input id="contact_info" v-model:value="item.contact_info" placeholder="联系方式" required />
            </div>
            <button @click="handleUpdateItem">更新</button>
        </n-form>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { fetchItem, updateItem } from "@/utils/api";
import { useMessage } from "naive-ui";

const route = useRoute();
const router = useRouter();
const message = useMessage();

const itemId = route.params.id;
const item = ref({
    id: 0,
    name: "",
    description: "",
    contact_info: "",
    owner: {
        id: 0,
        username: "",
    },
});

onMounted(async () => {
    fetchItem(itemId)
        .then((data) => {
            item.value = data;
        })
        .catch((error) => {
            console.error(error);
            message.error("获取物品信息失败:");
        });
});

async function handleUpdateItem() {
    updateItem(itemId, item.value)
        .then(() => {
            message.success("物品更新成功");
            router.push({ name: "User" });
        })
        .catch((error) => {
            console.error(error);
            message.error("更新物品失败");
        });
}
</script>

