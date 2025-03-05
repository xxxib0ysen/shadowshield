<template>
  <div class="sidebar-container">
    <!-- 侧边栏菜单 -->
    <el-menu default-active="1" class="el-menu-vertical-demo">
      <el-menu-item index="1">
        <el-icon><HomeFilled /></el-icon>
        <template #title>首页</template>
      </el-menu-item>

      <el-menu-item index="2">
        <el-icon><HelpFilled /></el-icon>
        <template #title>浏览保护</template>
      </el-menu-item>

      <el-menu-item index="3">
        <el-icon><RemoveFilled /></el-icon>
        <template #title>广告拦截</template>
      </el-menu-item>

      <el-menu-item index="4">
        <el-icon><Platform /></el-icon>
        <template #title>监控防护</template>
      </el-menu-item>

      <el-menu-item index="5">
        <el-icon><Management /></el-icon>
        <template #title>日志分析</template>
      </el-menu-item>

      <el-menu-item index="6">
        <el-icon><Tools /></el-icon>
        <template #title>上网管理</template>
      </el-menu-item>

      <el-menu-item index="7" @click="openSettings">
        <el-icon><Setting /></el-icon>
        <template #title>系统设置</template>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup>
import { 
  HomeFilled,
  HelpFilled,
  RemoveFilled,
  Platform,
  Management,
  Tools,
  Setting
} from '@element-plus/icons-vue';

const openSettings = () => {
  window.electronAPI.openSettingsWindow(); // 触发 Electron 事件，打开新窗口
};
</script>

<style scoped>
.sidebar-container {
  width: 200px;
  height: 100vh;
  background: #f8f9fa;
  border-right: 1px solid #e6e6e6;
}

.el-menu-vertical-demo {
  width: 100%;
  min-height: 100vh;
}
</style>
