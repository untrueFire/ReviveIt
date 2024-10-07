<template>
  <div class="notifications-container">
    <template v-if="unreadNotifications.length > 0">
      <h2>未读通知</h2>
      <ul>
        <li v-for="notification in unreadNotifications" :key="notification.id">
          <template v-if="notification.verb == 'proposed'">
            {{ notification.actor.username }} 请求以
            {{ notification.action_object.price }} 功德的代价复活
            {{ notification.action_object.target.name }}
          </template>
          <template v-else-if="notification.verb == 'accepted'">
            {{ notification.actor.username }} 接受了你以
            {{ notification.action_object.price }} 功德的代价复活
            {{ notification.action_object.target.name }} 的请求
          </template>
          <template v-else-if="notification.verb == 'rejected'">
            {{ notification.actor.username }} 拒绝了你以
            {{ notification.action_object.price }} 功德的代价复活
            {{ notification.action_object.target.name }} 的请求
          </template>
          <template v-if="notification.verb == 'proposed'">
            <button @click="handleAcceptNotification(notification.id)">
              接受
            </button>
            <button @click="handleRejectNotification(notification.id)">
              拒绝
            </button>
          </template>
          <template
            v-else-if="
              notification.verb == 'accepted' || notification.verb == 'rejected'
            "
          >
            <button @click="handleSetRead(notification.id)">已读</button>
          </template>
        </li>
      </ul>
    </template>
    <template v-else><p>暂无未读通知</p></template>
    <template v-if="readNotifications.length > 0">
      <h2>已读通知</h2>
      <ul>
        <li v-for="notification in readNotifications" :key="notification.id">
          <template v-if="notification.verb == 'proposed'">
            {{ notification.actor.username }} 请求以
            {{ notification.action_object.price }} 功德的代价复活
            {{ notification.action_object.target.name }}
            <template v-if="notification.data == 'accepted'">（已同意）</template>
            <template v-else>（已拒绝）</template>
          </template>
          <template v-else-if="notification.verb == 'accepted'">
            {{ notification.actor.username }} 接受了你以
            {{ notification.action_object.price }} 功德的代价复活
            {{ notification.action_object.target.name }} 的请求
          </template>
          <template v-else-if="notification.verb == 'rejected'">
            {{ notification.actor.username }} 拒绝了你以
            {{ notification.action_object.price }} 功德的代价复活
            {{ notification.action_object.target.name }} 的请求
          </template>
        </li>
      </ul>
    </template>
    <template v-else>暂无已读通知</template>
  </div>
</template>

  <script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useToast } from "vue-toastification";
import {
  fetchNotifications,
  acceptNotification,
  rejectNotification,
  setRead,
} from "@/utils/api";

const notifications = ref([]);
const toast = useToast();
let intervalId = null;

const fetchData = async () => {
  try {
    notifications.value = await fetchNotifications();
  } catch (error) {
    console.error("获取通知失败", error);
  }
};

const unreadNotifications = computed(() => {
  return notifications.value.filter((notification) => notification.unread);
});

const readNotifications = computed(() => {
  return notifications.value.filter((notification) => !notification.unread);
});

const handleAcceptNotification = async (notificationId) => {
  try {
    await acceptNotification(notificationId);
    await fetchData();
    toast.success("同意请求成功");
  } catch (error) {
    toast.error("同意请求失败");
  }
};

const handleRejectNotification = async (notificationId) => {
  try {
    await rejectNotification(notificationId);
    await fetchData();
    toast.success("拒绝请求成功");
  } catch (error) {
    toast.error("拒绝请求失败");
  }
};

const handleSetRead = async (notificationId) => {
  try {
    await setRead(notificationId);
    await fetchData();
  } catch (error) {
    toast.error("设置已读失败");
  }
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