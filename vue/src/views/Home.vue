<template>
    <el-container class="home-container">
      <el-aside width="200px" class="sidebar">
        <Sidebar1 />
      </el-aside>
      <el-main class="main-content">
        <h2>已保护 {{ daysProtected }} 天</h2>
        <p>火绒正在保护您的电脑</p>
        <el-row class="action-buttons" justify="space-around">
          <el-button type="primary">
            <el-icon><Download /></el-icon>
            检查更新
          </el-button>
          <el-button type="info">
            <el-icon><Document /></el-icon>
            安全日志
          </el-button>
          <el-button type="success">
            <el-icon><Check /></el-icon>
            信任区
          </el-button>
          <el-button type="danger">
            <el-icon><Delete /></el-icon>
            隔离区
          </el-button>
        </el-row>
      </el-main>
    </el-container>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import Sidebar1 from '../components/Sidebar1.vue';
  import { HomeFilled, HelpFilled,RemoveFilled, Platform, Management, Tools, Download, Check, Delete } from '@element-plus/icons-vue';

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
  