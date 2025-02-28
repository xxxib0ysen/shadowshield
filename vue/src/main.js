import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'

const app = createApp(App)
app.use(router) // 注册路由

app.use(ElementPlus) // 注册 Element Plus
app.mount('#app')
