<template>
    <div class="edit-item-form">
        <h1>编辑物品</h1>
        <form @submit.prevent="handleUpdateItem">
            <div class="form-group">
                <label for="name">物品名称</label>
                <input id="name" v-model="item.name" placeholder="物品名称" required />
            </div>
            <div class="form-group">
                <label for="description">物品描述</label>
                <input id="description" v-model="item.description" placeholder="物品描述" required />
            </div>
            <div class="form-group">
                <label for="contact_info">联系方式</label>
                <input id="contact_info" v-model="item.contact_info" placeholder="联系方式" required />
            </div>
            <button type="submit">更新</button>
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { fetchItem, updateItem } from '@/utils/api';
import { useMessage } from 'naive-ui';

const route = useRoute();
const router = useRouter();
const message = useMessage();

const itemId = route.params.id;
const item = ref({
    name: '',
    description: '',
    contact_info: ''
});

onMounted(async () => {
    try {
        const response = await fetchItem(itemId);
        item.value = response;
    } catch (error) {
        console.log('获取物品信息失败:', error);
    }
});

async function handleUpdateItem() {
    try {
        await updateItem(itemId, item.value);
        message.success('物品更新成功');
        router.push('/user');
    } catch (error) {
        console.log('更新物品失败:', error);
        message.error('更新物品失败');
    }
}
</script>

<style scoped src="@/assets/css/styles.css"></style>