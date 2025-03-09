import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import 'element-plus/dist/index.css'
import router from './router'

const app = createApp(App)

app.use(router) // 注册路由

app.use(ElementPlus, { locale: zhCn }) // 注册 Element Plus
app.mount('#app')
