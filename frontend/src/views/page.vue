<script setup lang="ts">
import { useSession } from '@/store/session';
import axios from 'axios';
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import ReportTable from './report/table.vue';
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
    <template v-for="report in reports">
        <ReportTable v-if="report.type == ReportType.FORM" :data="report.data" :fields="report.fields" />
    </template>

</template>