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

if (props.fragment.type == ReportFragmentType.FILTER_DATEDAY) {
    const date = new Date()
    date.setHours(0, 0, 0, 0)
    value.value = date
}

if (props.fragment.type == ReportFragmentType.FILTER_DATEMONTH) {
    const date = new Date()
    date.setDate(0)
    date.setHours(0, 0, 0, 0)
    value.value = date
}

const toDate = (date: Date) => {
    const year = date.getFullYear()
    const month = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1
    const day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate()
    return `${year}-${month}-${day} 00:00:00`
}

watch(value, (newVal) => {
    if (props.fragment.type == ReportFragmentType.FILTER_DATERANGE) {
        newVal = newVal ? toDate(newVal[0]) + "," + toDate(newVal[1]) : null
    }
    if (props.fragment.type == ReportFragmentType.FILTER_DATEDAY) {
        const nextDay = new Date()
        if (newVal) nextDay.setTime(newVal.getTime() + 3600 * 1000 * 24)
        newVal = newVal ? toDate(newVal) + "," + toDate(nextDay) : null
    }
    if (props.fragment.type == ReportFragmentType.FILTER_DATEMONTH) {
        if (!newVal) return
        const thisMonth = new Date(newVal)
        thisMonth.setDate(0)
        const nextMonth = new Date(thisMonth)
        nextMonth.setMonth(thisMonth.getMonth() + 2, 0)
        newVal = toDate(thisMonth) + "," + toDate(nextMonth)
    }
    emits("filter", props.fragment.trait, newVal)
}, { immediate: true })

const rangeShortcuts = [
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

const dayShortcuts = [
    {
        text: '今天',
        value: () => {
            const date = new Date()
            date.setHours(0, 0, 0, 0)
            return date
        },
    },
    {
        text: '昨天',
        value: () => {
            const date = new Date()
            date.setHours(0, 0, 0, 0)
            date.setTime(date.getTime() - 3600 * 1000 * 24)
            return date
        },
    },
]

const monthShortcuts = [
    {
        text: '本月',
        value: () => {
            const date = new Date()
            date.setDate(0)
            date.setHours(0, 0, 0, 0)
            return date
        },
    },
    {
        text: '上月',
        value: () => {
            var date = new Date()
            date.setHours(0, 0, 0, 0)
            date.setMonth(date.getMonth() - 1, 0)
            return date
        },
    },
]
</script>
<template>
    <div>
        <el-select v-if="props.fragment.type == ReportFragmentType.FILTER_SELECT" style="width: 160px;" v-model="value"
            :placeholder="'筛选 ' + props.fragment.name" clearable>
            <el-option v-for="label, index in props.fragment.labels" :key="label" :label="label"
                :value="props.fragment.values[index]" />
        </el-select>
        <el-date-picker v-if="props.fragment.type == ReportFragmentType.FILTER_DATERANGE" v-model="value"
            type="daterange" unlink-panels range-separator="到" start-placeholder="起始日期" end-placeholder="终止日期"
            :shortcuts="rangeShortcuts" />
        <el-date-picker v-if="props.fragment.type == ReportFragmentType.FILTER_DATEDAY" v-model="value" type="date"
            :placeholder="'筛选 ' + props.fragment.name" :shortcuts="dayShortcuts" />
        <el-date-picker v-if="props.fragment.type == ReportFragmentType.FILTER_DATEMONTH" v-model="value" type="month"
            :placeholder="'筛选 ' + props.fragment.name" :shortcuts="monthShortcuts" />
    </div>
</template>