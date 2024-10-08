<template>
    <div>
        <input type="text" v-model="query" @input="handleInput" placeholder="搜索..." />
        <table v-if="results.length">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>物品名称</th>
                    <th>物品描述</th>
                    <th>联系方式</th>
                    <th>持有者</th>
                    <th v-if="store.isLoggedIn">操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in results" :key="item.id">
                    <td>{{ item.id }}</td>
                    <td>{{ item.name }}</td>
                    <td>{{ item.description }}</td>
                    <td>{{ item.contact_info }}</td>
                    <td>{{ item.owner.username }}</td>
                    <td>
                        <button v-if="store.isLoggedIn && item.owner.id != store.user.id"
                            @click="handleReviveItem(item.id)">
                            复活
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
        <div v-if="showModal" class="modal-overlay">
            <div class="modal">
                <div class="modal-content">
                    <h2>你愿意消耗多少功德复活这件物品？</h2>
                    <input v-model.number="price" type="number" placeholder="请输入一个非负整数..." min="0"
                        v-bind:max="store.user.balance" />
                    <p>当前可用功德：{{ store.user.balance }}</p>
                    <button @click="SendReviveItem">确认</button>
                    <button @click="showModal = false">取消</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { search, ReviveItem, updateUser } from "@/utils/api.js";
import { useToast } from "vue-toastification"
import { useStore } from "@/store";
const store = useStore();
const query = ref("");
const results = ref([]);
const toast = useToast();
const selectedItemId = ref();
const showModal = ref(false);
const price = ref(0);
const handleInput = async () => {
    try {
        if (store.isLoggedIn) {
            updateUser();
        }
        results.value = await search(query.value);
    } catch (error) {
        toast.error("数据获取失败");
    }
};

const handleReviveItem = async (itemId) => {
    updateUser();
    selectedItemId.value = itemId;
    showModal.value = true;
};

const SendReviveItem = async () => {
    try {
        if (!(price.value <= store.user.balance)) {
            toast.error("功德不足");
            return;
        }
        await ReviveItem(selectedItemId.value, { "price": price.value });
        toast.success("请求发送成功");
        showModal.value = false;
    } catch (error) {
        toast.error("请求发送失败");
    }
};

onMounted(() => {
    updateUser();
    handleInput();
});
</script>

<style scoped src="@/assets/css/styles.css"></style>