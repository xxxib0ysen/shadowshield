import { createRouter, createWebHashHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Setting from '../views/Setting.vue';


const routes = [
  { path: '/', component: Home },
  { path: '/settings', component: Setting, }

];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export default router;
