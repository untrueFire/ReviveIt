<template>
  <iframe :src="iframeUrl" class="admin-iframe"></iframe>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

// 将 LocationQuery 转换为 Record<string, string>
const queryParams = Object.fromEntries(
  Object.entries(route.query).map(([key, value]) => [
    key,
    Array.isArray(value) ? value.join(',') : value || ''
  ])
);

// 生成查询参数字符串
const queryString = new URLSearchParams(queryParams).toString();

// 计算 iframe 的 src 属性
const iframeUrl = computed(() => {
  const path = route.params.pathMatch || ''; // 获取 /admin/ 后面的路径
  return `/admin/${path}${queryString ? `?${queryString}` : ''}`; // 构建 iframe URL
});
</script>

<style scoped>
.admin-iframe {
  width: 100%;
  height: 100vh;
  border: none;
}
</style>