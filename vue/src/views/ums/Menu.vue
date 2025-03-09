<template>
    <div class="menu-list">
  
      <el-card class="operate-container">
        <el-icon size="small"><Tickets /></el-icon>
        <span> 数据列表</span>
        <el-button size="mini" class="btn-add" @click="openAddMenuDialog" style="float:right">添加</el-button>
      </el-card>
  
      <el-table :data="menuList" stripe border v-loading="loading" style="width: 100%;">
        <el-table-column prop="menu_id" label="菜单ID" width="100" align="center"/>
        <el-table-column prop="title" label="菜单名称" width="160" align="center"/>
        <el-table-column prop="level" label="菜单级数" width="160" align="center">
          <template #default="{ row }">
            <span v-if="row.level === 1">一级</span>
            <span v-else-if="row.level === 2">二级</span>
            <span v-else-if="row.level === 3">三级</span>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="前端名称" width="160" align="center"/>
        <el-table-column prop="icon" label="前端图标" width="160" align="center">
            <template #default="{ row }">
                <el-icon v-if="row.icon">
                <component :is="icons[row.icon]" />
                </el-icon>
            </template>
        </el-table-column>
        <el-table-column label="是否启用" width="140" align="center">
          <template #default="{ row }">
            <el-switch :model-value="row.hidden" :active-value="0" :inactive-value="1" @change="confirmStatusChange(row)"/>
          </template>
        </el-table-column>
        <el-table-column prop="createdon" label="创建时间" width="160" align="center"/>
        <el-table-column label="操作" width="260" align="center">
          <template #default="{ row }">
            <el-button size="mini" type="text" @click="openHierarchyDialog(row)">查看上下级</el-button>
            <el-button size="mini" type="text" @click="openEditMenuDialog(row)">编辑</el-button>
            <el-button size="mini" type="text" @click="confirmDeleteMenu(row.menu_id)">删除</el-button>
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
          @current-change="fetchMenus"
        />
      </div>
  
      <el-dialog v-model="menuDialog.visible" :title="menuDialog.isEdit ? '修改菜单' : '添加菜单'"
                 @close="resetMenuDialog" width="40%">
        <el-form ref="menuFormRef" :model="menuDialog.form" label-width="150px">
          <el-form-item label="菜单名称" prop="title">
            <el-input v-model="menuDialog.form.title" style="width: 250px"/>
          </el-form-item>
          <el-form-item label="上级菜单">
            <el-cascader
              v-model="menuDialog.form.menu_pid"
              :options="menuTree"
              :props="{ 
                value: 'menu_id', 
                label: 'title' ,
                children: 'children',
                expandTrigger: 'hover' 
                }"
              style="width: 250px"
              clearable
              @change="handleMenuSelect"
            />
          </el-form-item>
          <el-form-item label="前端名称" prop="name">
            <el-input v-model="menuDialog.form.name" style="width: 250px"/>
          </el-form-item>
          <el-form-item label="前端图标" prop="icon">
            <div style="display: flex; align-items: center;">
                <el-input v-model="menuDialog.form.icon" style="width: 250px" />
                <el-icon v-if="menuDialog.form.icon" style="margin-left: 10px; font-size:20px">
                    <component :is="menuDialog.form.icon" />
                </el-icon>
            </div>

          </el-form-item>
          <el-form-item label="是否显示">
            <el-radio-group v-model="menuDialog.form.hidden">
              <el-radio :label="0">是</el-radio>
              <el-radio :label="1">否</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="menuDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="saveMenu">提交</el-button>
        </template>
      </el-dialog>
    </div>
  </template>
  
<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMenuList, getMenuTree, addMenu, updateMenu, deleteMenu, updateMenuStatus } from '@/api/ums/menu'
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
const icons = ref(ElementPlusIconsVue);


const menuList = ref([])
const menuTree = ref([])
const loading = ref(false)
const pagination = reactive({ page: null, pageSize: null, total: 0 })
const menuHierarchy = ref([]);  // 存放层级菜单
const hierarchyDialog = ref(false);

const menuDialog = reactive({
visible: false,
isEdit: false,
form: { menu_id: '', title: '', menu_pid: null, name: '', icon: '', hidden: 0 }
})

const fetchMenus = async () => {
    loading.value = true
    const res = await getMenuList(pagination.page, pagination.page_size)
    menuList.value = res.data.menus || [];
    pagination.page = res.data.page || 1;         
    pagination.page_size = res.data.page_size || 6;
    pagination.total = res.data.total || 0;  
    loading.value = false
}

const fetchMenuTree = async () => {
    const res = await getMenuTree();
    menuTree.value = [
        { menu_id: null, title: "无上级菜单" }, //一级
        ...res.data
  ];
}

const handleMenuSelect = (value) => {
  // 选择 "无上级菜单" 时，将 menu_pid 设为 null
  menuDialog.form.menu_pid = value === null ? null : value;
};


const confirmDeleteMenu = async (menu_id) => {
    await ElMessageBox.confirm('确定删除该菜单吗？', '警告', { type: 'warning' })
    await deleteMenu(menu_id)
    ElMessage.success('菜单删除成功')
    fetchMenus()
}


const confirmStatusChange = async (menu) => {
    try{
        await ElMessageBox.confirm(`确定要${newStatus ? '启用' : '禁用'}该菜单吗？`, '确认', { type: 'warning' });
        await updateMenuStatus(menu.menu_id, newStatus);
        menu.status = newStatus;
        ElMessage.success(`菜单已${newStatus ? '启用' : '禁用'}`);
        fetchMenus(); 
  } catch {
        menu.status = oldStatus; 
    };
}

// 添加
const openAddMenuDialog = () => {
  menuDialog.form = { menu_id: '', title: '', menu_pid: null, name: '', icon: '', hidden: 0 }
  menuDialog.isEdit = false
  menuDialog.visible = true
}

// 编辑
const openEditMenuDialog = (menu) => {
  menuDialog.form = { ...menu }
  menuDialog.isEdit = true
  menuDialog.visible = true
}

// 保存
const saveMenu = async () => {
  await ElMessageBox.confirm('确定要提交吗？', '确认', { type: 'warning' })
  if (menuDialog.isEdit) {
    await updateMenu(menuDialog.form.menu_id, menuDialog.form)
    ElMessage.success('菜单更新成功')
  } else {
    await addMenu(menuDialog.form)
    ElMessage.success('菜单添加成功')
  }
  menuDialog.visible = false
  fetchMenus()
}

// 查看上下级
const openHierarchyDialog = async (menu) => {
  try {
    const res = await getMenuHierarchy(menu.menu_id);
    menuHierarchy.value = res.data;
    hierarchyDialog.value = true;  
  } catch (error) {
    ElMessage.error("获取上下级菜单失败");
  }
};


onMounted(() => {
fetchMenus()
fetchMenuTree()
})
</script>

<style scoped>
.operate-container { margin-bottom: 15px; padding: 15px; }
.pagination-container { display: flex; justify-content: flex-end; padding: 10px 20px; }
</style>
