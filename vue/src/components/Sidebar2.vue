<template>
    <div class="sidebar-container">
      <el-menu class="permission-menu"         
      @select="handleMenuSelect"  
      :default-active="activeMenu" >

        <!-- 权限设置主菜单 -->
        <el-sub-menu index="permission">
          <template #title>
            <el-icon class="menu-icon"><Lock /></el-icon>
            <span class="menu-title">权限设置</span>
          </template>

          <!-- 二级菜单项 -->
          <el-menu-item index="user-list">
            <el-icon><User /></el-icon>
            <template #title>用户列表</template>
          </el-menu-item>

          <el-menu-item index="role-list">
            <el-icon><Avatar /></el-icon>
            <template #title>角色列表</template>
          </el-menu-item>

          <el-menu-item index="menu-list">
            <el-icon><Menu /></el-icon>
            <template #title>菜单列表</template>
          </el-menu-item>

          <el-menu-item index="resource-list">
            <el-icon><Files /></el-icon>
            <template #title>资源列表</template>
          </el-menu-item>

          <el-menu-item index="data-list">
            <el-icon><DataAnalysis /></el-icon>
            <template #title>数据列表</template>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter, useRoute} from 'vue-router';
import {
  Lock,
  User,
  Avatar,
  Menu,
  Files,
  DataAnalysis
} from '@element-plus/icons-vue';

const router = useRouter();
const route = useRoute(); 

const activeMenu = computed(() => {
  const pathMap = {
    '/ums/user': 'user-list',
    '/ums/role': 'role-list',
    '/ums/menu': 'menu-list',
    '/ums/resource': 'resource-list',
    '/ums/data': 'data-list'
  };
  return pathMap[route.path] || '';
});

// 菜单选择处理函数
const handleMenuSelect = (index) => {
  const routeMap = {
    "user-list": "/ums/user",
    "role-list": "/ums/role",
    "menu-list": "/ums/menu",
    "resource-list": "/ums/resource",
    "data-list": "/ums/data"
  };
  
  if (routeMap[index]) {
    router.push(routeMap[index]);
  }
};
</script>

<style scoped>
.sidebar-container {
  height: 100vh;
  background: #f8f9fa;
  border-right: 1px solid #e6e6e6;
}

.permission-menu {
  border-right: none;
}

.menu-icon {
  vertical-align: middle;
  margin-right: 8px;
}

.menu-title {
  font-weight: 600;
  color: #2c3e50;
}

.el-menu-item {
  transition: all 0.3s;
}

.el-menu-item:hover {
  background-color: #ecf5ff;
}

.el-menu-item.is-active {
  background-color: #ecf5ff;
  color: #409eff;
  border-right: 3px solid #409eff;
}
</style>
