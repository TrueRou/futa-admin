<template>
    <el-container class="layout-container-demo" style="height: calc(100vh - 60px)">
        <el-aside width="200px">
            <el-scrollbar>
                <el-menu :default-active="$route.path" class="border-r-0" router>
                    <el-menu-item>
                        <el-icon>
                            <house />
                        </el-icon>回到主页
                    </el-menu-item>
                    <el-sub-menu index="1">
                        <template #title>
                            <el-icon>
                                <files />
                            </el-icon>系统结构
                        </template>
                        <el-menu-item-group>
                            <template #title>页面元素</template>
                            <el-menu-item index="/admin/pages">
                                <el-icon>
                                    <document />
                                </el-icon>页面定义
                            </el-menu-item>
                            <el-menu-item>
                                <el-icon>
                                    <data-analysis />
                                </el-icon>图表定义
                            </el-menu-item>
                        </el-menu-item-group>
                        <el-menu-item-group>
                            <template #title>图表元素</template>
                            <el-menu-item>
                                <el-icon>
                                    <knife-fork />
                                </el-icon>筛选器
                            </el-menu-item>
                            <el-menu-item>
                                <el-icon>
                                    <bowl />
                                </el-icon>混合器
                            </el-menu-item>
                        </el-menu-item-group>
                    </el-sub-menu>
                </el-menu>
            </el-scrollbar>
        </el-aside>
        <el-main style="border-left: 1px solid var(--el-menu-border-color);" class="w-full h-full overflow-y-hidden">
            <router-view />
        </el-main>
    </el-container>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Menu as IconMenu, Message, Setting } from '@element-plus/icons-vue'

const item = {
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
}
const tableData = ref(Array.from({ length: 20 }).fill(item))
</script>

<style scoped>
.layout-container-demo .el-header {
    position: relative;
    background-color: var(--el-color-primary-light-7);
    color: var(--el-text-color-primary);
}

.layout-container-demo .el-aside {
    color: var(--el-text-color-primary);
    background: var(--el-color-primary-light-8);
}

.layout-container-demo .el-menu {
    border-right: none;
}

.layout-container-demo .el-main {
    padding: 0;
}

.layout-container-demo .toolbar {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    right: 20px;
}
</style>