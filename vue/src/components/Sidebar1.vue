<template>
    <el-menu default-active="1" class="el-menu-vertical" :collapse="isCollapse">
      <el-menu-item index="1">
        <el-icon><HomeFilled /></el-icon>
        <template #title>首页</template>
      </el-menu-item>
      <el-menu-item index="2">
        <el-icon><HelpFilled /></el-icon>
        <span>浏览保护</span>
      </el-menu-item>
      <el-menu-item index="3">
        <el-icon><RemoveFilled /></el-icon>
        <span>广告拦截</span>
      </el-menu-item>
      <el-menu-item index="4">
        <el-icon><Platform /></el-icon>
        <span>监控防护</span>
      </el-menu-item>
      <el-menu-item index="5">
        <el-icon><Management /></el-icon>
        <span>日志分析</span>
      </el-menu-item>
      <el-menu-item index="6">
        <el-icon><Tools /></el-icon>
        <span>上网管理</span>
      </el-menu-item>
      <el-menu-item index="7" @click="openSettings">
        <el-icon><Setting /></el-icon>
        <span>系统设置</span>
      </el-menu-item>
    </el-menu>
</template>
  
<script setup>
import { ref } from 'vue';
import { 
    HomeFilled,
    HelpFilled,
    RemoveFilled,
    Platform,
    Management,
    Tools,
    Setting
} from '@element-plus/icons-vue';

const isCollapse = ref(false);

const openSettings = () => {
    window.electronAPI.openSettingsWindow(); // 触发 Electron 事件，打开新窗口
};
</script>
