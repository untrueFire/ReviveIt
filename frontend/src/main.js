import { createApp } from 'vue'
import { createPinia } from 'pinia'
import naive from "naive-ui"
import router from './router'
import App from './App.vue'
import './assets/styles.css'

const app = createApp(App)
const pinia = createPinia()
app.use(naive)
app.use(pinia)
app.use(router)

app.mount('#app')
