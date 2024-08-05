<script setup lang="ts">
import { type ReportFull } from '@/types';
import VChart from 'vue-echarts';
import 'echarts';
import { computed } from 'vue';

const props = defineProps<{
    report: ReportFull
}>()

const option = computed(() => {
    return {
        xAxis: {
            type: 'category',
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