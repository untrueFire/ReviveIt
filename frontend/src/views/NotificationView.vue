<template>
    <div class="notifications-container">
        <template v-if="store.unreadNotifications.length > 0">
            <h2>未读通知</h2>
            <table>
                <tr v-for="notification in store.unreadNotifications" :key="notification.id">
                    <td>
                        <template v-if="notification.verb == 'proposed'">
                            {{ notification.actor.username }} 请求以
                            {{ notification.action_object.price }} 功德的代价复活
                            {{ notification.action_object.target.name }}
                        </template>
                        <template v-else-if="notification.verb == 'accepted'">
                            {{ notification.actor.username }} 同意了你以
                            {{ notification.action_object.price }} 功德的代价复活
                            {{ notification.action_object.target.name }} 的请求
                        </template>
                        <template v-else-if="notification.verb == 'rejected'">
                            {{ notification.actor.username }} 拒绝了你以
                            {{ notification.action_object.price }} 功德的代价复活
                            {{ notification.action_object.target.name }} 的请求
                        </template>
                        <template v-else-if="notification.verb == 'sold out'">
                            你向 {{ notification.actor.username }} 请求的 {{ notification.action_object.target.name }} 已被先行复活
                        </template>
                        <template v-if="notification.verb == 'proposed'">
                            <button @click="handleAcceptNotification(notification.id)">
                                同意
                            </button>
                            <button @click="handleRejectNotification(notification.id)">
                                拒绝
                            </button>
                        </template>
                        <template v-else-if="
                            notification.verb == 'accepted' ||
                            notification.verb == 'rejected' ||
                            notification.verb == 'sold out'
                        ">
                            <button @click="handleSetRead(notification.id)">已读</button>
                        </template>
                    </td>
                </tr>
            </table>
        </template>
        <template v-else>
            <p>暂无未读通知</p>
        </template>
        <template v-if="store.readNotifications.length > 0">
            <h2>已读通知</h2>
            <table>
                <tr v-for="notification in store.readNotifications" :key="notification.id">
                    <td>
                        <template v-if="notification.verb == 'proposed'">
                            {{ notification.actor.username }} 请求以
                            {{ notification.action_object.price }} 功德的代价复活
                            {{ notification.action_object.target.name }}
                            <template v-if="notification.data == 'accepted'">（已同意）</template>
                            <template v-else-if="notification.data == 'rejected'">（已拒绝）</template>
                            <template v-else-if="notification.data == 'sold out'">（已被先行复活）</template>
                        </template>
                        <template v-else-if="notification.verb == 'accepted'">
                            {{ notification.actor.username }} 同意了你以
                            {{ notification.action_object.price }} 功德的代价复活
                            {{ notification.action_object.target.name }} 的请求
                        </template>
                        <template v-else-if="notification.verb == 'rejected'">
                            {{ notification.actor.username }} 拒绝了你以
                            {{ notification.action_object.price }} 功德的代价复活
                            {{ notification.action_object.target.name }} 的请求
                        </template>
                        <template v-else-if="notification.verb == 'sold out'">
                            你向 {{ notification.actor.username }} 请求的 {{ notification.action_object.target.name }} 已被先行复活
                        </template>
                    </td>
                </tr>
            </table>
        </template>
        <template v-else>暂无已读通知</template>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useStore } from "../store";
import { updateUnread, updateRead, acceptNotification, rejectNotification, setRead } from "../utils/api";
import { useMessage } from "naive-ui";
const store = useStore();
const message = useMessage();
const intervalId = ref(null);
const handleAcceptNotification = async (notificationId) => {
    try {
        await acceptNotification(notificationId);
        message.success("同意请求成功");
    } catch (error) {
        message.error("同意请求失败");
    }
    await updateUnread();
};

const handleRejectNotification = async (notificationId) => {
    try {
        await rejectNotification(notificationId);
        message.success("拒绝请求成功");
    } catch (error) {
        message.error("拒绝请求失败");
    }
    await updateUnread();
};

const handleSetRead = async (notificationId) => {
    try {
        await setRead(notificationId);

    } catch (error) {
        message.error("设置已读失败");
    }
    let notification = store.unreadNotifications.filter((item)=> item.id == notificationId)[0];
    store.unreadNotifications = store.unreadNotifications.filter((item)=> item.id != notificationId);
    store.readNotifications.unshift(notification);
};

onMounted(() => {
    intervalId.value = setInterval(updateRead, 30000);
    updateRead();
});

onUnmounted(() => {
    clearInterval(intervalId.value);
});

</script>


