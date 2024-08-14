<script setup lang="ts">
import type { ReportFragment } from '@/types';
import { ReportFragmentType } from '@/types';
import { ref, watch } from 'vue';

const value = ref<any>()

const props = defineProps<{
    fragment: ReportFragment
}>()

const emits = defineEmits<{
    filter: [source: string, value: string]
}>()

const toDate = (date: Date) => {
    const year = date.getFullYear()
    const month = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1
    const day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate()
    return `${year}-${month}-${day} 00:00:00`
}

watch(value, (newVal) => {
    if (props.fragment.type == ReportFragmentType.FILTER_DATEPICKER) {
        newVal = newVal ? toDate(newVal[0]) + "," + toDate(newVal[1]) : null
    }
    emits("filter", props.fragment.trait, newVal)
})

const shortcuts = [
    {
        text: '过去一周',
        value: () => {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            return [start, end]
        },
    },
    {
        text: '过去一个月',
        value: () => {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            return [start, end]
        },
    },
    {
        text: '过去三个月',
        value: () => {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
            return [start, end]
        },
    },
    {
        text: '过去一年',
        value: () => {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 365)
            return [start, end]
        },
    },
]
</script>
<template>
    <div>
        <el-select v-if="props.fragment.type == ReportFragmentType.FILTER_SELECT" style="width: 160px;" v-model="value"
            :placeholder="'筛选 ' + props.fragment.name" size="large" clearable>
            <el-option v-for="item in props.fragment.values" :key="item" :label="item" :value="item" />
        </el-select>
        <el-date-picker v-if="props.fragment.type == ReportFragmentType.FILTER_DATEPICKER" v-model="value"
            type="daterange" unlink-panels range-separator="到" start-placeholder="起始日期" end-placeholder="终止日期"
            :shortcuts="shortcuts" />
    </div>
</template>