<template>
	<n-tabs type="line" animated>
		<n-tab-pane name="修改用户名" tab="修改用户名">
			<ModifyUsername />
		</n-tab-pane>
		<n-tab-pane name="修改密码" tab="修改密码">
			<ModifyPassword />
		</n-tab-pane>
		<n-tab-pane name="修改头像" tab="修改头像">
			<Suspense>
				<ModifyAvatar />
			</Suspense>
		</n-tab-pane>
	</n-tabs>
</template>