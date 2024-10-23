<template>
    <div>
        <input type="text" v-model="query" @input="handleInput" placeholder="搜索名称或描述..." class="searchBox" />
        <n-data-table v-if="results.length" :columns="columns" :data="results" :pagination="pagination" striped />
        <div v-if="showModal" class="modal-overlay">
            <div class="modal">
                <div class="modal-content">
                    <h2>你愿意消耗多少功德复活这件物品？</h2>
                    <n-input-number v-model:value="price" :input-props="{ type: 'number' }" placeholder="请输入一个非负整数..."
                        :min="0" :max="store.user.balance" />
                    <n-slider v-model:value="price" :step="1" :max="store.user.balance" />
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
import { h, ref, onMounted, computed, reactive } from "vue";
import { search, ReviveItem, updateUser } from "../utils/api.js";
import { useStore } from "../store";
import { useMessage, NButton, NSpace } from "naive-ui";
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
    } catch {
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
        price.value = Number(price.value);
        if (!(Number.isFinite(price.value) && price.value <= store.user.balance && price.value >= 0)) {
            message.error("功德不足");
            return;
        }
        await ReviveItem(selectedItemId.value, { "price": price.value });
        message.success("请求发送成功");
        price.value = 0;
        showModal.value = false;
    } catch {
        message.error("请求发送失败");
    }
};

function handleViewItem(itemId) {
    router.push({ name: 'ViewItem', params: { id: itemId } });
}

const columns = computed(() => {
    let res = [
        {
            title: "ID",
            key: "id",
            sorter: 'default',
            resizable: true,
        },
        {
            title: "物品名称",
            key: "name",
            ellipsis: true,
            resizable: true,
            sorter: 'default'
        },
        {
            title: "物品描述",
            key: "description",
            ellipsis: true,
            resizable: true,
            sorter: 'default'
        },
        {
            title: "联系方式",
            key: "contact_info",
            ellipsis: true,
            resizable: true,
            sorter: 'default'
        },
        {
            title: "持有者",
            key: "owner.username",
            resizable: true,
        }
    ];
    if (store.isLoggedIn) {
        res.push({
            title: "操作",
            key: "actions",
            render(row) {
                let buttons = [
                    h(
                        NButton,
                        {
                            strong: true,
                            tertiary: true,
                            size: "small",
                            onClick: () => handleViewItem(row.id)
                        },
                        { default: () => '详情' }
                    )];
                if (row.owner.id != store.user.id) {
                    buttons.push(h(
                        NButton,
                        {
                            strong: true,
                            tertiary: true,
                            size: "small",
                            onClick: () => handleReviveItem(row.id),
                        },
                        { default: () => '复活' }
                    ))
                }
                return h(
                    NSpace,
                    null,
                    () => buttons
                );
            }
        });
    }
    return res;
}
);

const paginationReactive = reactive({
      page: 1,
      pageSize: 20,
      showSizePicker: true,
      pageSizes: [10, 20, 50, 100],
      onChange: (page) => {
        paginationReactive.page = page;
      },
      onUpdatePageSize: (pageSize) => {
        paginationReactive.pageSize = pageSize;
        paginationReactive.page = 1;
      }
});
const pagination = paginationReactive;

onMounted(() => {
    handleInput();
});
</script>
