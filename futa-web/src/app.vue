<template>
  <el-container class="h-full w-full">
    <el-header class="flex justify-between items-center">
      <div class="flex items-center font-bold text-lg">{{ siteName }}</div>
      <el-button class="flex items-center" @click="router.push('/admin')">
        <el-icon :size="24">
          <setting />
        </el-icon>
      </el-button>
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
import { RouterView, useRouter } from 'vue-router';

const siteName = ref(import.meta.env.VITE_SITE_NAME);
const router = useRouter();
</script>

<style scoped>
.el-header {
  height: 60px;
  color: var(--el-text-color-primary);
  border-left: 1px solid var(--el-menu-border-color);
  border-bottom: 1px solid var(--el-menu-border-color);
}
</style>