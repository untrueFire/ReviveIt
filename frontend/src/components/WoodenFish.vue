<template>
	<n-button @click="handleKnock" type="primary">我是木鱼</n-button>
</template>

<script setup>
import { post } from '../utils/api';
import CryptoJS from 'crypto-js';
import { useLoadingBar, useMessage } from "naive-ui";
const message = useMessage();
const loadingBar = useLoadingBar();
async function handleKnock() {
	post('/api/user/challenge/').then((response) => {
		const { challenge, difficulty } = response;
		loadingBar.start();
		let nonce = 0;
		while (true) {
			nonce += 1;
			const data = `${challenge}${nonce}`;
			const hash = CryptoJS.SHA256(data).toString(CryptoJS.enc.Hex);
			if (hash.endsWith('0'.repeat(difficulty))) {
				break;
			}
		}
		return nonce.toString();
	}).then((nonce) =>
		post('/api/user/knock/', { nonce }).then(() => {
			loadingBar.finish();
			message.success('功德+1');
		}).catch((err) => {
			loadingBar.error();
			console.error(err);
			message.error('失败了失败了失败了');
		})
	).catch((err) => {
		console.error(err);
		message.error('出师未捷身先死');
	})
}
</script>