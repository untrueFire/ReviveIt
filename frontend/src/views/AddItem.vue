<template>
    <div class="add-item-form">
        <h1>添加物品</h1>
        <n-form>
            <div class="form-group">
                <label for="name">物品名称</label>
                <n-input
                    id="name"
                    v-model:value="name"
                    placeholder="物品名称"
                    required
                />
            </div>
            <div class="form-group">
                <label for="description">物品描述</label>
                <n-input
                    type="textarea"
                    id="description"
                    v-model:value="description"
                    placeholder="物品描述"
                    required
                />
            </div>
            <div class="form-group">
                <label for="contactInfo">联系方式</label>
                <n-input
                    id="contactInfo"
                    v-model:value="contactInfo"
                    placeholder="联系方式"
                    required
                />
            </div>
            <n-button attr-type="submit" @click="HandleAddItem">添加</n-button>
        </n-form>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { addItem } from '../utils/api'
import { useMessage } from 'naive-ui'
const name = ref('')
const description = ref('')
const contactInfo = ref('')
const message = useMessage()
const router = useRouter()

const HandleAddItem = async () => {
    try {
        const data = {
            name: name.value,
            description: description.value,
            contact_info: contactInfo.value,
        }
        await addItem(data)
        message.success('物品添加成功')
        router.push('/user')
    } catch {
        message.error('物品添加失败')
    }
}
</script>
