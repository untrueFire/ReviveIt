<template>
    <img
        draggable="false"
        width="100"
        src="@/assets/muyu.svg"
        alt="我是木鱼"
        @click="handleKnock"
        :style="style"
    />
</template>

<script setup lang="ts">
import { post } from '@/utils/api'
import CryptoJS from 'crypto-js'
import { useLoadingBar, useMessage } from 'naive-ui'
import { ref, computed, type StyleValue } from 'vue'
import { useStore, useThemeStore } from '@/stores'
import type { User } from '@/types/Api'
const message = useMessage()
const loadingBar = useLoadingBar()
const store = useStore()
const themeStore = useThemeStore()
const isAnimePlaying = ref(false)
const style = computed(() => {
    const res: StyleValue = {
        position: 'relative',
        top: '50px',
    }
    if (isAnimePlaying.value) {
        res.animation = 'run 0.2s linear'
    }
    if (themeStore.themeName === 'dark') {
        res.filter = 'invert(1)'
    }
    return res
})
async function handleKnock() {
    isAnimePlaying.value = true
    post('/api/user/challenge/')
        .then(data => {
            const { challenge, difficulty } = data
            loadingBar.start()
            let nonce = 0
            let found = false
            while (!found) {
                nonce += 1
                const data = `${challenge}${nonce}`
                const hash = CryptoJS.SHA256(data).toString(CryptoJS.enc.Hex)
                if (hash.endsWith('0'.repeat(difficulty))) {
                    found = true
                }
            }
            return nonce.toString()
        })
        .then(nonce =>
            post('/api/user/knock/', { nonce })
                .then(() => {
                    (store.user as User).balance += 1
                    loadingBar.finish()
                    message.success('功德+1')
                })
                .catch(err => {
                    loadingBar.error()
                    console.error(err)
                    message.error('点击过快')
                }),
        )
        .catch(err => {
            console.error(err)
            message.error('木鱼被敲坏了......')
        })
    setTimeout(() => {
        isAnimePlaying.value = false
    }, 200)
}
</script>

<style>
@keyframes run {
    0% {
        transform: scale(1);
    }

    50% {
        transform: scale(0.8);
    }

    100% {
        transform: scale(1);
    }
}
</style>
