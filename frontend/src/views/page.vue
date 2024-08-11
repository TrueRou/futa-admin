<script setup lang="ts">
import { useSession } from '@/store/session';
import axios from 'axios';
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import ReportTable from './report/table.vue';
import ReportChartLine from './report/charts/line.vue';
import { ReportType, type ReportFragment, type ReportFull } from '@/types';

const session = useSession()
const route = useRoute()
const page = session.pages.find((page) => page.path === route.params.path)!
const reports = ref<ReportFull[]>([])
const fragments = ref<ReportFragment[]>([])
const filter_dict = ref<{ [key: string]: string }>({})

fragments.value = (await axios.get(`/reports/fragments/`)).data

page.reports.forEach(async (report) => {
    reports.value.push((await axios.post(`/reports/${report.id}`)).data)
})

const updateReports = async () => {
    [...reports.value].forEach(async (report, index) => {
        reports.value.splice(index, 1, (await axios.post(`/reports/${report.id}`, filter_dict.value)).data)
    })
}

watch(filter_dict, async () => await updateReports(), { deep: true })
</script>
<template>
    <div class="ml-4 mt-4">
        <h2>{{ page.name }}</h2>
        <p class="text-lg">{{ page.description }}</p>
    </div>
    <div class="ml-4 mt-4" v-for="frag in fragments" :key="frag.trait">
        <el-select style="width: 160px;" v-model="filter_dict[frag.trait]" :placeholder="'筛选 ' + frag.name" size="large"
            clearable>
            <el-option v-for="item in frag.values" :key="item" :label="item" :value="item" />
        </el-select>
    </div>
    <div class="ml-4 mr-4 mt-4" v-for="report in reports" :key="report.id">
        <ReportTable v-if="report.type == ReportType.FORM" :report="report" @update="updateReports" />
        <ReportChartLine v-if="report.type == ReportType.LINE_CHART" :report="report" />
    </div>
</template>