<template>
	<div>
		<h1>物品详情</h1>
		<n-flex vertical>
			<n-layout>
				<n-layout-header>{{ item.name }}</n-layout-header>
				<n-layout-content content-style="padding: 24px;">
					{{ item.description }}
				</n-layout-content>
				<n-layout-footer>{{ item.contact_info }}</n-layout-footer>
			</n-layout>
		</n-flex>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { fetchItem } from "@/utils/api";
import { useMessage } from "naive-ui";

const route = useRoute();
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
</script>
