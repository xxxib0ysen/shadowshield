<template>
  <div class="user-list">
    <el-card class="card-container">
      <div class="header">
        <el-input 
          v-model="searchKeyword" 
          placeholder="请输入账号/姓名" 
          prefix-icon="Search"
          clearable
          @clear="fetchUsers"
          @keyup.enter="fetchUsers"
          class="search-input"
        />
        <el-button type="primary" @click="fetchUsers">查询搜索</el-button>
        <el-button type="success" @click="openAddUserDialog">添加</el-button>
      </div>

      <el-table :data="userList" stripe border class="user-table">
        <el-table-column prop="user_id" label="用户ID" width="80"/>
        <el-table-column prop="username" label="账号" width="150"/>
        <el-table-column prop="fullname" label="姓名" width="150"/>
        <el-table-column prop="createdon" label="创建时间" width="180"/>
        <el-table-column prop="lastlogin" label="最后登录" width="180"/>
        <el-table-column prop="status" label="是否启用" width="120">
          <template #default="{ row }">
            <el-switch 
              v-model="row.status" 
              :active-value="1" 
              :inactive-value="0" 
              @change="updateStatus(row)"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="260">
          <template #default="{ row }">
            <el-link type="primary" @click="openAssignRoleDialog(row)">分配角色</el-link>
            <el-link type="warning" @click="openEditUserDialog(row)">编辑</el-link>
            <el-link type="danger" @click="handleDeleteUser(row.id)">删除</el-link>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination 
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :total="pagination.total"
        layout="total, prev, pager, next"
        @current-change="fetchUsers"
      />
    </el-card>

    <!-- 添加/编辑用户弹窗 -->
    <el-dialog v-model="userDialog.visible" :title="userDialog.isEdit ? '编辑用户' : '添加用户'">
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

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUserList, addUser, updateUser, deleteUser, updateUserStatus } from '@/api/ums/user'

const searchKeyword = ref('')
const userList = ref([])
const pagination = reactive({ page: 1, pageSize: 10, total: 0 })

const userDialog = reactive({
  visible: false,
  isEdit: false,
  form: { user_id: '', username: '', fullname: '', password: '', status: 1 }
})

const fetchUsers = async () => {
  const res = await getUserList(searchKeyword.value, pagination.page, pagination.pageSize)
  userList.value = res.data.users
  pagination.total = res.data.total
}

const handleDeleteUser = async (user_id) => {
  await ElMessageBox.confirm('确定删除此用户吗？', '警告', { type: 'warning' })
  await deleteUser(user_id)
  ElMessage.success('用户删除成功')
  fetchUsers()
}

const updateStatus = async (user) => {
  await ElMessageBox.confirm('确定修改用户状态吗？', '确认', { type: 'warning' })
  await updateUserStatus(user.user_id, user.status)
  ElMessage.success('用户状态更新成功')
}

onMounted(fetchUsers)
</script>

<style scoped>
.card-container { padding: 20px; }
.header { display: flex; gap: 10px; margin-bottom: 20px; }
.search-input { width: 250px; }
.user-table { margin-bottom: 20px; }
</style>
