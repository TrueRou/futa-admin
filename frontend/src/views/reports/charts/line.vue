<script setup lang="ts">
import { type ReportFull } from '@/types';
import VChart from 'vue-echarts';
import 'echarts';
import { ref, watch, type Ref } from 'vue';
import { deepMergeDict } from '@/utils';

const props = defineProps<{
    report: ReportFull,
}>()

const emits = defineEmits<{
    update: []
}>()

const option = ref({})

const updateOption = () => {
    const mixin = props.report.mixins.find((mixin) => mixin.ref_variable == 'option')
    var optionValue: Record<string, any> = {
        xAxis: {
            type: 'category',
            axisTick: {
                alignWithLabel: true
            },
            data: props.report.data.map((row) => row[0]),
        },
        yAxis: {
            type: 'value'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: props.report.fields.slice(1).map((field) => field.name),
        },
        grid: {
            top: '40px',
            bottom: '60px',
            left: '80px',
            right: '40px'
        },
        series: props.report.fields.map((field, index) => {
            return {
                name: field.name,
                type: 'line',
                data: props.report.data.map((row) => row[index]),
            }
        })
    }
    // Apply merge with mixin
    if (mixin != null) optionValue = deepMergeDict(optionValue, mixin.values)
    option.value = optionValue
}

watch(() => props.report, updateOption, { immediate: true, deep: true })
</script>
<template>
    <v-chart class="mt-4 h-80" :option="option" autoresize></v-chart>
</template>