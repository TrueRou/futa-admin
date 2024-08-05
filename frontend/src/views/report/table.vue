<script setup lang="ts">
import { ReportFieldType, type ReportField, type ReportFull } from '@/types';
import { computed } from 'vue';

const props = defineProps<{
    report: ReportFull
}>()

const tableData = computed(() => {
    return props.report.data.map((row) => {
        const rowData: Record<string, string | number> = {};
        props.report.fields.forEach((field, index) => {
            rowData[field.name] = row[index];
        });
        return rowData;
    });
});

const findWidth = (field: ReportField) => {
    return field.type == ReportFieldType.NUMBER ? '180' : '240';
}
</script>
<template>
    <el-table :data="tableData" class="w-full">
        <el-table-column v-for="field in report.fields" :prop="field.name" :label="field.name"
            :width="findWidth(field)" />
    </el-table>
</template>