import axios from 'axios';

export function getCookie(name) {
	const cookies = document.cookie.split(';');
	for (let cookie of cookies) {
		cookie = cookie.trim();
		if (cookie.startsWith(name + '=')) {
			return cookie.substring(name.length + 1);
		}
	}
	return null;
}
export async function fetchUserInfo() {
	try {
		const response = await axios.get('/api/user/', {
			withCredentials: true
		});
		return response.data;
	} catch (error) {
		console.error(error);
		throw error;
	}
}

export async function fetchUserItems() {
	try {
		const response = await axios.get('/api/user/items/', {
			withCredentials: true
		});
		return response.data;
	} catch (error) {
		console.error(error);
		throw error;
	}
}

export async function deleteItem(itemId) {
	try {
		const csrfToken = getCookie('csrftoken');
		await axios.post(`/api/items/delete/${itemId}/`, '', {
			withCredentials: true,
			headers: {
				'X-CSRFToken': csrfToken
			}
		});
		return itemId;
	} catch (error) {
		console.error(error);
		throw error;
	}
}

export async function fetchItem(itemId) {
	try {
		const response = await axios.get(`/api/items/${itemId}/`, {
			withCredentials: true
		});
		return response.data;
	} catch (error) {
		console.error(error);
		throw error;
	}
}

export async function updateItem(itemId, itemData) {
	try {
		const csrfToken = getCookie('csrftoken');
		const response = await axios.post(`/api/items/update/${itemId}/`, itemData, {
			withCredentials: true,
			headers: {
				'X-CSRFToken': csrfToken
			}
		});
		return response.data;
	} catch (error) {
		console.error(error);
		throw error;
	}
}

export async function fetchNotifications() {
	try {
		const response = await axios.get("/api/user/notifications/", {
			withCredentials: true
		});
		return response.data;
	} catch (error) {
		console.error(error);
		throw error;
	}
}

export async function acceptNotification(notificationId) {
	try {
		const csrfToken = getCookie('csrftoken');
		const response = await axios.post(`/api/notification/accept/${notificationId}/`, null, {
			withCredentials: true,
			headers: {
				'X-CSRFToken': csrfToken
			}
		});
		return response.data;
	} catch (error) {
		console.error(error);
		throw error;
	}
}

export async function rejectNotification(notificationId) {
	try {
		const csrfToken = getCookie('csrftoken');
		const response = await axios.post(`/api/notification/reject/${notificationId}/`, null, {
			withCredentials: true,
			headers: {
				'X-CSRFToken': csrfToken
			}
		});
		return response.data;
	} catch (error) {
		console.error(error);
		throw error;
	}
}

export async function ReviveItem(itemId, price) {
	try {
		const csrfToken = getCookie('csrftoken');
		const response = await axios.post(`/api/items/revive/${itemId}/`, price, {
			withCredentials: true,
			headers: {
				'X-CSRFToken': csrfToken
			}
		});
		return response.data;
	} catch (error) {
		console.error(error);
		throw error;
	}
}

export async function search(query) {
	try {
		const response = await axios.get(
			`/api/search/?q=${encodeURIComponent(query)}`
		);
		return response.data;
	} catch (error) {
		console.error(error);
		throw error;
	}
}

export async function addItem(data) {
	try {
		const csrfToken = getCookie("csrftoken");
		await axios.post("/api/items/add/", data, {
			withCredentials: true,
			headers: {
				"X-CSRFToken": csrfToken,
			},
		});
	} catch (error) {
		console.error(error);
		throw error;
	}
}

export async function setRead(notificationId) {
	try {
		const csrfToken = getCookie('csrftoken');
		const response = await axios.post(`/api/notification/read/${notificationId}/`, null, {
			withCredentials: true,
			headers: {
				'X-CSRFToken': csrfToken
			}
		});
		return response.data;
	} catch (error) {
		console.error(error);
		throw error;
	}
}