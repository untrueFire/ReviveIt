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
		const response = await axios.get('http://localhost:8000/api/user/', {
			withCredentials: true
		});
		return response.data;
	} catch (error) {
		console.log('获取用户信息失败:', error);
		throw error;
	}
}

export async function fetchUserItems() {
	try {
		const response = await axios.get('http://localhost:8000/api/user/items/', {
			withCredentials: true
		});
		return response.data;
	} catch (error) {
		console.log('获取用户物品失败:', error);
		throw error;
	}
}

export async function deleteItem(itemId) {
	try {
		const csrfToken = getCookie('csrftoken');
		await axios.post(`http://localhost:8000/api/items/delete/${itemId}/`, '', {
			withCredentials: true,
			headers: {
				'X-CSRFToken': csrfToken
			}
		});
		return itemId;
	} catch (error) {
		console.log('删除物品失败:', error);
		throw error;
	}
}

export async function fetchItem(itemId) {
	try {
		const response = await axios.get(`http://localhost:8000/api/items/${itemId}/`, {
			withCredentials: true
		});
		return response.data;
	} catch (error) {
		console.log('获取物品信息失败:', error);
		throw error;
	}
}

export async function updateItem(itemId, itemData) {
	try {
		const csrfToken = getCookie('csrftoken');
		const response = await axios.post(`http://localhost:8000/api/items/update/${itemId}/`, itemData, {
			withCredentials: true,
			headers: {
				'X-CSRFToken': csrfToken
			}
		});
		return response.data;
	} catch (error) {
		console.log('更新物品失败:', error);
		throw error;
	}
}