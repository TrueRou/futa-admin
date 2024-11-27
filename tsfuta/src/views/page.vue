<script setup lang="ts">
import { useSession } from '@/store/session';
import { useRoute } from 'vue-router';
import Report from './reports/report.vue';
import { ref } from 'vue';

const session = useSession()
const route = useRoute()
const page = session.pages.find((page) => page.path === route.params.path)!
const reportStamp = ref(new Date())

const updateStamp = () => {
    reportStamp.value = new Date()
}

</script>
<template>
    <div class="ml-4 mt-4">
        <h2>{{ page.name }}</h2>
        <p class="text-lg">{{ page.description }}</p>
    </div>
    <div class="ml-4 mr-4 mt-4 mb-4" v-for="report in page.reports.sort((a, b) => a.id - b.id)" :key="report.id">
        <Report :ident="report.id" :stamp="reportStamp" @updateStamp="updateStamp"></Report>
    </div>
</template>