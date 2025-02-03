<script setup lang="ts">
import type { ReportAdmin } from '@/types';
import axios from 'axios';
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

import ReportSql from '@/views/admin/reports/sql.vue'
import ReportFragments from '@/views/admin/reports/fragments.vue'
import ReportFields from '@/views/admin/reports/fields.vue'
import ReportMixins from '@/views/admin/reports/mixins.vue'

const route = useRoute()
const report = ref<ReportAdmin>()
const isSaving = ref(false)
const lastSaveTime = ref<Date>()

const autoSave = debounce(async () => {
    if (!report.value) return

    try {
        isSaving.value = true
        await axios.patch(`/reports/${report.value.id}`, report.value)
        lastSaveTime.value = new Date()
    } catch (error) {
        ElMessage.error({
            message: '保存失败，请检查网络连接',
            duration: 3000,
            showClose: true
        })
    } finally {
        isSaving.value = false
    }
}, 500)

const fetchReport = async (id: string | string[]) => {
    try {
        const { data } = await axios.get<ReportAdmin>(`/reports/${id}`)
        report.value = data
    } catch (error) {
        ElMessage.error('数据加载失败')
    }
}

watch(
    () => report.value,
    (newVal) => {
        if (newVal) autoSave()
    },
    { deep: true }
)

function debounce<T extends (...args: any[]) => any>(fn: T, delay: number) {
    let timeoutId: number | null = null
    return function (this: unknown, ...args: Parameters<T>) {
        if (timeoutId) clearTimeout(timeoutId)
        timeoutId = setTimeout(() => {
            fn.apply(this, args)
        }, delay) as unknown as number
    }
}

watch(() => route.params.id, fetchReport, { immediate: true })
</script>

<template>
    <div class="flex flex-col h-full p-4 space-y-4 bg-gray-50">
        <el-form :model="report" label-width="120px" class="bg-white shadow-md rounded-lg p-6 relative" v-if="report">
            <div class="absolute right-4 top-4 text-sm text-gray-500">
                <template v-if="isSaving">
                    <i class="el-icon-loading mr-1" />
                    保存中...
                </template>
                <template v-else-if="lastSaveTime">
                    <i class="el-icon-success text-green-500 mr-1" />
                    已保存 {{ lastSaveTime.toLocaleTimeString() }}
                </template>
            </div>
            <div class="space-y-4 max-w-3xl">
                <el-form-item label="报告名称">
                    <el-input v-model="report.label" placeholder="请输入报告名称" class="w-full" />
                </el-form-item>

                <el-form-item label="报告类型">
                    <el-select v-model="report.type" placeholder="请选择报告类型" class="w-full">
                        <el-option v-for="t in ['TABLE', 'VIEW', 'CUSTOM']" :key="t" :label="t" :value="t" />
                    </el-select>
                </el-form-item>

                <el-form-item label="关联数据表">
                    <el-input v-model="report.linked_table" placeholder="请输入关联表名" class="w-full" />
                </el-form-item>

                <el-form-item label="允许追加数据">
                    <el-switch v-model="report.appendable" />
                </el-form-item>
            </div>
        </el-form>
        <el-tabs type="card" class="flex-1 bg-white shadow-md rounded-lg p-4 min-h-0" v-if="report">
            <el-tab-pane label="SQL编辑">
                <report-sql :report="report" v-model="report.sql" />
            </el-tab-pane>
            <el-tab-pane label="字段管理" lazy>
                <report-fields :report="report" />
            </el-tab-pane>
            <el-tab-pane label="筛选器管理" lazy>
                <report-fragments />
            </el-tab-pane>
            <el-tab-pane label="混合器管理" lazy>
                <report-mixins />
            </el-tab-pane>
        </el-tabs>
    </div>
</template>