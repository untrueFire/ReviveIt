<template>
  <div id="app">
    <TopMenu/>
    <router-view />
  </div>
</template>

<script setup>
import TopMenu from './components/TopMenu.vue';
</script>

<style scoped src="@/assets/css/styles.css"></style>