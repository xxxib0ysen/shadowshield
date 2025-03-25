<template>
  <el-container style="height: 100vh;">
    <el-container>

      <el-header height="80px" style="padding-left: 24px;">
        <div>
          <el-text tag="h1" size="large" style="font-weight: bold;">访问控制</el-text>
          <div style="margin-top: 10px;">
            <el-text type="info">通过设定规则，控制用户对电脑资源的访问</el-text>
          </div>
        </div>
      </el-header>

      <el-main>
        <el-row :gutter="20">
          <el-col :span="12" v-for="item in controlList" :key="item.key">
            <el-card shadow="hover" style="cursor: pointer;" @click="() => goTo(item.route)">
              <div style="display: flex; align-items: flex-start; gap: 12px;">
                <img :src="item.icon" alt="icon" style="width: 32px; height: 32px;" />
                <div style="flex: 1;">
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span class="card-title">{{ item.title }}</span>
                    <el-tag size="small" :type="item.status === '1' ? 'success' : 'info'">
                      {{ item.status === '1' ? '已开启' : '未开启' }}
                    </el-tag>
                  </div>
                  <el-text type="info" size="small" style="margin-top: 6px;">{{ item.desc }}</el-text>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
      
    </el-container>
  </el-container>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getSetting } from '@/api/system/setting'

const router = useRouter()
const status = ref('0')

onMounted(async () => {
  const res = await getSetting('website_blocking_enabled')
  if (res.code === 200) {
    status.value = res.data
  }
})

// 路由跳转
const goTo = (route) => {
  router.push(route)
}

// 获取设置状态
onMounted(async () => {
  const res = await getSetting('website_blocking_enabled')
  if (res.code === 200) {
    status.value = res.data
  }
})

// 控制功能模块列表
const controlList = ref([
  {
    key: 'website',
    title: '网站内容控制',
    desc: '限制计算机访问特定类型网站',
    status: status.value,
    route: '/control/custom_rule',
    icon: new URL('@/components/icons/互联网.svg', import.meta.url).href
  },
  {
    key: 'website',
    title: '网站内容控制',
    desc: '限制计算机访问特定类型网站',
    status: status.value,
    route: '/control/custom_rule',
    icon: new URL('@/components/icons/互联网.svg', import.meta.url).href
  }
])
</script>
