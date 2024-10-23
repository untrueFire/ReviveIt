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
        <n-data-table v-if="items.length" :columns="columns" :data="items" :pagination="pagination" :bordered="false" striped />
        <div v-else>
            <p>没有添加的物品</p>
        </div>
    </div>
</template>

<script setup>
import { h, ref, onMounted, reactive } from "vue";
import { useRouter } from "vue-router";
import { fetchUserItems, deleteItem } from "../utils/api";
import { useStore } from "../store";
import { useMessage, NButton, NSpace } from "naive-ui";
const message = useMessage();
const router = useRouter();
const items = ref([]);
const store = useStore();

function handleViewItem(itemId) {
    router.push({ name: 'ViewItem', params: { id: itemId } });
}

function handleEditItem(itemId) {
    router.push({ name: "EditItem", params: { id: itemId } });
}

async function handleDeleteItem(itemId) {
    try {
        await deleteItem(itemId);
        items.value = items.value.filter((item) => item.id !== itemId);
        message.success("物品删除成功");
    } catch (error) {
        message.error("删除物品失败");
    }
}

const columns = [
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
        sorter: 'default',
        resizable: true,
    },
    {
        title: "物品描述",
        key: "description",
        ellipsis: true,
        sorter: 'default',
        resizable: true,
    },
    {
        title: "联系方式",
        key: "contact_info",
        ellipsis: true,
        sorter: 'default',
        resizable: true,
    },
    {
        title: "操作",
        key: "actions",
        render(row) {
            return h(
                NSpace,
                null,
                () => [
                    h(
                        NButton,
                        {
                            strong: true,
                            tertiary: true,
                            size: "small",
                            onClick: () => handleViewItem(row.id)
                        },
                        { default: () => '详情' }
                    ),
                    h(
                        NButton,
                        {
                            strong: true,
                            tertiary: true,
                            size: "small",
                            onClick: () => handleEditItem(row.id)

                        },
                        { default: () => '编辑' }
                    ),
                    h(
                        NButton,
                        {
                            strong: true,
                            tertiary: true,
                            size: "small",
                            onClick: () => handleDeleteItem(row.id)

                        },
                        { default: () => '删除' }
                    )
                ]
            );
        }
    }
];

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

onMounted(async () => {
    fetchUserItems()
        .then((data) => {
            items.value = data;
        })
        .catch((error) => message.error("加载用户信息和物品失败:", error));
});

</script>
