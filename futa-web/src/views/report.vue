<script setup lang="ts">
import axios from 'axios';
import { ReportType, type ReportFull } from '@/types';
import { computed, ref, watch } from 'vue';
import ReportTable from '@/components/table.vue';
import ReportChartLine from '@/components/charts/line.vue';
import ReportFilter from '@/components/fragments/filter.vue';
import { Plus, Minus } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

const props = defineProps<{
    ident: number
    stamp: Date
}>()

const emits = defineEmits<{
    updateStamp: []
}>()

const report = ref<ReportFull>()
const reports = ref<{ [key: string]: ReportFull }>({})
const fragmentDefs = ref<string[]>(["条件组1"])
const fragmentSets = ref<[{ [key: string]: string }]>([{}])

const newRowDialogVisible = ref(false)
const newRowForm = ref<Record<string, any>>({})

const fetchReports = async () => {
    for (const [index, fragmentDef] of fragmentDefs.value.entries()) {
        const response = await axios.post(`/reports/${props.ident}`, fragmentSets.value[index])
        reports.value[fragmentDef] = response.data
    }
    updateReport()
}

const updateReport = () => {
    const keys = Object.keys(reports.value)
    const values = Object.values(reports.value)
    const length = values.length
    if (length == 0) return // no data
    // fill the empty data columns with 0, if any
    for (let i = 0; i < length; i++) {
        if (values[i].data.length == 0) {
            const firstFull = values.find((value) => value.data.length != 0)
            if (firstFull) {
                values[i].data = firstFull.data.map((row) => [row[0], 0])
            }
        }
    }
    const result = { ...values[0], fields: [...values[0].fields] }
    if (!allowFragmentSets.value || length <= 1) {
        report.value = values[0]
        return
    }
    result.fields[1].label = keys[0]
    for (let i = 1; i < length; i++) {
        const newField = { ...result.fields[1] }
        newField.label = keys[i]
        newField.id = i + 1
        result.fields.push(newField)

        values[i].data.forEach((row, index) => {
            result.data[index].push(row[1])
        })
    }
    report.value = result
}

const handleFileUpload = async (report_id: number) => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.xlsx'; // Specify the accepted file type(s) here
    fileInput.addEventListener('change', async (event: any) => {
        const file = event.target.files[0];
        if (file) {
            try {
                const formData = new FormData();
                formData.append('file', file);
                ElMessage('正在导入,请稍候...');
                // Make a POST request to the backend API endpoint to upload the file
                const response = await axios.post('/imports/excel?report_id=' + report_id.toString(), formData);
                if (response.status === 200) {
                    // File uploaded successfully
                    await fetchReports()
                    ElMessage({
                        message: '导入成功.',
                        type: 'success',
                    })
                }
            } catch (error) {
                ElMessage({
                    message: '导入失败, 请检查文件格式是否正确.',
                    type: 'error',
                })
            }
        }
    });
    fileInput.click();
};

const insertFragment = async () => {
    fragmentDefs.value.push(`条件组${fragmentDefs.value.length + 1}`)
    fragmentSets.value.push({})
    await fetchReports()
}

const removeFragment = async (index: number) => {
    const key = fragmentDefs.value.splice(index, 1)
    fragmentSets.value.splice(index, 1)
    delete (reports.value[key[0]])
    await fetchReports()
}

const updateFragment = async (index: number, source: string, value: string) => {
    fragmentSets.value[index][source] = value
    await fetchReports()
}

const newRow = async () => {
    await axios.post(`/reports/${report.value?.id}/rows`, newRowForm.value)
    newRowDialogVisible.value = false
    newRowForm.value = {}
    await fetchReports()
}

const allowFragmentSets = computed(() => {
    const values = Object.values(reports.value)
    const firstElement = values[0]
    if (!firstElement) return false
    return firstElement.type > 10 && firstElement.fields.length == 2

})

watch(() => props.stamp, fetchReports, { immediate: true })
</script>
<template>
    <el-card class="mt-4" shadow="hover">
        <template #header>
            <div class="flex flex-col">
                <div class="flex items-center justify-between">
                    <span class="font-semibold flex">{{ report?.label }}</span>
                    <div class="mr-2" v-if="report?.linked_table && report?.appendable">
                        <el-button type="info" @click="handleFileUpload(report?.id)">批量导入</el-button>
                        <el-button type="primary" @click="newRowDialogVisible = true">单条插入</el-button>
                    </div>
                </div>
                <template v-for="(_, index) in fragmentDefs.length">
                    <div class="mt-4 flex" v-if="report?.fragments.length != 0">
                        <template v-for="fragment in report?.fragments">
                            <ReportFilter class="mr-2" v-if="fragment.type < 10" :fragment="fragment"
                                @filter="(source, value) => updateFragment(index, source, value)">
                            </ReportFilter>
                        </template>
                        <el-button class="mr-2" :icon="Minus" type="danger"
                            v-if="allowFragmentSets && index == fragmentDefs.length - 1 && index != 0"
                            @click="removeFragment(index)" />
                        <el-button class="mr-2" :icon="Plus" type="primary"
                            v-if="allowFragmentSets && index == fragmentDefs.length - 1" @click="insertFragment" />
                    </div>
                </template>
            </div>
        </template>
        <ReportTable v-if="report?.type == ReportType.FORM" :report="report" @updateStamp="emits('updateStamp')" />
        <ReportChartLine v-else-if="report?.type == ReportType.LINE_CHART" :report="report" />
    </el-card>
    <el-dialog v-model="newRowDialogVisible" title="添加条目" width="500">
        <el-form label-width="auto">
            <el-form-item v-for="field in report?.fields.filter(f => f.linked_field)" :label="field.label">
                <el-input v-model="newRowForm[field.linked_field!]" autocomplete="off" />
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="newRowDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="newRow">确认</el-button>
            </div>
        </template>
    </el-dialog>
</template>