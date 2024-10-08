import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useStore = defineStore("main", () => {
	const notifications = ref([]);
	const unreadNotifications = computed(() => {
		return notifications.value.filter((notification) => notification.unread);
	});
	const readNotifications = computed(() => {
		return notifications.value.filter((notification) => !notification.unread);
	});
	const unreadCount = computed(() => {
		return unreadNotifications.value.length;
	});
	const intervalId = ref(null);
	const user = ref();
	const isLoggedIn = computed(() => user.value !== undefined);
	return {
		notifications,
		unreadNotifications,
		readNotifications,
		unreadCount,
		user,
		isLoggedIn,
		intervalId
	};
});
