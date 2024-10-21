<template>
    <div>
        <n-badge :value="store.unreadCount" @click="goToNotifications" style="display: flex; align-items: center;">
            <n-avatar round>
                <n-icon>
                    <NotificationsItem />
                </n-icon>
            </n-avatar>
        </n-badge>
    </div>
</template>

<script setup>
import { onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from '@/store';
import { updateNotifications } from '@/utils/api';
import { MailOutline as NotificationsItem } from '@vicons/ionicons5';
const router = useRouter();
const store = useStore();

const goToNotifications = async () => {
    await updateNotifications();
    router.push("/notifications");
};

onMounted(async () => {
    store.intervalId = setInterval(updateNotifications, 30000);
    await updateNotifications();
});

onUnmounted(() => {
    clearInterval(store.intervalId);
});
</script>
