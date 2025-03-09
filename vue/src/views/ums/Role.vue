<template>
    <div class="role-list">
      <el-card class="filter-container">
        <div>
        <el-icon size="small"><Search /></el-icon>
        <span> 筛选搜索</span>
          <el-button style="float:right" type="primary" size="mini" @click="fetchRoles">查询</el-button>
          <el-button style="float:right;margin-right: 15px" size="mini" @click="resetSearch">重置</el-button>
        </div>
        <div style="margin-top: 15px">
            <el-form :inline="true" :model="searchQuery"  label-width="140px">
            <el-form-item label="输入搜索：">
            <el-input v-model="searchQuery.keyword" class="input-width" placeholder="角色名称" clearable></el-input>
            </el-form-item>
        </el-form>
        </div>
        
      </el-card>
  
      <el-card class="operate-container">
        <el-icon size="small"><Tickets /></el-icon>
        <span> 数据列表</span>
        <el-button size="mini" class="btn-add" @click="openAddRoleDialog" style="float:right">添加</el-button>
      </el-card>
  
      <el-table :data="roleList" stripe border v-loading="loading" style="width: 100%;">
        <el-table-column prop="role_id" label="角色ID" width="100" align="center"/>
        <el-table-column prop="role_name" label="角色名称" width="160" align="center"/>
        <el-table-column prop="description" label="角色描述" width="200" align="center"/>
        <el-table-column prop="count" label="用户数" width="100" align="center"/>
        <el-table-column prop="createdon" label="创建时间" width="160" align="center"/>
        <el-table-column label="是否启用" width="140" align="center">
          <template #default="{ row }">
            <el-switch :model-value="row.status" :active-value="1" :inactive-value="0" @change="confirmStatusChange(row)"/>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="260" align="center">
          <template #default="{ row }">

            <el-row>
                <el-button size="mini"  type="text" @click="openAssignMenuDialog(row)">分配菜单</el-button>
                <el-button size="mini"  type="text" @click="openAssignResourceDialog(row)">分配资源</el-button>
            </el-row>
            <el-row>
                <el-button size="mini"  type="text" @click="openAssignPermissionDialog(row)">分配权限</el-button>
                <el-button size="mini"  type="text" @click="openEditRoleDialog(row)">编辑</el-button>
                <el-button size="mini"  type="text" @click="confirmDeleteRole(row.role_id)">删除</el-button>
            </el-row>

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
          @current-change="fetchRoles"
        />
      </div>
  
      <el-dialog v-model="roleDialog.visible" :title="roleDialog.isEdit ? '编辑角色' : '添加角色'"
                 @close="resetRoleDialog" width="40%">
        <el-form ref="roleFormRef" :model="roleDialog.form" label-width="150px" >
          <el-form-item label="角色名称: " prop="role_name" >
            <el-input v-model="roleDialog.form.role_name" style="width: 250px" />
          </el-form-item>
          <el-form-item label="角色描述:" prop="description">
            <el-input v-model="roleDialog.form.description"  type="textarea" :rows="5" style="width: 250px"/>
          </el-form-item>
          <el-form-item label="是否启用">
            <el-radio-group v-model="roleDialog.form.status">
              <el-radio :label="1">是</el-radio>
              <el-radio :label="0">否</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="roleDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="saveRole">确定</el-button>
        </template>
      </el-dialog>
    </div>
  </template>
  
<script setup>
import { ref, reactive, onMounted } from 'vue'
import {
Search, Tickets
} from '@element-plus/icons-vue';
import {  ElMessage, ElMessageBox } from 'element-plus'
import { getRoleList, addRole, updateRole, deleteRole, updateRoleStatus } from '@/api/ums/role'

const searchQuery = reactive({ keyword: '' })
const roleList = ref([])
const loading = ref(false)
const pagination = reactive({ page: null, pageSize: null, total: 0 })

// 角色弹窗
const roleDialog = reactive({
visible: false,
isEdit: false,
form: { role_id: '', role_name: '', description: '', status: 1 }
})


// 获取角色
const fetchRoles = async () => {
loading.value = true;
try {
    const res = await getRoleList(searchQuery.keyword, pagination.page, pagination.pageSize);
    roleList.value = res.data.roles || [];
    pagination.page = res.data.page || 1;         
    pagination.pageSize = res.data.pageSize || 6;
    pagination.total = res.data.total || 0;  
} finally {
    loading.value = false;
}
}

//  重置搜索
const resetSearch = () => {
searchQuery.keyword = '';
fetchRoles();
}

// 添加
const openAddRoleDialog = () =>{
    roleDialog.form = {
        role_id: '',
        role_name: '',
        description: '',
        status: 1
    };
    roleDialog.isEdit = false;
    roleDialog.visible = true;
}
// 编辑角色
const openEditRoleDialog = (role) => {
  roleDialog.form = { ...role };
  roleDialog.isEdit = true;
  roleDialog.visible = true;
}

// 确认删除角色
const confirmDeleteRole = async (role_id) => {
  await ElMessageBox.confirm('确定删除该角色吗？', '警告', { type: 'warning' });
  await deleteRole(role_id);
  ElMessage.success('角色删除成功');
  fetchRoles();
}

// 确认启用/禁用角色
const confirmStatusChange = async (role) => {
  const oldStatus = role.status;
  const newStatus = oldStatus === 1 ? 0 : 1;
  try{
    await ElMessageBox.confirm(`确定要${newStatus ? '启用' : '禁用'}该角色吗？`, '确认', { type: 'warning' });
    await updateRoleStatus(role.role_id, newStatus);
    role.status = newStatus;
    ElMessage.success(`角色已${newStatus ? '启用' : '禁用'}`);
    fetchRoles(); 
  } catch {
      role.status = oldStatus; 
    };
}

// 保存
const saveRole = async () => {
  await ElMessageBox.confirm('确定要保存吗？', '确认', { type: 'warning' });
  if (roleDialog.isEdit) {
    await updateRole(roleDialog.form.role_id, roleDialog.form);
    ElMessage.success('角色更新成功');
  } else {
    await addRole(roleDialog.form);
    ElMessage.success('角色添加成功');
  }
  roleDialog.visible = false;
  fetchRoles();
}

onMounted(fetchRoles)
</script>

<style scoped>
.filter-container, .operate-container { margin-bottom: 15px; padding: 15px; }
.input-width { width: 250px; }
.pagination-container { display: flex; justify-content: flex-end; padding: 10px 20px; }
</style>
