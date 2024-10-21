<template>
	<div>
		<h1>物品详情</h1>
		<!-- <n-flex vertical>
			<n-layout>
				<n-layout-header>{{ item.name }}</n-layout-header>
				<n-layout-content embedded content-style="padding: 24px;">
					{{ item.description }}
				</n-layout-content>
				<n-layout-footer>{{ item.contact_info }}</n-layout-footer>
			</n-layout>
		</n-flex> -->
		<div class="container">
			<n-card
				embedded
				:title="item.name"
				:segmented="{
				content: true,
				footer: 'soft',
			}">
				{{ item.description }}
				<template #footer>
					联系方式：{{ item.contact_info }}
				</template>
			</n-card>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { fetchItem } from "@/utils/api";
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
			router.push({ name: 'NotFound' });
		});
});
</script>

<style scoped>
.n-card {
	max-width: 80%;
	margin: auto;
}
</style>