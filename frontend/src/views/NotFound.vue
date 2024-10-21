<template>
	<n-result status="404" title="404 资源不存在" description="你似乎来到了没有功德存在的荒原......">
		<template #footer>
			<n-button @click="$router.push({ name: 'Home' })">返回首页</n-button>
		</template>
	</n-result>
</template>
