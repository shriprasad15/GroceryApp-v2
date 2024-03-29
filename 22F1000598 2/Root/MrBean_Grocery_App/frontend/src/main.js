

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS


// import 'bootstrap';
import './registerServiceWorker'
const app = createApp(App)

app.use(router)

app.mount('#app')