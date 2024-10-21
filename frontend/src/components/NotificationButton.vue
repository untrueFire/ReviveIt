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
import { updateUnread } from '@/utils/api';
import { MailOutline as NotificationsItem } from '@vicons/ionicons5';
const router = useRouter();
const store = useStore();

const goToNotifications = async () => {
    await updateUnread();
    router.push("/notifications");
};

onMounted(() => {
    store.intervalId = setInterval(updateUnread, 30000);
    updateUnread();
});

onUnmounted(() => {
    clearInterval(store.intervalId);
});
</script>
