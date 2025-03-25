<template>
  <el-container class="home-container">
    <el-main class="main-content">

      <div class="top-text">
        <div class="days">
          已保护 <span class="highlight">{{ daysProtected }}</span> 天
        </div>
        <h2 class="headline">正在保护您的电脑</h2>
      </div>

    </el-main>

    <div class="bottom-bar">

      <div class="left-buttons">
        <div
          v-for="(item, index) in buttons"
          :key="index"
          class="action-col"
        >
          <div class="icon-circle">
            <img :src="item.icon" class="svg-icon" />
          </div>
          <div class="label">{{ item.label }}</div>
        </div>
      </div>


      <div class="footer-info">
        <span>版本：xxx</span>
        <span>规则库：2025-03-25 18:36</span>
      </div>
    </div>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'

const daysProtected = ref(90)

import iconUpdate from '@/components/icons/update.svg'
import iconLog from '@/components/icons/log.svg'
import iconCheck from '@/components/icons/check.svg'
import iconQuarantine from '@/components/icons/错误.svg'

const buttons = [
  { label: '检查更新', icon: iconUpdate },
  { label: '安全日志', icon: iconLog },
  { label: '信任区', icon: iconCheck },
  { label: '隔离区', icon: iconQuarantine }
]
</script>

<style scoped>
.home-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f9f9f9;
}

.main-content {
  flex: 1;
  padding: 40px;
}

/* 顶部文字 */
.top-text {
  margin-bottom: 20px;
}
.days {
  font-size: 20px;
}
.days .highlight {
  color: #f90;
  font-weight: bold;
}
.headline {
  font-size: 26px;
  font-weight: bold;
  margin: 10px 0;
}

/* 底部栏：两端对齐 */
.bottom-bar {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding: 20px 40px;
  background-color: #fff;
  border-top: 1px solid #eee;
}

/* 左下角功能区 */
.left-buttons {
  display: flex;
  gap: 40px;
}
.action-col {
  text-align: center;
}
.icon-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #fff;
  margin: 0 auto 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #eee;
}
.svg-icon {
  width: 22px;
  height: 22px;
}
.label {
  font-size: 14px;
  color: #333;
}

/* 右下角版本信息 */
.footer-info {
  text-align: right;
  font-size: 13px;
  color: #888;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}
</style>
