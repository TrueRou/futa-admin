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
      <Suspense>
        <RouterView />
      </Suspense>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { RouterView } from 'vue-router';

const siteName = ref(import.meta.env.VITE_SITE_NAME);

</script>

<style scoped>
.el-header {
  height: 50px;
  color: var(--el-text-color-primary);
  border-left: 1px solid var(--el-menu-border-color);
  border-bottom: 1px solid var(--el-menu-border-color);
}

.toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}
</style>