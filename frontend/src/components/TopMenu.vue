<template>
    <nav class="top-menu">
        <n-menu mode="horizontal" :options="menuOptions" />
    </nav>
</template>

<script setup>
import { RouterLink } from "vue-router";
import NotificationButton from "@/components/NotificationButton.vue";
import { useStore } from "@/store";
import { h, computed } from "vue";
import { useMessage } from "naive-ui";
import SwitchTheme from "@/components/SwitchTheme.vue";
const store = useStore();
window.$message = useMessage();
const menuOptions = computed(() => [
    {
        label: () =>
            h(
                RouterLink,
                {
                    to: {
                        name: "Home",
                    },
                },
                { default: () => "广场" }
            ),
        key: "home",
    },
    {
        label: () =>
            h(
                RouterLink,
                {
                    to: {
                        name: "Login",
                    },
                },
                { default: () => "登录" }
            ),
        key: "login",
        show: !store.isLoggedIn,
    },
    {
        label: () =>
            h(
                RouterLink,
                {
                    to: {
                        name: "Register",
                    },
                },
                { default: () => "注册" }
            ),
        key: "register",
        show: !store.isLoggedIn,
    },
    {
        label: () =>
            h(
                RouterLink,
                {
                    to: {
                        name: "User",
                    },
                },
                { default: () => "我的" }
            ),
        key: "user",
        show: store.isLoggedIn,
    },
    {
        label: () =>
            h(
                RouterLink,
                {
                    to: {
                        name: "Logout",
                    },
                },
                { default: () => "登出" }
            ),
        key: "logout",
        show: store.isLoggedIn,
    },
    {
        label: () =>
            h(
                RouterLink,
                {
                    to: {
                        name: "AddItem",
                    },
                },
                { default: () => "添加物品" }
            ),
        key: "additem",
        show: store.isLoggedIn,
    },
    {
        label: () =>
            h(
                RouterLink,
                {
                    to: {
                        name: "WoodenFish",
                    },
                },
                { default: () => "木鱼" }
            ),
        key: "woodenfish",
        show: store.isLoggedIn,
    },
    {
        label: () => h(NotificationButton),
        key: "notification",
        show: store.isLoggedIn,
    },
    {
        label: () => h(SwitchTheme),
        key: "switchtheme"
    }
]);
</script>

<style scoped src="@/assets/css/styles.css"></style>