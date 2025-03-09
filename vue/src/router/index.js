import { createRouter, createWebHashHistory } from 'vue-router';

const routes = [
  { 
    path: '/', 
    redirect: '/login', 
    meta: { title: '登录' }  
  },
  { 
    path: '/login', 
    name: 'Login',
    component: () => import('@/views/ums/Login.vue'),
    meta: { 
      title: '登录'
    }
  },
  { path: '/home',
    component: () => import('@/views/Home.vue'),
    meta: { 
      title: '首页', 
      requiresAuth: true } 
  },
  {
    path: '/ums',
    name: 'UMS',
    redirect: '/ums/user',
    meta: { 
      title: '权限管理',
      icon: 'user-management',
      requiresAuth: true 
    },
    children: [
      {
        path: 'user',
        name: 'UserList',
        component: () => import('@/views/ums/User.vue'),
        meta: { 
          title: '用户列表',
          keepAlive: true 
        }
      },
      {
        path: 'role',
        name: 'RoleList',
        component: () => import('@/views/ums/Role.vue'),
        meta: { 
          title: '角色列表' 
        }
      }
    ]
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Setting.vue'),
    meta: { 
      title: '系统设置',
      requiresAuth: true 
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/404.vue'),
    meta: { 
      title: '404页面',
      hidden: true 
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
});

export default router;
