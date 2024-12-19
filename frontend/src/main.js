import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import socketPlugin from './plugins/socket'; 
import { useUserStore } from './store/store'; 
import './assets/tailwind.css';
import Toast from 'vue-toastification'; 
import 'vue-toastification/dist/index.css';

const app = createApp(App);
const pinia = createPinia(); 

app.use(pinia); 
app.use(router);
app.use(socketPlugin); 
app.use(Toast); 

const userStore = useUserStore();
userStore.initializeFromToken(); 

app.mount('#app');
