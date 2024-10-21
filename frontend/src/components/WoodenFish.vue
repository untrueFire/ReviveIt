<template>
	<img width="100" src="/muyu.svg" alt="我是木鱼" @click="handleKnock" :style="style" />
</template>

<script setup>
import { post } from '../utils/api';
import CryptoJS from 'crypto-js';
import { useLoadingBar, useMessage } from "naive-ui";
import { ref, computed } from 'vue';
const message = useMessage();
const loadingBar = useLoadingBar();
const baseStyle = {
	position: 'relative',
	top: '50px',
}
const animeStyle = {
	animation: 'run 0.2s linear'
}
const isAnimePlaying = ref(false);
const style = computed(() => isAnimePlaying.value ? { ...baseStyle, ...animeStyle } : baseStyle);
async function handleKnock() {
	isAnimePlaying.value = true;
	post('/api/user/challenge/').then((data) => {
		const { challenge, difficulty } = data;
		loadingBar.start();
		let nonce = 0;
		let found = false;
		while (!found) {
			nonce += 1;
			const data = `${challenge}${nonce}`;
			const hash = CryptoJS.SHA256(data).toString(CryptoJS.enc.Hex);
			if (hash.endsWith('0'.repeat(difficulty))) {
				found = true;
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
			message.error('点击过快');
		})
	).catch((err) => {
		console.error(err);
		message.error('木鱼被敲坏了......');
	});
	setTimeout(() => { isAnimePlaying.value = false; }, 200);

}
</script>