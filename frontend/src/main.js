import { createApp } from 'vue';
import { createPinia } from 'pinia'
import App from './App.vue';
import naive from "naive-ui";
import router from './router';
import './assets/css/styles.css';
const app = createApp(App);
const pinia = createPinia();
app.use(naive);
app.use(pinia);
app.use(router);

if (module.hot) {
	module.hot.accept();
}

app.mount('#app');