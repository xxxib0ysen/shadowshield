<template>
  <el-container class="layout-container">
    <sidebar />
    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<script setup>
import Sidebar from "@/components/Sidebar.vue";
</script>

<style>
.layout-container {
  height: 100vh;
}
</style>
