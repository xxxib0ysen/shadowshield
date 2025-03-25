<template>
  <el-container style="padding: 16px;">
    <el-header height="auto" style="padding: 0;">
      <el-row justify="space-between" align="middle">
        <el-col>
          <el-space :size="12" alignment="center">
            <img 
              src="../../components/icons/返回.svg" 
              alt="返回" 
              class="back-icon"
              @click="goBack" 
              />
            <el-text tag="h2" size="large" style="font-weight: bold;">网站内容控制</el-text>
          </el-space>
        </el-col>
        <el-col>
          <el-space>
            <el-text>限制计算机访问特定类型网站：</el-text>
            <el-switch v-model="blockingEnabled" @change="onToggleBlocking" />
          </el-space>
        </el-col>
      </el-row>
    </el-header>

    <el-main>
      <el-tabs v-model="activeTab">
        <!-- 功能设置页 -->
        <el-tab-pane label="功能设置" name="function">
          <el-text tag="h3" size="medium" style="font-weight: bold;">网站类型</el-text>
          <el-space direction="vertical" fill :size="16" style="margin-top: 16px;width: 100%;"> 
            <el-card 
              v-for="type in websiteTypes" 
              :key="type.type_id" 
              shadow="never"
              body-style="padding: 16px;">
              <el-row justify="space-between" align="middle">
                <el-col :span="20">
                  <el-space alignment="center">
                    <el-icon><component :is="type.icon" /></el-icon>
                    <el-text>{{ type.type_name }}</el-text>
                  </el-space>
                </el-col>
                <el-col :span="4" style="text-align: right;">
                  <el-switch
                    v-model="type.status"
                    @change="toggleTypeStatus(type)"
                    :disabled="!blockingEnabled"
                  />
                </el-col>
              </el-row>
            </el-card>
          </el-space>
        </el-tab-pane>

        <!-- 自定义规则页 -->
        <el-tab-pane label="自定义规则" name="custom">
          <el-row class="toolbar" justify="space-between" align="middle" style="margin-bottom: 10px;">
            <el-button :disabled="!multipleSelection.length" @click="batchDeleteCustom">删除所选</el-button>
            <el-button type="primary" @click="showImport = true">
              添加
            </el-button>
          </el-row>
          
          <el-table
            :data="customRules"
            border
            ref="customTable"
            style="width: 100%"
            @selection-change="handleSelectionChange"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="website_url" label="受控网站" />
            <el-table-column label="状态">
              <template #default="{ row }">
                <el-switch
                  v-model="row.status"
                  :active-value="1"
                  :inactive-value="0"
                  @change="toggleCustomRule(row)"
                  :disabled="!blockingEnabled"
                />
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template #default="{ row }">
                <el-button type="text" @click="handleDeleteCustom(row.id)">删除</el-button>
              </template>
            </el-table-column>

             <!-- 空状态展示 -->
            <template #empty>
              <div style="text-align: center; padding: 40px 0;">
                <div style="color: #999; font-size: 14px; margin-top: 10px;">
                  添加网站阻止应用程序访问
                </div>
              </div>
    </template>

          </el-table>

          <!-- 添加规则弹窗 -->
          <el-dialog v-model="showImport" title="添加网址规则" width="500px">
            <el-input
              type="textarea"
              v-model="importText"
              placeholder="每行一个网址，支持 * 和 > 通配符"
              :rows="10"
            />
            <template #footer>
              <el-button @click="showImport = false">取消</el-button>
              <el-button type="primary" @click="submitImport">提交</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>
      </el-tabs>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  getWebsiteType,
  updateWebsiteTypeStatus
} from '@/api/rule/website_control'
import {
  getCustomRules,
  updateCustomRuleStatus,
  deleteCustomRule,
  addCustomRules,
  deleteCustomRuleBatch
} from '@/api/control/website'
import {
  getSetting,
  setSetting
} from '@/api/system/setting'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

const activeTab = ref('function')
const websiteTypes = ref([])
const customRules = ref([])
const blockingEnabled = ref(false)
const multipleSelection = ref([])
const showImport = ref(false)
const importText = ref('')

onMounted(() => {
  loadAll()
})

const goBack = () => {
  router.push('/control')
}

const loadAll = async () => {
  await loadSetting()
  await loadTypes()
  await loadCustomRules()
}

const loadSetting = async () => {
  const res = await getSetting('website_blocking_enabled')
  blockingEnabled.value = res?.data === '1'
}

const loadTypes = async () => {
  const res = await getWebsiteType()
  if (res.code === 200) {
    websiteTypes.value = res.data.map(type => ({
      ...type,
      icon: type.icon || 'CircleCheck' 
    }))
  }
}

const loadCustomRules = async () => {
  const res = await getCustomRules()
  if (res.code === 200) customRules.value = res.data
}

const onToggleBlocking = async (value) => {
  await setSetting('website_blocking_enabled', value ? '1' : '0')
  ElMessage.success('设置已更新')
}

const toggleTypeStatus = async (type) => {
  const res = await updateWebsiteTypeStatus(type.type_id, type.status)
  if (res.code !== 200) ElMessage.error(res.message || '状态更新失败')
}

const toggleCustomRule = async (row) => {
  const res = await updateCustomRuleStatus(row.id, row.status)
  if (res.code !== 200) ElMessage.error(res.message || '状态更新失败')
}

const handleDeleteCustom = async (id) => {
  await ElMessageBox.confirm('确定删除该规则？', '提示')
  await deleteCustomRule(id)
  await loadCustomRules()
}

const handleSelectionChange = (val) => {
  multipleSelection.value = val.map(item => item.id)
}

const batchDeleteCustom = async () => {
  await ElMessageBox.confirm('确定删除所选规则？', '警告')
  await deleteCustomRuleBatch(multipleSelection.value)
  await loadCustomRules()
  multipleSelection.value = []
}

const submitImport = async () => {
  if (!importText.value.trim()) {
    return ElMessage.warning('请输入网址')
  }
  const res = await addCustomRules({ website_url: importText.value, status: 0 })
  if (res.code === 200) {
    ElMessage.success('导入成功')
    showImport.value = false
    importText.value = ''
    await loadCustomRules()
  } else {
    ElMessage.error(res.message || '导入失败')
  }
}
</script>

<style scoped>
.back-icon {
  width: 20px;
  height: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.back-icon:hover {
  transform: scale(1.1);
  opacity: 0.8;
}
</style>