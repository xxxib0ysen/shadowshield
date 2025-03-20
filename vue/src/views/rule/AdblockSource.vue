<template>
  <el-container class="adblock-container">
    <el-main>

      <el-card shadow="never" class="card-spacing">
        <el-tabs v-model="activeTab" @tab-click="handleTabClick">
          <el-tab-pane label="广告拦截规则源" name="adblock"></el-tab-pane>
          <el-tab-pane label="网站控制规则" name="website"></el-tab-pane>
        </el-tabs>
      </el-card>

      <el-card shadow="never" class="operate-container">
        <el-icon size="small"><Tickets /></el-icon>
          <span> 数据列表</span>
        <el-button size="mini" circle @click="fetchRules" style="float:right">
          <el-icon><RefreshRight /></el-icon>
        </el-button>
        <el-button  size="mini"  @click="openImportDialog" style="float:right;margin-right: 15px">导入</el-button>

    </el-card>


      <el-table 
        :data="ruleList" 
        border 
        stripe 
        v-loading="loading" 
        :height="tableHeight"
        class="table-spacing"
      >
        <el-table-column prop="source_id" label="规则源ID" width="100"></el-table-column>
        <el-table-column prop="source_name" label="规则名称" ></el-table-column>
        <el-table-column prop="source_url" label="规则URL" ></el-table-column>
        <el-table-column prop="createdon" label="创建时间" ></el-table-column>
        <el-table-column prop="last_modified" label="最后更新时间" ></el-table-column>

        <el-table-column label="是否启用" width="120">
          <template #default="{ row }">
            <el-switch v-model="row.status" @change="toggleStatus(row)" />
          </template>
        </el-table-column>

        <el-table-column label="操作" >
          <template #default="{ row }">
            <el-button type="text" size="mini"  @click="deleteSource(row.source_id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-row justify="end" class="pagination-spacing">
        <el-pagination
          v-model:current-page="pagination.page"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          layout="total, prev, pager, next, jumper"
          @current-change="fetchRules"
        />
      </el-row>
    </el-main>

    <el-dialog title="广告拦截规则源 - 导入" v-model="importDialogVisible" width="500px" @closed="resetAlert">
      <!-- 提示框 -->
      <el-alert 
        v-if="alertVisible"
        type="info" 
        show-icon 
        class="mb-3 alert-spacing"
        :closable="true"
        @close="alertVisible = false"
      >
        <template #title>
          <span style="font-size: 13px;">输入格式：规则名称 | 规则URL</span>
        </template>
      </el-alert>

      <!-- 错误提示 -->
      <el-alert v-if="errorMessage" type="error" show-icon class="mb-3">
        <template #title>{{ errorMessage }}</template>
      </el-alert>

      <el-form>
        <el-form-item label="规则数据" class="input-spacing">
          <el-input 
            type="textarea" 
            v-model="importRules" 
            :rows="5" 
            placeholder="多个规则源以换行符进行区分(必填)"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="importDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="importRulesHandler">保存</el-button>
      </template>
    </el-dialog>

  </el-container>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount , watch} from "vue";
import { getAdblockList, addAdblockSource, deleteAdblockSource, updateAdblockStatus } from "@/api/rule/adblocksource";
import { ElMessage, ElMessageBox } from "element-plus";
import {useRoute, useRouter} from "vue-router";


const activeTab = ref("adblock");
const ruleList = ref([]);
const loading = ref(false);
const importDialogVisible = ref(false);
const importRules = ref("");
const alertVisible = ref(true);
const errorMessage = ref(""); // 存储后端返回的错误信息
const route = useRoute();
const router = useRouter();

// 点击选项卡
watch(() => route.path, (newPath) => {
  activeTab.value = newPath.includes("website") ? "website" : "adblock";
});
const handleTabClick = (tab) => {
  router.push(tab.paneName === "website" ? "/setting/rule/website_control" : "/setting/rule/adblock");
};

// 分页
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0,
});

// 表格高度自适应
const tableHeight = ref("500px");

// 动态计算表格高度
const updateTableHeight = () => {
  tableHeight.value = `${window.innerHeight - 320}px`;
};

// 监听窗口变化
onMounted(() => {
  updateTableHeight();
  window.addEventListener("resize", updateTableHeight);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", updateTableHeight);
});

// 获取列表
const fetchRules = async (page = 1) => {
  loading.value = true;
  pagination.page = page;
  try {
    const res = await getAdblockList({ page: pagination.page, page_size: pagination.pageSize });
    if (res.code === 200) {
      ruleList.value = res.data.data.map(rule => ({
        ...rule,
        status: rule.status === 1?true:false
      }));
      pagination.total = res.data.total;
    } else {
      ElMessage.error(res.message || "获取数据失败");
    }
  } finally {
    loading.value = false;
  }
};

// 打开导入弹窗
const openImportDialog = () => {
  importDialogVisible.value = true;
  alertVisible.value = true;
  importRules.value = ""; // 清空输入框
  errorMessage.value = ""; // 清空错误信息
};

// 关闭弹窗重置alert
const resetAlert = () => {
  alertVisible.value = true;
};

// 提交导入规则
const importRulesHandler = async () => {
  if (!importRules.value.trim()) {
    errorMessage.value = "请输入规则数据";
    return;
  }

  try {
    const res = await addAdblockSource({ rules: importRules.value });
    if (res.code === 200) {
      ElMessage.success("导入成功");
      importDialogVisible.value = false;
      fetchRules();
    } else {
      errorMessage.value = res.message || "导入失败";
    }
  } catch (error) {
    errorMessage.value = "导入失败，请检查网络或稍后重试";
  }
};

// 删
const deleteSource = async (source_id) => {
  ElMessageBox.confirm("确定要删除该规则源吗？", "提示", { type: "warning" })
    .then(async () => {
      try {
        const res = await deleteAdblockSource({ source_id });
        if (res.code === 200) {
          ElMessage.success("删除成功");
          fetchRules();
        } else {
          ElMessage.error(res.message || "删除失败");
        }
      } catch (error) {
        ElMessage.error("删除失败");
      }
    });
};

// 启用/禁用
const toggleStatus = async (row) => {
  try {
    const res = await updateAdblockStatus({ source_id: row.source_id, status: row.status ? 1 : 0 });
    if (res.code === 200) {
      ElMessage.success("状态更新成功");
      fetchRules();
    } else {
      ElMessage.error(res.message || "状态更新失败");
      row.status =! row.status;
    }
  } catch (error) {
    ElMessage.error("状态更新失败");
    row.status =! row.status;
  }
};

onMounted(fetchRules);
</script>

<style scoped>
.operate-container {
  margin-bottom: 15px;
  padding: 15px;
}

.card-spacing {
  margin-bottom: 16px;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px; /* 按钮之间留一点间距 */
}

.table-spacing {
  margin-top: 16px;
}

.alert-spacing {
  margin-bottom: 12px; 
}

.input-spacing {
  margin-top: 10px; 
}

.pagination-spacing {
  margin-top: 16px;
  padding-bottom: 16px;
}
</style>