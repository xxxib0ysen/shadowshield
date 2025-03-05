import { createRouter, createWebHashHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Setting from '../views/Setting.vue';
import User from '../views/User.vue';


const routes = [
  { path: '/', component: Home },
  { path: '/settings', component: Setting},
  { path: '/users', component: User }

];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export default router;
