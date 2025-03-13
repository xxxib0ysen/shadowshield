import { createRouter, createWebHashHistory } from 'vue-router';

const routes = [
  { 
    path: '/', 
    redirect: '/login' 
  },
  { 
    path: '/login', 
    name: 'Login', 
    component: () => import('@/views/ums/Login.vue') 
  },
  { 
    path: '/home', 
    name: 'home', 
    component: () => import('@/views/Home.vue') 
  },

  { 
    path: '/setting', 
    name: 'Setting', 
    component: () => import('@/views/Setting.vue'), 
    meta:{ windowKey: "B"},
    children: [
      {
        path: 'ums', 
        name: 'UMS',
        children: [
          { 
            path: 'user',
             name: 'user', 
             component: () => import('@/views/ums/User.vue') 
            },
          { 
            path: 'role', 
            name: 'role', 
            component: () => import('@/views/ums/Role.vue') 
          },
          { 
            path: 'menu', 
            name: 'menu', 
            component: () => import('@/views/ums/Menu.vue')
          },
          { 
            path: 'resource', 
            name: 'resource', 
            component: () => import('@/views/ums/Resource.vue') 
          },
          { 
            path: 'permission', 
            name: 'permission', 
            component: () => import('@/views/ums/Permission.vue') 
          }
      
        ]
      }     
    ]
},
  { 
    path: '/:pathMatch(.*)*', 
    name: 'NotFound', 
    component: () => import('@/views/404.vue') 
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export default router;
