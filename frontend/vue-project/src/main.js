// import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap'
import 'jquery' //main.js導入(全域)

const app = createApp(App)

// app.use(router)

app.mount('#app')
