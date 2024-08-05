<template>
  <el-container class="h-full w-full">
    <el-header style="text-align: right; font-size: 12px">
      <div class="toolbar">
        <el-dropdown>
          <el-icon style="margin-right: 8px; margin-top: 1px">
            <setting />
          </el-icon>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item>View</el-dropdown-item>
              <el-dropdown-item>Add</el-dropdown-item>
              <el-dropdown-item>Delete</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <span>Tom</span>
      </div>
    </el-header>
    <el-container>
      <el-aside width="200px">
        <el-scrollbar>
          <el-menu :default-active="$router.currentRoute.value.path" :default-openeds="['analysis']" :router="true">
            <el-menu-item index="/">
              <el-icon>
                <HomeFilled />
              </el-icon>主页
            </el-menu-item>
            <el-sub-menu index="analysis">
              <template #title>
                <el-icon>
                  <Grid />
                </el-icon>
                数据分析
              </template>
              <el-menu-item v-for="page in session.pages" :index="'/' + page.path">{{ page.title }}</el-menu-item>
            </el-sub-menu>
          </el-menu>
        </el-scrollbar>
      </el-aside>
      <el-main class="content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useSession } from './store/session';
import router from './router';

const session = useSession();

const item = {
  date: '2016-05-02',
  name: 'Tom',
  address: 'No. 189, Grove St, Los Angeles',
}
const tableData = ref(Array.from({ length: 200 }).fill(item))
</script>

<style scoped>
.el-header {
  height: 50px;
  color: var(--el-text-color-primary);
  border-left: 1px solid var(--el-menu-border-color);
  border-bottom: 1px solid var(--el-menu-border-color);
}

.el-menu {
  border-right: none;
  position: relative;
  top: 0px;
  left: 0px;
}

.el-main {
  border-left: 1px solid var(--el-menu-border-color);
  padding: 0;
}

.toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}

.content {
  position: relative;
  width: 100%;
  height: calc(100vh - 50px);
  overflow-y: scroll;
}
</style>