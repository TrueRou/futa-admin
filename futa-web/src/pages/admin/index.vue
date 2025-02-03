<template>
    <el-container class="layout-container" style="height: calc(100vh - 60px)">
        <el-aside width="200px">
            <el-scrollbar>
                <el-menu :default-active="$route.path" :default-openeds="['1']" class="border-r-0" router>
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
                            <el-menu-item index="/admin/reports">
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

<style scoped>
.layout-container .el-header {
    position: relative;
    background-color: var(--el-color-primary-light-7);
    color: var(--el-text-color-primary);
}

.layout-container .el-menu {
    border-right: none;
}

.layout-container .el-main {
    padding: 0;
}

.layout-container .toolbar {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    right: 20px;
}
</style>