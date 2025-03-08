import { createRouter, createWebHashHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Setting from '../views/Setting.vue';
import User from '../views/ums/User.vue';
import Login from '../views/ums/Login.vue';



const routes = [
  { path: '/', redirect: '/login', meta: { title: '登录' }  },
  { path: '/login', component: Login },
  { path: '/home', component: Home, meta: { title: '首页', requiresAuth: true } },
  { path: '/:pathMatch(.*)*', component: () => import('../views/404.vue') },
  { path: '/settings', component: Setting},
  { path: '/user', component: User, meta: { title: '用户列表' }  }

];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export default router;
