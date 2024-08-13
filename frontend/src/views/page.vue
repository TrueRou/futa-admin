<script setup lang="ts">
import { useSession } from '@/store/session';
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import ReportTable from './report/table.vue';
import ReportChartLine from './report/charts/line.vue';
import ReportFilter from './report/fragments/filter.vue';
import { ReportType, type ReportFull } from '@/types';

const session = useSession()
const route = useRoute()
const page = session.pages.find((page) => page.path === route.params.path)!
const reports = ref<ReportFull[]>([])
const fragments = ref<{ [key: string]: string }>({})

page.reports.forEach(async (report) => {
    reports.value.push((await axios.post(`/reports/${report.id}`)).data)
})

const updateReports = async () => {
    [...reports.value].forEach(async (report, index) => {
        reports.value.splice(index, 1, (await axios.post(`/reports/${report.id}`, fragments.value)).data)
    })
}

const updateFragment = (source: string, value: string) => {
    fragments.value[source] = value
    updateReports()
}

</script>
<template>
    <div class="ml-4 mt-4">
        <h2>{{ page.name }}</h2>
        <p class="text-lg">{{ page.description }}</p>
    </div>

    <div class="ml-4 mr-4 mt-4 mb-4" v-for="report in reports.sort((a, b) => a.id - b.id)" :key="report.id">
        <el-card class="mt-4" shadow="hover">
            <template #header>
                <span class="font-semibold">{{ report.name }}</span>
                <div class="mt-4" v-if="report.fragments.length != 0">
                    <template v-for="fragment in report.fragments">
                        <ReportFilter v-if="fragment.type < 10" :fragment="fragment" @filter="updateFragment">
                        </ReportFilter>
                    </template>
                </div>
            </template>
            <ReportTable v-if="report.type == ReportType.FORM" :report="report" @update="updateReports" />
            <ReportChartLine v-else-if="report.type == ReportType.LINE_CHART" :report="report" />
        </el-card>
    </div>
</template>