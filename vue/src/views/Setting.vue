<template>
    <el-container>
      <el-aside width="220px">
        <Sidebar2 />
      </el-aside>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </template>
  
  <script setup>
  import Sidebar2 from '@/components/Sidebar2.vue'
  </script>