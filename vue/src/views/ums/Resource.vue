<template>
    <div class="resource-list">
      <el-card class="filter-container" shadow="never">
        <div>
          <el-icon size="small"><Search /></el-icon>
          <span> 筛选搜索</span>
          <el-button style="float:right" size="mini" @click="resetSearch">重置</el-button>
        </div>
        <div style="margin-top: 15px">
          <el-form :inline="true" label-width="100px">
            <el-form-item label="资源名称：" style="width: 280px">
              <el-input v-model="searchQuery.name" placeholder="请输入资源名称" clearable>
                <template #suffix>
                  <el-icon @click="fetchResources" style="cursor: pointer"><Search /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item label="资源路径：" style="width: 280px">
              <el-input v-model="searchQuery.uri" placeholder="请输入资源路径" clearable>
                <template #suffix>
                  <el-icon @click="fetchResources" style="cursor: pointer"><Search /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item label="资源分类：" style="width: 260px">
              <el-select v-model="searchQuery.category_id" placeholder="全部" clearable @change="fetchResources">
                <el-option v-for="category in resourceCategories" :key="category.category_id" :label="category.category_name" :value="category.category_id"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <el-card class="operate-container">
        <el-icon size="small"><Tickets /></el-icon>
        <span> 数据列表</span>
        <el-button size="mini" class="btn-add" type="primary" @click="openCategoryDialog" style="float:right">资源分类</el-button>
        <el-button size="mini" class="btn-add" @click="openAddResourceDialog" style="float:right; margin-right: 10px">添加</el-button>
      </el-card>
  
      <el-table :data="resourceList" stripe border v-loading="loading" style="width: 100%;">
        <el-table-column prop="resource_id" label="资源ID" width="100" align="center"/>
        <el-table-column prop="name" label="资源名称" width="160" align="center"/>
        <el-table-column prop="category_name" label="资源分类" width="160" align="center"/>
        <el-table-column prop="uri" label="资源路径" width="160" align="center"/>
        <el-table-column prop="description" label="描述" width="200" align="center"/>
        <el-table-column prop="createdon" label="创建时间" width="160" align="center"/>
        <el-table-column label="操作" width="200" align="center">
          <template #default="{ row }">
            <el-button size="mini" type="text" @click="openEditResourceDialog(row)">编辑</el-button>
            <el-button size="mini" type="text" @click="confirmDeleteResource(row.resource_id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
  
      <div class="pagination-container">
        <el-pagination 
          v-model:current-page="pagination.page" 
          v-model:page-size="pagination.pageSize"
          :total="pagination.total" 
          background
          layout="total, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="fetchResources"
        />
      </div>
  
      <el-dialog v-model="resourceDialog.visible" :title="resourceDialog.isEdit ? '编辑资源' : '添加资源'"
                 @close="resetResourceDialog" width="40%">
        <el-form ref="resourceFormRef" :model="resourceDialog.form" label-width="120px">
          <el-form-item label="资源名称：" prop="name">
            <el-input v-model="resourceDialog.form.name" style="width: 250px"/>
          </el-form-item>
          <el-form-item label="资源路径：" prop="uri">
            <el-input v-model="resourceDialog.form.uri" style="width: 250px"/>
          </el-form-item>
          <el-form-item label="资源分类：" prop="category_id">
            <el-select v-model="resourceDialog.form.category_id" placeholder="请选择分类" style="width: 250px">
              <el-option v-for="category in resourceCategories" :key="category.category_id" :label="category.category_name" :value="category.category_id"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="描述：" prop="description">
            <el-input v-model="resourceDialog.form.description" type="textarea" :rows="3" style="width: 250px"/>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="resourceDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="saveResource">提交</el-button>
        </template>
      </el-dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { getResourceList, addResource, updateResource, deleteResource, getResourceCategories } from '@/api/ums/resource'
  
  const searchQuery = reactive({ name: '', uri: '', category_id: null })
  const resourceList = ref([])
  const resourceCategories = ref([])
  const loading = ref(false)
  const pagination = reactive({ page: 1, pageSize: 10, total: 0 })
  
  const resourceDialog = reactive({
    visible: false,
    isEdit: false,
    form: { resource_id: '', name: '', uri: '', category_id: null, description: '' }
  })
  
  // 获取资源列表
  const fetchResources = async () => {
    loading.value = true
    const res = await getResourceList(searchQuery.category_id, searchQuery.name, searchQuery.uri, pagination.page, pagination.pageSize)
    resourceList.value = res.data.resources || []
    pagination.page = res.data.page || 1;         
    pagination.pageSize = res.data.pageSize || 6;
    pagination.total = res.data.total || 0;  
    loading.value = false
  }
  
  // 获取资源分类
  const fetchResourceCategories = async () => {
    const res = await getResourceCategories()
    resourceCategories.value = res.data || []
  }
  
  // 添加资源
  const openAddResourceDialog = () => {
    resourceDialog.form = { resource_id: '', name: '', uri: '', category_id: null, description: '' }
    resourceDialog.isEdit = false
    resourceDialog.visible = true
  }
  
  // 编辑资源
  const openEditResourceDialog = (resource) => {
    resourceDialog.form = { ...resource }
    resourceDialog.isEdit = true
    resourceDialog.visible = true
  }
  
  // 保存
  const saveResource = async () => {
    if (resourceDialog.isEdit) {
      await updateResource(resourceDialog.form.resource_id, resourceDialog.form)
      ElMessage.success('资源更新成功')
    } else {
      await addResource(resourceDialog.form)
      ElMessage.success('资源添加成功')
    }
    resourceDialog.visible = false
    fetchResources()
  }
  
  // 删除资源
  const confirmDeleteResource = async (resource_id) => {
    await ElMessageBox.confirm('确定删除该资源吗？', '警告', { type: 'warning' })
    await deleteResource(resource_id)
    ElMessage.success('资源删除成功')
    fetchResources()
  }

  // 重置搜索
const resetSearch = () => {
  searchQuery.name = ''
  searchQuery.uri = ''
  searchQuery.category_id = null
  fetchResources() // 重新获取数据
}
  
  onMounted(() => {
    fetchResources()
    fetchResourceCategories()
  })
  </script>

<style>
.filter-container, .operate-container {
margin-bottom: 15px;
padding: 15px;
}
</style>
