<template>
  <el-container class="h-full w-full">
    <el-header class="flex justify-between">
      <div class="flex items-center font-bold text-lg">{{ siteName }}</div>
      <div class="toolbar flex">
        <el-dropdown>
          <el-icon :size="24" style="margin-right: 8px; margin-top: 1px">
            <setting />
          </el-icon>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item>导入数据表</el-dropdown-item>
              <el-dropdown-item>查看数据表</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    <el-container>
      <el-aside width="200px" style="height: calc(100vh - 50px)">
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
              <el-menu-item v-for="page in session.pages" :index="'/' + page.path">{{ page.name }}</el-menu-item>
            </el-sub-menu>
          </el-menu>
        </el-scrollbar>
      </el-aside>
      <el-main class="content">
        <Suspense>
          <template #default>
            <router-view :key="$router.currentRoute.value.path" />
          </template>
          <template #fallback>
            <el-skeleton :rows="16" :throttle="500" />
          </template>
        </Suspense>
      </el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useSession } from './store/session';

const session = useSession();
const siteName = ref(import.meta.env.VITE_SITE_NAME);

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