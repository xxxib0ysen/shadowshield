import { createRouter, createWebHashHistory } from 'vue-router';

const routes = [
  { 
    path: '/', 
    redirect: '/login' ,
    component: () => import('@/layout/Layout.vue'),
    children: [
      { 
        path: '/home', 
        name: 'home', 
        component: () => import('@/views/Home.vue') 
      },
    ]
  },
  { 
    path: '/login', 
    name: 'Login', 
    component: () => import('@/views/ums/Login.vue') 
  },

  {
    path: '/control',
    component: () => import('@/layout/Layout.vue'),
    children: [
      {
        path: '',
        name: 'control',
        component: () => import('@/views/control/Control.vue')
      },
      {
        path: 'custom_rule',
        name: 'custom_rule',
        component: () => import('@/views/control/Website.vue')
      }
    ]
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
      } ,
      {
        path: 'rule',
        name: 'rule',
        redirect: '/setting/rule/adblock',
        children: [
          {
            path: 'adblock',
            name: 'adblock',
            component: () => import('@/views/rule/AdblockSource.vue')
          },
          {
            path: 'website_control',
            name: 'website_control',
            component: () => import('@/views/rule/WebsiteControl.vue')
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
