<script setup lang="ts">
import { useSession } from '@/store/session';
import axios from 'axios';
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import ReportTable from './report/table.vue';
import ReportChartLine from './report/charts/line.vue';
import { ReportType, type ReportFull } from '@/types';

const session = useSession()
const route = useRoute()
const page = session.pages.find((page) => page.path === route.params.path)!
const reports = ref<ReportFull[]>([])

page.reports.forEach(async (report) => {
    reports.value.push((await axios.post(`/reports/${report.id}`)).data)
})
</script>
<template>
    <h1>{{ page.name }}</h1>
    {{ page.description }}
    <template v-for="report in reports">
        <ReportTable v-if="report.type == ReportType.FORM" :report="report" />
        <ReportChartLine v-else-if="report.type == ReportType.LINE_CHART" :report="report" />
    </template>
</template>