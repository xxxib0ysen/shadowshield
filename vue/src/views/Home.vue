<template>
    <el-container class="home-container">
      <el-aside width="200px" class="sidebar">
        <el-menu default-active="1" class="el-menu-vertical">
          <el-menu-item index="1">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="2">
            <el-icon><Monitor /></el-icon>
            <span>浏览保护</span>
          </el-menu-item>
          <el-menu-item index="3">
            <el-icon><Promotion /></el-icon>
            <span>广告拦截</span>
          </el-menu-item>
          <el-menu-item index="4">
            <el-icon><Shield /></el-icon>
            <span>监控防护</span>
          </el-menu-item>
          <el-menu-item index="5">
            <el-icon><Document /></el-icon>
            <span>日志分析</span>
          </el-menu-item>
          <el-menu-item index="6">
            <el-icon><Setting /></el-icon>
            <span>上网管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="main-content">
        <h2>已保护 {{ daysProtected }} 天</h2>
        <p>火绒正在保护您的电脑</p>
        <el-row class="action-buttons" justify="space-around">
          <el-button type="primary" icon="Upload">检查更新</el-button>
          <el-button type="info" icon="Document">安全日志</el-button>
          <el-button type="success" icon="Check">信任区</el-button>
          <el-button type="danger" icon="Close">隔离区</el-button>
        </el-row>
      </el-main>
    </el-container>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { HomeFilled, Monitor, Promotion, Shield, Document, Setting, Upload, Check, Close } from '@element-plus/icons-vue';
  
  const daysProtected = ref(46);
  </script>
  
  <style scoped>
  .home-container {
    height: 100vh;
    display: flex;
  }
  .sidebar {
    background: #f8f9fa;
    height: 100vh;
  }
  .main-content {
    text-align: center;
    padding: 20px;
  }
  .action-buttons {
    margin-top: 20px;
  }
  </style>
  