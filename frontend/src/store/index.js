import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useStore = defineStore("main", () => {
	// const notifications = ref([]);
	const unreadNotifications = ref([]);
	const readNotifications = ref([]);
	const unreadCount = computed(() => {
		return unreadNotifications.value.length;
	});
	const intervalId = ref(null);
	const user = ref();
	const isLoggedIn = computed(() => user.value !== undefined);
	const theme = ref(null);
	return {
		// notifications,
		unreadNotifications,
		readNotifications,
		unreadCount,
		user,
		isLoggedIn,
		intervalId,
		theme
	};
});
