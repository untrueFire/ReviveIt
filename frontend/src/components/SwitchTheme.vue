<template>
	<n-icon>
		<LightModeFilled v-if="store.theme !== null" @click="store.theme = null" />
		<DarkModeFilled v-else @click="store.theme = darkTheme" />
	</n-icon>
</template>

<script setup>
import { useStore } from '@/store';
import { LightModeFilled, DarkModeFilled } from '@vicons/material';
import { darkTheme } from 'naive-ui';
const store = useStore();
</script>