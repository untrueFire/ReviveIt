<template>
    <div>
        <n-alert type="info" :bordered="false"
            >请勿点击过快，否则可能会被认为是心不诚</n-alert
        >
        <WoodenFish />
    </div>
</template>

<script setup lang="ts">
import WoodenFish from '@/components/WoodenFish.vue'
</script>
