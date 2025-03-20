<template>
    <el-container class="website-control-container">
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
          <el-button size="mini" circle @click="refresh" style="float:right" :loading="loading">
            <el-icon><RefreshRight /></el-icon>
          </el-button>
          <el-button size="mini" @click="openRuleDialog" style="float:right;margin-right: 15px">添加</el-button>
          <el-button type="primary" size="mini" @click="openTypeDialog" style="float:right;margin-right: 15px">网站类型</el-button>
        </el-card>
  
        <!-- 折叠面板 -->
        <el-collapse 
            v-model="activePanels" 
            accordion>
          <el-collapse-item 
            v-for="type in websiteTypes" 
            :key="type.type_id" 
            :name="type.type_id"
            >
            <template #title>
                <el-icon style="font-size: 18px; margin-right: 10px;"><CircleCheck /></el-icon>
                <span style="font-weight: bold; font-size: 14px;" >{{ type.type_name }}</span>
                &nbsp;&nbsp;&nbsp;&nbsp;
                <span style="font-size: 12px; color: gray;">更新于 {{ lastUpdated[type.type_id] }}</span>
            </template>
            <el-scrollbar max-height="300px" >
              <el-table :data="rules[type.type_id] || []" style="width: 100%">
                <el-table-column prop="website_url" label="网址" />
                <el-table-column label="状态">
                  <template #default="{ row }">
                    <el-switch 
                        v-model="row.status" 
                        @change="toggleStatus(row)" 
                        :active-value="1" 
                        :inactive-value="0" 
                    />
                  </template>
                </el-table-column>
                <el-table-column label="操作">
                  <template #default="{ row }">
                    <el-button type="text" size="mini" @click="deleteRule(row.website_id)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-scrollbar>
          </el-collapse-item>
        </el-collapse>
      </el-main>
  
      <!-- 添加网站弹窗 -->
      <el-dialog v-model="showRuleDialog" title="添加网站规则" width="500px">
        <el-form ref="ruleForm" :model="newRule" label-width="120px" class="centered-form">
          <el-form-item label="类型">
            <el-select v-model="newRule.type_id" placeholder="请选择类型" style="width: 75%;">
              <el-option 
                v-for="type in websiteTypes" 
                :key="type.type_id" 
                :label="type.type_name" 
                :value="type.type_id" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="网址">
            <el-input 
                v-model="newRule.website_url" 
                type="textarea" 
                clearable
                :rows="5"
                placeholder="多个网站以换行符进行区分，支持通配符“*”“>”(必填)" 
                style="width: 75%;"
            />
          </el-form-item>
          <el-form-item label="启用" >
            <el-radio-group v-model="newRule.status">
              <el-radio :label="1">是</el-radio>
              <el-radio :label="0">否</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
          <template #footer>
            <el-button @click="showRuleDialog = false">取消</el-button>
            <el-button type="primary" @click="submitRule">提交</el-button>
          </template>
      </el-dialog>
  
      <!-- 网站类型管理弹窗 -->
      <el-dialog v-model="showTypeDialog" title="网站类型管理" width="500px">
        <el-card shadow="never">
            <el-table :data="websiteTypes" style="width: 100%" size="mini">
            <el-table-column prop="type_name" label="类型名称" />
            <el-table-column label="操作">
                <template #default="{ row }">
                <el-button type="text" size="mini" @click="deleteType(row.type_id)">删除</el-button>
                </template>
            </el-table-column>
            </el-table>
            <el-form ref="typeForm" :model="newType" label-width="80px" style="margin-top: 15px;">
            <el-form-item label="新增类型">
                <el-input v-model="newType.type_name" placeholder="请输入类型名称" clearable style="width: 75%;"/>
                <el-button  @click="submitType" style="margin-left: 10px;">添加</el-button>
            </el-form-item>
            </el-form>
        </el-card>
      </el-dialog>
    </el-container>
</template>
  
<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import {
getWebsiteRule, deleteWebsiteRule, addWebsiteRule,
getWebsiteType, updateWebsiteStatus, addWebsiteType, deleteWebsiteType
} from "@/api/rule/website_control";


const activeTab = ref("website");
const activePanels = ref([]);
const websiteTypes = ref([]);
const rules = ref({});
const showRuleDialog = ref(false);
const showTypeDialog = ref(false);
const newRule = ref({ website_url: "", type_id: null, status: 1 });
const newType = ref({ type_name: "" });

const route = useRoute();
const router = useRouter();
const lastUpdated = ref({});
const loading = ref(false)

// 选项卡切换
watch(() => route.path, (newPath) => {
activeTab.value = newPath.includes("website") ? "website" : "adblock";
});
const handleTabClick = (tab) => {
router.push(tab.paneName === "website" ? "/setting/rule/website_control" : "/setting/rule/adblock");
};

// 获取网站类型
const fetchTypes = async () => {
  if (loading.value) return;
  loading.value = true;
  try {
    const res = await getWebsiteType();
    if (res.code===200){
        websiteTypes.value = res.data;
        res.data.forEach(type => {
            lastUpdated.value[type.type_id] = type.last_modified;
        });
    } else {
        ElMessage.error(res.message || "获取网站类型失败");
    }
  } catch (error) {
    ElMessage.error("获取网站类型失败");
  } finally {
    loading.value = false;
  }
};

// 获取网站规则
const fetchRules = async () => {
  try {
    const res = await getWebsiteRule();
    if (res.code === 200) {
        rules.value = {};

        websiteTypes.value.forEach(type => {
            rules.value[type.type_id] = [];
        });

        res.data.forEach(rule => {
            const matchedType = websiteTypes.value.find(type => type.type_name === rule.type_name);
            if (matchedType) {
                rules.value[matchedType.type_id].push({
                    ...rule, 
                    type_id: matchedType.type_id // 手动补充 type_id，防止后续用到
                });
            } else {
                console.warn("未匹配到规则的 type_name:", rule.type_name);
            }
        });
    } else {
      ElMessage.error(res.message);
    }
  } catch (error) {
    ElMessage.error("获取网站规则失败");
  }
};

// 刷新
const refresh = async () => {
    await fetchTypes();
    await fetchRules();
};

// 删除网站类型
const deleteType = async (type_id) => {
    try {
        await ElMessageBox.confirm("确定要删除该网站类型吗？", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
        });
        const res = await deleteWebsiteType(type_id);
        if (res.code === 200) {
            ElMessage.success("网站类型删除成功");
            showTypeDialog.value = false;
            await refresh();
        } else {
            ElMessage.error(res.message || "删除失败");
        }
    } catch (error) {
        if (error !== "cancel") {
            ElMessage.error("请求失败，请检查网络或稍后重试");
            console.error("删除网站类型错误:", error);
        }
    }
};

// 删除网站规则
const deleteRule = async (website_id) => {
    try {
        await ElMessageBox.confirm("确定要删除该网站规则吗？", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
        });
        const res = await deleteWebsiteRule(website_id);
        if (res.code === 200) {
            ElMessage.success("网站规则删除成功");
            await refresh();
        } else {
            ElMessage.error(res.message || "删除失败");
        }
    } catch (error) {
        if (error !== "cancel") {
            ElMessage.error("请求失败，请检查网络或稍后重试");
            console.error("删除网站规则错误:", error);
        }
    }
};

// 启用/禁用规则
const toggleStatus = async (row) => {
    const oldStatus = row.status;
    try {
        await ElMessageBox.confirm(`确定要${row.status ? "启用" : "禁用"}该规则吗？`, "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
        });
        const res = await updateWebsiteStatus(row.website_id, row.status);
        if (res.code === 200) {
            ElMessage.success("状态更新成功");
            await refresh();
        } else {
            row.status = oldStatus;  // 失败时还原状态
            ElMessage.error(res.message || "状态更新失败");
        }
    } catch (error) {
        row.status = oldStatus;
        if (error !== "cancel") {
            ElMessage.error("请求失败，请检查网络或稍后重试");
            console.error("状态更新失败:", error);
        }
    }
};


// 添加规则弹窗
const openRuleDialog = () => {
  showRuleDialog.value = true;
  newRule.value = { website_url: "", type_id: null, status: 1 }; // 清空数据
};

// 处理用户输入
const normalizeInput = (input) => {
    return input.replace(/\r\n/g, "\n").replace(/\r/g, "\n").trim();
};

// 提交规则
const submitRule = async () => {
    if (!newRule.value.website_url.trim() || !newRule.value.type_id) {
        return ElMessage.error("请输入网址并选择网站类型");;
    }

    try {
        await ElMessageBox.confirm("确定要添加该网站规则吗？", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "info",
        });
        newRule.value.website_url = normalizeInput(newRule.value.website_url);  // 确保 \r\n , \r 处理为 \n
        const res = await addWebsiteRule(newRule.value);
        if (res.code === 200) {
            ElMessage.success("规则添加成功");
            newRule.value.website_url = "";
            showRuleDialog.value = false;
            await refresh();
        } else {
            ElMessage.error(res.message || "添加失败");
        }
    } catch (error) {
        if (error !== "cancel") {
            ElMessage.error("请求失败，请检查网络或稍后重试");
            console.error("添加网站规则错误:", error);
        }
    }
};

// 类型弹窗
const openTypeDialog = () => {
  showTypeDialog.value = true;
  newType.value = { type_name: "" }; 
};

// 提交网站类型
const submitType = async () => {
    if (!newType.value.type_name.trim()) {     
        return ElMessage.error("网站类型不能为空");;
    }

    try {
        await ElMessageBox.confirm("确定要添加该网站类型吗？", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "info",
        });
        const res = await addWebsiteType(newType.value.type_name.trim());
        if (res.code === 200) {
            ElMessage.success("网站类型添加成功");
            newType.value.type_name = "";  // 清空输入框
            showTypeDialog.value = false; //关闭弹窗
            await refresh();
        } else {
            ElMessage.error(res.message || "添加失败");
        }
    } catch (error) {
        if (error !== "cancel") {
            ElMessage.error("请求失败，请检查网络或稍后重试");
            console.error("添加网站类型错误:", error);
        }
    }
};

onMounted(refresh);
</script>

<style scoped>
.operate-container {
margin-bottom: 15px;
padding: 15px;
}

.card-spacing {
margin-bottom: 16px;
}

.table-spacing {
margin-top: 16px;
}
</style>
