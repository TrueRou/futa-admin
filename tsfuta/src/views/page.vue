<script setup lang="ts">
import Report from '@/views/report.vue';
import { ref } from 'vue';
import type { Page } from '@/types';

const reportStamp = ref(new Date())

const props = defineProps<{
    page: Page
}>()


const updateStamp = () => {
    reportStamp.value = new Date()
}

</script>
<template>
    <div class="ml-4 mt-4">
        <h2>{{ props.page.name }}</h2>
        <p class="text-lg">{{ props.page.description }}</p>
    </div>
    <div class="ml-4 mr-4 mt-4 mb-4" v-for="report in props.page.reports.sort((a, b) => a.id - b.id)" :key="report.id">
        <Report :ident="report.id" :stamp="reportStamp" @updateStamp="updateStamp"></Report>
    </div>
</template>