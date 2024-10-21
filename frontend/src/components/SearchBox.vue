<template>
    <div>
        <input type="text" v-model="query" @input="handleInput" placeholder="搜索..." class="searchBox" />
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
                    <td><n-ellipsis style="max-width: 100px">{{ item.name }}</n-ellipsis></td>
                    <td><n-ellipsis style="max-width: 240px">{{ item.description }}</n-ellipsis></td>
                    <td><n-ellipsis style="max-width: 100px">{{ item.contact_info }}</n-ellipsis></td>
                    <td>{{ item.owner.username }}</td>
                    <td v-if="store.isLoggedIn">
                        <n-space>
                            <button @click="router.push({ name: 'ViewItem', params: { id: item.id } })">详情</button>
                            <button v-if="item.owner.id != store.user.id" @click="handleReviveItem(item.id)">
                                复活
                            </button>
                        </n-space>
                    </td>
                </tr>
            </tbody>
        </table>
        <div v-if="showModal" class="modal-overlay">
            <div class="modal">
                <div class="modal-content">
                    <h2>你愿意消耗多少功德复活这件物品？</h2>
                    <n-input-number
                        v-model:value="price"
                        :input-props="{ type: 'number' }"
                        placeholder="请输入一个非负整数..."
                        :min="0"
                        :max="store.user.balance" />
                    <n-slider
                        v-model:value="price"
                        :step="1"
                        :max="store.user.balance" />
                    <p>当前可用功德：{{ store.user.balance }}</p>
                    <n-flex justify="center">
                        <button @click="SendReviveItem">确认</button>
                        <button @click="showModal = false">取消</button>
                    </n-flex>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { search, ReviveItem, updateUser } from "@/utils/api.js";
import { useStore } from "@/store";
import { useMessage } from "naive-ui";
import { useRouter } from "vue-router";
const router = useRouter();
const store = useStore();
const query = ref("");
const results = ref([]);
const message = useMessage();
const selectedItemId = ref();
const showModal = ref(false);
const price = ref(0);
const handleInput = async () => {
    try {
        results.value = await search(query.value);
    } catch (error) {
        message.error("数据获取失败");
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
            message.error("功德不足");
            return;
        }
        await ReviveItem(selectedItemId.value, { "price": price.value });
        message.success("请求发送成功");
        price.value = 0;
        showModal.value = false;
    } catch (error) {
        message.error("请求发送失败");
    }
};

onMounted(() => {
    handleInput();
});
</script>
