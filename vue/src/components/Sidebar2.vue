<template>
    <div class="sidebar-container">
      <el-menu class="permission-menu">
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
import { useRouter } from 'vue-router';
import {
  Lock,
  User,
  Avatar,
  Menu,
  Files,
  DataAnalysis
} from '@element-plus/icons-vue';
</script>

const router = useRouter();

const handleMenuSelect = (index) => {
  const routeMap = {
    "user-list": "/users",
    "role-list": "/roles",
    "menu-list": "/menus",
    "resource-list": "/resources",
    "data-list": "/data"
  };
  
  if (routeMap[index]) {
    router.push(routeMap[index]);
  }
};

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
