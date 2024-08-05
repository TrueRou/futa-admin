<script setup lang="ts">
import { useSession } from '@/store/session';
import axios from 'axios';
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const session = useSession()
const route = useRoute()
const page = session.pages.find((page) => page.path === route.params.path)!
const reports = ref<ReportFull[]>([])

page.reports.forEach(async (report) => {
    reports.value.push((await axios.post(`/reports/${report.id}`)).data)
})
</script>
<template>
    <div v-for="report in reports">{{ report.name }}</div>
</template>