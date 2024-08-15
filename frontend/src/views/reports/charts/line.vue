<script setup lang="ts">
import { type ReportFull } from '@/types';
import VChart from 'vue-echarts';
import 'echarts';
import { computed } from 'vue';

const props = defineProps<{
    report: ReportFull
}>()

const emits = defineEmits<{
    update: []
}>()

const option = computed(() => {
    return {
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
            bottom: '20px',
            left: '40px',
            right: '0px'
        },
        series: props.report.fields.map((field, index) => {
            return {
                name: field.name,
                type: 'line',
                data: props.report.data.map((row) => row[index]),
            }
        })
    };
})
</script>
<template>
    <v-chart class="h-80" :option="option" autoresize></v-chart>
</template>