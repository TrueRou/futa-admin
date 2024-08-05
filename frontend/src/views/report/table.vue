<script setup lang="ts">
import { ReportFieldType, type ReportField } from '@/types';
import { computed } from 'vue';

const props = defineProps<{
    data: (string | number)[][]
    fields: ReportField[]
}>()

const tableData = computed(() => {
    return props.data.map((row) => {
        const rowData: Record<string, string | number> = {};
        props.fields.forEach((field, index) => {
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
        <el-table-column v-for="field in fields" :prop="field.name" :label="field.name" :width="findWidth(field)" />
    </el-table>
</template>