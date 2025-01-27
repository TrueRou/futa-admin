<script setup lang="ts">
import { type ReportFull } from '@/types';
import axios from 'axios';
import qs from 'qs';
import { computed, nextTick, ref } from 'vue';

const props = defineProps<{
    report: ReportFull
}>()

const emits = defineEmits<{
    updateStamp: []
}>()

const tableRowEditIndex = ref(-1);
const tableColumnEditIndex = ref(-1);
const tableRowInputRef: any = ref(null);
const navCols = ref<(string | number)[]>([]);
const showTable = ref(false);


// to prohibit the table from showing before the data is ready
setTimeout(() => {
    showTable.value = true;
}, 200);

const tableData = computed(() => {
    var flatted = props.report.data.map((row) => {
        const rowData: Record<string, string | number> = {};
        props.report.fields.forEach((field, index) => {
            rowData[field.label] = row[index];
        });
        return rowData;
    });
    var firstCols = flatted.map((row) => Object.values(row)[0]);
    navCols.value = firstCols; // for update field
    flatted.forEach((row, index) => {
        row[Object.keys(row)[0]] = firstCols[index];
    });

    return flatted;
});

const dbClickCell = (scope: any) => {
    const field = props.report.fields.find((field) => field.label === scope.column.property)!
    const navValue = scope.row[Object.keys(scope.row)[0]]
    if (!field.linked_field) return
    if (typeof (navValue) == 'string' && navValue.indexOf("合计") != -1) return

    tableRowEditIndex.value = scope.$index
    tableColumnEditIndex.value = scope.column.id

    nextTick(() => {
        tableRowInputRef.value[0].focus()
    })
}

const onInputTableBlur = async (scope: any) => {
    tableRowEditIndex.value = -1
    tableColumnEditIndex.value = -1
    const navField = props.report.fields.find(field => field.label == Object.keys(scope.row)[0])!
    const upsertField = props.report.fields.find(field => field.label == scope.column.property)!
    const navValue = navCols.value[scope.$index]
    const value = scope.row[scope.column.property]

    await axios.patch(`/reports/${props.report.id}?` + qs.stringify({
        nav_field_id: navField.id,
        nav_value: navValue,
        field_id: upsertField.id,
        value: value
    }))

    emits('updateStamp') // update all the reports data in the current page.
}

const deleteRow = async (scope: any) => {
    const navValue = navCols.value[scope.$index]

    await axios.delete(`/reports/${props.report.id}/rows?` + qs.stringify({
        primary_key_value: navValue,
    }))

    emits('updateStamp') // update all the reports data in the current page.
}

const tableMaxHeight = computed(() => {
    return window.innerHeight - 300;
})

</script>
<template>
    <el-table v-if="showTable" :data="tableData" class="w-full" :max-height="tableMaxHeight" stripe>
        <template :key="field.label" v-for="field in report.fields">
            <el-table-column :prop="field.label" :label="field.label" :min-width="60">
                <template #header>
                    <el-icon v-if="field.linked_field">
                        <EditPen />
                    </el-icon>
                    {{ field.label }}
                </template>
                <template #default="scope">
                    <el-input v-if="tableRowEditIndex === scope.$index && tableColumnEditIndex == scope.column.id"
                        ref="tableRowInputRef" v-model="scope.row[scope.column.property]"
                        @blur="onInputTableBlur(scope)" @keyup.enter="(e: any) => e.target.blur()" />
                    <div v-else class=" h-8" @dblclick="dbClickCell(scope)">
                        <p>
                            {{ scope.row[scope.column.property] }}
                        </p>
                    </div>
                </template>
            </el-table-column>
        </template>
        <template v-if="report.linked_table && report.appendable">
            <el-table-column width="100" fixed="right" label="操作">
                <template #default="scope">
                    <el-button type="danger" @click="deleteRow(scope)">
                        删除
                    </el-button>
                </template>
            </el-table-column>
        </template>
    </el-table>
</template>