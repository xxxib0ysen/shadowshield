<template>
  <div class="user-list">
    <el-card class="filter-container">
      <div>
        <el-icon size="small"><Search /></el-icon>
        <span> 筛选搜索</span>
        <el-button style="float:right" type="primary" size="mini" @click="fetchUsers">查询搜索</el-button>
        <el-button style="float:right;margin-right: 15px" size="mini" @click="resetSearch">重置</el-button>
      </div>
      <div style="margin-top: 15px">
        <el-form :inline="true" :model="searchQuery"  label-width="140px">
          <el-form-item label="输入搜索：">
            <el-input v-model="searchQuery.keyword" class="input-width" placeholder="账号/姓名" clearable></el-input>
          </el-form-item>
        </el-form>
      </div>
    </el-card>

    <el-card class="operate-container">
      <el-icon size="small"><Tickets /></el-icon>
      <span> 数据列表</span>
      <el-button size="mini" class="btn-add" @click="openAddUserDialog" style="float:right">添加</el-button>
    </el-card>
    <el-table :data="userList" stripe border class="user-table" v-loading="loading">
      <el-table-column prop="user_id" label="用户ID" width="100" align="center"/>
      <el-table-column prop="username" label="账号" width="100" align="center"/>
      <el-table-column prop="fullname" label="姓名" width="160" align="center"/>
      <el-table-column prop="createdon" label="创建时间" width="160" align="center"/>
      <el-table-column prop="lastlogin" label="最后登录" width="160" align="center"/>
      <el-table-column label="是否启用" width="140" align="center">
        <template #default="{ row }">
          <el-switch v-model="row.status" :active-value="1" :inactive-value="0" @change="confirmStatusChange(row)"/>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" align="center">
        <template #default="{ row }">
          <el-button size="mini" type="text" @click="openAssignRoleDialog(row)">分配角色</el-button>
          <el-button size="mini" type="text"  @click="openEditUserDialog(row)">编辑</el-button>
          <el-button size="mini" type="text"  @click="confirmDeleteUser(row.user_id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination 
      v-model:current-page="pagination.page" 
      v-model:page-size="pagination.pageSize"
      :total="pagination.total" 
      background
      layout="total, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="fetchUsers"/>
    </div>
    

    <!-- 添加/编辑用户 -->
    <el-dialog v-model="userDialog.visible" :title="userDialog.isEdit ? '编辑用户' : '添加用户'"
               @close="resetUserDialog">
      <el-form ref="userFormRef" :model="userDialog.form" :rules="userRules" label-width="80px">
        <el-form-item label="账号" prop="username">
          <el-input v-model="userDialog.form.username"/>
        </el-form-item>
        <el-form-item label="姓名" prop="fullname">
          <el-input v-model="userDialog.form.fullname"/>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="userDialog.form.password" type="password" placeholder="不修改请留空"/>
        </el-form-item>
        <el-form-item label="是否启用">
          <el-radio-group v-model="userDialog.form.status">
            <el-radio :label="1">是</el-radio>
            <el-radio :label="0">否</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="userDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="saveUser">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup >
import {
  Search, Tickets
} from '@element-plus/icons-vue';
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUserList, addUser, updateUser, deleteUser, updateUserStatus } from '@/api/ums/user'

const searchQuery = reactive({ keyword: '' })
const userList = ref([])
const loading = ref(false)
const pagination = reactive({ page: null, pageSize: null, total: 0 })

// 用户弹窗
const userDialog = reactive({
  visible: false,
  isEdit: false,
  form: { user_id: '', username: '', fullname: '', password: '', status: 1 }
})

const handleSizeChange = (newSize) => {
  pagination.pageSize = newSize;
  pagination.page = 1;
  fetchUsers();
}

// 获取用户列表
const fetchUsers = async () => {
  loading.value = true;
  try {
    const res = await getUserList(searchQuery.keyword, pagination.page, pagination.pageSize);

    console.log("后端返回的数据:", res.data); 

    userList.value = res.data.users || []; 

    pagination.page = res.data.page || 1;         
    pagination.pageSize = res.data.pageSize || 6;
    pagination.total = res.data.total || 0;  

  } catch (error) {
    console.error("获取用户列表失败:", error);
  } finally {
    loading.value = false;
  }
};


// 重置搜索
const resetSearch = () => {
  searchQuery.keyword = ''
  fetchUsers()
}

// 添加用户
const openAddUserDialog = () => {
  resetUserDialog()
  userDialog.isEdit = false
  userDialog.visible = true
}

// 编辑用户
const openEditUserDialog = (user) => {
  userDialog.form = { ...user, password: '' } 
  userDialog.isEdit = true
  userDialog.visible = true
}

// 保存用户
const saveUser = async () => {
  await ElMessageBox.confirm('确定要保存吗？', '确认', { type: 'warning' })
  if (userDialog.isEdit) {
    await updateUser(userDialog.form.user_id, userDialog.form)
    ElMessage.success('用户更新成功')
  } else {
    await addUser(userDialog.form)
    ElMessage.success('用户添加成功')
  }
  userDialog.visible = false
  fetchUsers()
}

// 确认删除
const confirmDeleteUser = async (user_id) => {
  await ElMessageBox.confirm('确定删除此用户吗？', '警告', { type: 'warning' })
  await deleteUser(user_id)
  ElMessage.success('用户删除成功')
  fetchUsers()
}

// 确认修改状态
const confirmStatusChange = async (user) => {
  await ElMessageBox.confirm('确定修改用户状态吗？', '确认', { type: 'warning' })
  await updateUserStatus(user.user_id, user.status)
  ElMessage.success('用户状态更新成功')
}

const resetUserDialog = () => {
  userDialog.form = { user_id: '', username: '', fullname: '', password: '', status: 1 }
}

onMounted(fetchUsers)
</script>

<style scoped>
.filter-container, .operate-container {
  margin-bottom: 15px;
  padding: 15px;
}
.input-width { width: 250px; }
.user-table { margin-bottom: 20px; }
.pagination-container {
  display: flex;
  justify-content: flex-end;  
  padding: 10px 20px;
}

</style>
