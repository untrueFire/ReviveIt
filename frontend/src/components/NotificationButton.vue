<template>
  <button @click="goToNotifications">
    通知
    <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
  </button>
</template>

  <script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { fetchNotifications } from "@/utils/api";
const notifications = ref([]);
const router = useRouter();
let intervalId = null;

const unreadNotifications = computed(() => {
  return notifications.value.filter((notification) => notification.unread);
});

const unreadCount = computed(() => {
  return unreadNotifications.value.length;
});

const fetchData = async () => {
  try {
    notifications.value = await fetchNotifications();
  } catch (error) {
    console.error("获取通知失败：", error);
  }
};

const goToNotifications = () => {
	router.push("/notifications");
};

onMounted(() => {
  intervalId = setInterval(fetchData, 10000);
  fetchData();
});

onUnmounted(() => {
  clearInterval(intervalId);
});
</script>

<style scoped src="@/assets/css/styles.css"></style>