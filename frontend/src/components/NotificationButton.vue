<template>
    <button @click="goToNotifications">
        通知
        <span v-if="store.unreadCount > 0" class="badge">{{ store.unreadCount }}</span>
    </button>
</template>

<script setup>
import { onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from '@/store';
import { updateNotifications } from '@/utils/api';
const router = useRouter();
const store = useStore();

const goToNotifications = async () => {
    await updateNotifications();
    router.push("/notifications");
};

onMounted(async () => {
    store.intervalId = setInterval(updateNotifications, 10000);
    await updateNotifications();
});

onUnmounted(() => {
    clearInterval(store.intervalId);
});
</script>

<style scoped src="@/assets/css/styles.css"></style>