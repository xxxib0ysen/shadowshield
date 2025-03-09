<template>
    <div class="permission-list">
      <el-card class="filter-container" shadow="never">
        <div>
          <el-icon size="small"><Search /></el-icon>
          <span> 筛选搜索</span>
          <el-button style="float:right" size="mini" @click="resetSearch">重置</el-button>
        </div>
        <div style="margin-top: 15px">
          <el-form :inline="true" label-width="100px">
            <el-form-item label="输入搜索：" style="width: 280px">
              <el-input v-model="searchQuery.keyword" placeholder="权限名称" clearable>
                <template #suffix>
                  <el-icon @click="fetchPermissions" style="cursor: pointer"><Search /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-form>
        </div>
      </el-card>

      <el-card class="operate-container">
        <el-icon size="small"><Tickets /></el-icon>
        <span> 数据列表</span>
        <el-button size="mini" class="btn-add" @click="openAddPermissionDialog" style="float:right">添加</el-button>
      </el-card>
  
      <el-table :data="permissionList" stripe border v-loading="loading" style="width: 100%;">
        <el-table-column prop="permission_id" label="权限ID" width="100" align="center"/>
        <el-table-column prop="parent_id" label="父级权限ID" width="120" align="center"/>
        <el-table-column prop="name" label="权限名称" width="160" align="center"/>
        <el-table-column prop="value" label="权限值" width="160" align="center"/>
        <el-table-column prop="type" label="权限类型" width="120" align="center"/>
        <el-table-column prop="route" label="前端资源路径" width="160" align="center"/>
        <el-table-column label="是否启用" width="120" align="center">
          <template #default="{ row }">
            <el-switch v-model="row.status" :active-value="1" :inactive-value="0" @change="confirmStatusChange(row)"/>
          </template>
        </el-table-column>
        <el-table-column prop="createdon" label="权限创建时间" width="160" align="center"/>
        <el-table-column label="操作" width="160" align="center">
          <template #default="{ row }">
            <el-button size="mini" type="text" @click="openEditPermissionDialog(row)">编辑</el-button>
            <el-button size="mini" type="text" @click="confirmDeletePermission(row.permission_id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination 
          v-model:current-page="pagination.page" 
          v-model:page-size="pagination.page_size"
          :total="pagination.total" 
          background
          layout="total, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="fetchPermissions"
        />
      </div>

      <el-dialog v-model="permissionDialog.visible" :title="permissionDialog.isEdit ? '编辑权限' : '添加权限'"
                 @close="resetPermissionDialog" width="40%">
        <el-form ref="permissionFormRef" :model="permissionDialog.form" label-width="120px">
          <el-form-item label="权限名称：" prop="name">
            <el-input v-model="permissionDialog.form.name" style="width: 250px"/>
          </el-form-item>
          <el-form-item label="权限值：" prop="value">
            <el-input v-model="permissionDialog.form.value" style="width: 250px"/>
          </el-form-item>
          <el-form-item label="权限类型：" prop="type">
            <el-select v-model="permissionDialog.form.type" style="width: 250px">
              <el-option label="菜单" value="menu"></el-option>
              <el-option label="按钮" value="button"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="前端资源路径：" prop="route">
            <el-input v-model="permissionDialog.form.route" style="width: 250px"/>
          </el-form-item>
          <el-form-item label="是否启用">
            <el-radio-group v-model="permissionDialog.form.status">
              <el-radio :label="1">是</el-radio>
              <el-radio :label="0">否</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="permissionDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="savePermission">提交</el-button>
        </template>
      </el-dialog>
    </div>
  </template>
  
<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getPermissionList, addPermission, updatePermission, deletePermission } from '@/api/ums/permission'

// 权限查询
const searchQuery = reactive({ keyword: '' })
const permissionList = ref([])
const loading = ref(false)
const pagination = reactive({ page: null, pageSize: null, total: 0  })

const permissionDialog = reactive({
visible: false,
isEdit: false,
form: { permission_id: '', name: '', value: '', type: '', route: '', icon: '', status: 1 }
})

// 获取权限列表
const fetchPermissions = async () => {
loading.value = true
const res = await getPermissionList(searchQuery.keyword, pagination.page, pagination.page_size)
permissionList.value = res.data.permissions || []
pagination.page = res.data.page || 1;         
pagination.pageSize = res.data.pageSize || 6;
pagination.total = res.data.total || 0;  
loading.value = false
}

// 重置搜索
const resetSearch = () => {
searchQuery.keyword = ''
fetchPermissions()
}

// 删除权限
const confirmDeletePermission = async (permission_id) => {
await ElMessageBox.confirm('确定删除该权限吗？', '警告', { type: 'warning' })
await deletePermission(permission_id)
ElMessage.success('权限删除成功')
fetchPermissions()
}

// 添加
const openAddPermissionDialog = () => {
permissionDialog.form = { permission_id: '', name: '', value: '', type: '', route: '', icon: '', status: 1 }
permissionDialog.isEdit = false
permissionDialog.visible = true
}

// 编辑
const openEditPermissionDialog = (permission) => {
permissionDialog.form = { ...permission }
permissionDialog.isEdit = true
permissionDialog.visible = true
}

// 保存
const savePermission = async () => {
await ElMessageBox.confirm('确定要提交吗？', '确认', { type: 'warning' })
if (permissionDialog.isEdit) {
    await updatePermission(permissionDialog.form.permission_id, permissionDialog.form)
    ElMessage.success('权限更新成功')
} else {
    await addPermission(permissionDialog.form)
    ElMessage.success('权限添加成功')
}
permissionDialog.visible = false
fetchPermissions()
}

onMounted(fetchPermissions)
</script>

<style scoped>
.filter-container, .operate-container { margin-bottom: 15px; padding: 15px; }
.pagination-container { display: flex; justify-content: flex-end; padding: 10px 20px; }
</style>
  