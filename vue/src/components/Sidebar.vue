<template>
  <el-aside class="sidebar" width="150px">
    <el-menu
      :default-active="activeMenu"
      background-color="#f4f4f4"
      text-color="#333"
      active-text-color="#409EFF"
      router
    >
      <!-- 递归渲染菜单 -->
      <template v-for="menu in filteredMenuList" :key="menu.menu_id">
        <el-menu-item
          v-if="!menu.children || menu.children.length === 0"
          :index="menu.name"
          @click="navigateTo(menu.name)"
        >
          <el-icon>
            <component :is="menu.icon"></component>
          </el-icon>
          <span>{{ menu.title }}</span>
        </el-menu-item>

        <el-sub-menu v-else :index="menu.name">
          <template #title>
            <el-icon>
              <component :is="menu.icon"></component>
            </el-icon>
            <span>{{ menu.title }}</span>
          </template>

          <el-menu-item
            v-for="child in menu.children"
            :key="child.menu_id"
            :index="child.name"
            @click="navigateTo(child.name)"
          >
            <el-icon>
              <component :is="child.icon"></component>
            </el-icon>
            <span>{{ child.title }}</span>
          </el-menu-item>
        </el-sub-menu>
      </template>
    </el-menu>

<!-- 窗口 A 显示设置按钮，窗口 B 不显示 -->
    <div v-if="window_key === 'A'" class="setting-button">
      <el-icon class="icon-button"  @click="openSetting"><Setting /></el-icon>
    </div>
  </el-aside>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { getMenuTree } from "@/api/ums/menu";
import { useRouter } from "vue-router";

const menuList = ref([]);
const activeMenu = ref("");
const router = useRouter();
const window_key = ref("A");

// 加载菜单
const loadMenu = async () => {
  try {
    window_key.value = await window.electron.getWindowType(); // 获取当前窗口标识
    const response = await getMenuTree(window_key.value); // 获取树形结构菜单
    console.log("菜单数据：", response.data); 
    
    menuList.value = Array.isArray(response.data) ? response.data : [];

    // 默认选中第一个菜单
    if (menuList.value.length > 0) {
      activeMenu.value = menuList.value[0].name;
    }
  } catch (error) {
    console.error("菜单加载失败:", error);
    menuList.value = [];
  }
};

// 过滤启用的菜单
const filteredMenuList = computed(() => {
  return Array.isArray(menuList.value) ? menuList.value.filter(menu => menu.hidden === 0) : [];
});

// 路由跳转
const navigateTo = (routeName) => {
  if (window_key.value === "B") {
    let basePath = "/setting";
    const parentMenu = menuList.value.find(menu =>
      menu.children?.some(child => child.name === routeName)
    );
    if (parentMenu) {
      basePath += `/${parentMenu.name}`;
    }
    router.push({path: `${basePath}/${routeName}`});
  } else {
    router.push({ name: routeName });
  }
};

// 打开设置窗口
const openSetting = () => {
  window.electron.openSetting();
};

onMounted(() => {
  loadMenu();
});
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  background-color: #f4f4f4;
  height: 100vh;
  border-right: 1px solid #dcdcdc;
}

.setting-button {
  margin-top: auto;
  width: 100%;
  display: flex;
  justify-content: center; 
  padding: 10px 0;
}

.icon-button {
  font-size: 30px; 
  cursor: pointer; 
  color: #6b6666; 
  transition: color 0.3s, transform 0.1s ease-in-out; 
}

.icon-button:active {
  transform: scale(0.9); 
  color: #dfe3e7; 
}
</style>
