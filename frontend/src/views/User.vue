<template>
    <div class="user-profile">
        <h1>用户信息</h1>
        <div v-if="store.user">
            <p><strong>用户名:</strong> {{ store.user.username }}</p>
            <p><strong>功德:</strong> {{ store.user.balance }}</p>
        </div>
        <div v-else>
            <p>加载中...</p>
        </div>

        <h2>添加的物品</h2>
        <table v-if="items.length" class="items-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>物品名称</th>
                    <th>物品描述</th>
                    <th>联系方式</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in items" :key="item.id">
                    <td>{{ item.id }}</td>
                    <td>{{ item.name }}</td>
                    <td>{{ item.description }}</td>
                    <td>{{ item.contact_info }}</td>
                    <td>
                        <button @click="handleEditItem(item.id)">编辑</button>
                        <button @click="handleDeleteItem(item.id)">删除</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <div v-else>
            <p>没有添加的物品</p>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { fetchUserItems, deleteItem, updateUser } from "@/utils/api";
import { useStore } from "@/store";
import { useMessage } from "naive-ui";
const message = useMessage();
const router = useRouter();
const items = ref([]);
const store = useStore();
onMounted(async () => {
    try {
        await updateUser();
        items.value = await fetchUserItems();
    } catch (error) {
        message.error("加载用户信息和物品失败:", error);
    }
});

async function handleDeleteItem(itemId) {
    try {
        await deleteItem(itemId);
        items.value = items.value.filter((item) => item.id !== itemId);
        message.success("物品删除成功");
    } catch (error) {
        message.error("删除物品失败");
    }
}

function handleEditItem(itemId) {
    router.push({ name: "EditItem", params: { id: itemId } });
}
</script>

<style scoped src="@/assets/css/styles.css"></style>