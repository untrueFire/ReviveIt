<template>
    <div id="app">
        <h1>ReviveIt</h1>
        <TopMenu />
        <router-view />
    </div>
</template>

<script setup>
import TopMenu from './components/TopMenu.vue';
</script>

<style scoped src="@/assets/css/styles.css"></style>