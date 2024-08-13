<script setup lang="ts">
import type { ReportFull } from '@/types';
import { ReportFragmentType } from '@/types';
import { reactive, watch } from 'vue';

const props = defineProps<{
    report: ReportFull
}>()

const filters = props.report.fragments.filter((fragment) => fragment.type < 10)
const filterValues = reactive<{ [key: string]: any }>({})

watch(() => filterValues, () => {
    console.log(filterValues)
}, { immediate: true })
</script>
<template>
    <template v-for="filter in filters" :key="filter.trait">
        <el-select v-if="filter.type == ReportFragmentType.FILTER_SELECT" style="width: 160px;"
            v-model="filterValues[filter.trait]" :placeholder="'筛选 ' + filter.name" size="large" clearable>
            <el-option v-for="item in filter.values" :key="item" :label="item" :value="item" />
        </el-select>
        <el-date-picker v-if="filter.type == ReportFragmentType.FILTER_DATEPICKER" v-model="filterValues[filter.trait]"
            type="daterange" unlink-panels range-separator="到" start-placeholder="起始日期" end-placeholder="终止日期" />
    </template>

</template>