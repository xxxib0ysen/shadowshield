<template>
    <el-container class="app-container">
      <Home />
    </el-container>
  </template>
  
  <script setup>
  import Home from './views/Home.vue';
  </script>
  
  <style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  html, body, #app {
    height: 100%;
    width: 100%;
    font-family: Arial, sans-serif;
  }
  .app-container {
    height: 100vh;
  }
  </style>
  