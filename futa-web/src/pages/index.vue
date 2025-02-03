<script setup lang="ts">
import type { Page } from '@/types';
import PageView from '@/views/page.vue';
import axios from 'axios';
import { ref } from 'vue';

const pages = ref<Page[]>([]);
const currentPage = ref<Page | null>(null);
pages.value = (await axios.get(`/pages`)).data
</script>

<template>
    <el-aside width="200px" style="height: calc(100vh - 60px)">
        <el-scrollbar>
            <el-menu class="border-r-0">
                <el-menu-item v-for="page in pages" @click="currentPage = page" :index="page.path">
                    {{ page.name }}
                </el-menu-item>
            </el-menu>
        </el-scrollbar>
    </el-aside>
    <el-main class="overflow-y-scroll w-full relative p-0"
        style="height: calc(100vh - 60px); border-left: 1px solid var(--el-menu-border-color);">
        <Suspense>
            <template #default>
                <PageView v-if="currentPage" :page="currentPage" />
            </template>
            <template #fallback>
                <el-skeleton :rows="16" :throttle="500" />
            </template>
        </Suspense>
    </el-main>
</template>