import axios, { AxiosError } from 'axios';
import { useStore } from '../store';
function getCookie(name) {
	const cookies = document.cookie.split(';');
	for (let cookie of cookies) {
		cookie = cookie.trim();
		if (cookie.startsWith(name + '=')) {
			return cookie.substring(name.length + 1);
		}
	}
	return null;
}

export async function getCsrftoken() {
	if (!document.cookie.includes("csrftoken")) {
		await get("/accounts/login");
	}
	return getCookie("csrftoken");
}

function errorHandler(error) {
	if (error instanceof AxiosError && error.response && error.response.status == 403 && error.response.data &&
		error.response.data.detail == '身份认证信息未提供。') {
		const store = useStore();
		if (!store.isLoggedIn) {
			return undefined;
		}
		store.user = undefined;
		const message = window.$message;
		message.error('登录失效');
		clearInterval(store.intervalId);
		window.location.href = '/login';
	} else {
		throw error;
	}
}

export async function get(url) {
	try {
		const response = await axios.get(url, {
			withCredentials: true,
		});
		return response.data;
	} catch (error) {
		errorHandler(error);
	}
}

export async function post(url, data) {
	try {
		const response = await axios.post(url, data, {
			withCredentials: true,
			headers: {
				'X-CSRFToken': await getCsrftoken(),
			},
		});
		return response.data;
	} catch (error) {
		errorHandler(error);
	}
}

export const fetchUserInfo = () => get('/api/user/');
export const fetchUserItems = () => get('/api/user/items/');
export const deleteItem = (itemId) => post(`/api/items/delete/${itemId}/`, '');
export const fetchItem = (itemId) => get(`/api/items/${itemId}/`);
export const updateItem = (itemId, itemData) =>
	post(`/api/items/update/${itemId}/`, itemData);
export const fetchUnread = () => get('/api/user/notifications/unread/');
export const fetchRead = () => get('/api/user/notifications/read/');
export const acceptNotification = (notificationId) =>
	post(`/api/notification/accept/${notificationId}/`, null);
export const rejectNotification = (notificationId) =>
	post(`/api/notification/reject/${notificationId}/`, null);
export const ReviveItem = (itemId, price) =>
	post(`/api/items/revive/${itemId}/`, price);
export const search = (query) =>
	get(`/api/search/?q=${encodeURIComponent(query)}`);
export const addItem = (data) => post('/api/items/add/', data);
export const setRead = (notificationId) =>
	post(`/api/notification/read/${notificationId}/`, null);
export const logout = () => post('/accounts/logout/');

export const updateUnread = async () => {
	fetchUnread()
		.then((data) => {
			const store = useStore();
			store.unreadNotifications = data;
		})
		.catch(() => { });
};

export const updateRead = async () => {
	fetchRead()
		.then((data) => {
			const store = useStore();
			store.readNotifications = data;
		})
		.catch(() => { });
};

export const updateUser = async () => {
	const store = useStore();
	store.user = await fetchUserInfo();
}