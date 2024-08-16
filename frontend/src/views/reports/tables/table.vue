<script setup lang="ts">
import { ReportFieldType, type ReportField, type ReportFull } from '@/types';
import { removeCommonPrefix } from '@/utils';
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
            rowData[field.name] = row[index];
        });
        return rowData;
    });
    var firstCols = flatted.map((row) => Object.values(row)[0]);
    navCols.value = firstCols; // for update field
    if (firstCols.length > 1) firstCols = removeCommonPrefix(firstCols);
    flatted.forEach((row, index) => {
        row[Object.keys(row)[0]] = firstCols[index];
    });

    return flatted;
});

const findWidth = (field: ReportField) => {
    return field.type == ReportFieldType.NUMBER ? '60' : '120';
}

const dbClickCell = (scope: any) => {
    const field = props.report.fields.find((field) => field.name === scope.column.property)!
    const navValue = scope.row[Object.keys(scope.row)[0]]
    if (field.field_name == null) return
    if (navValue.indexOf("合计") != -1) return

    tableRowEditIndex.value = scope.$index
    tableColumnEditIndex.value = scope.column.id

    nextTick(() => {
        tableRowInputRef.value[0].focus()
    })
}

const onInputTableBlur = async (scope: any) => {
    tableRowEditIndex.value = -1
    tableColumnEditIndex.value = -1
    const navField = props.report.fields.find(field => field.name == Object.keys(scope.row)[0])!
    const upsertField = props.report.fields.find(field => field.name == scope.column.property)!
    const navValue = navCols.value[scope.$index]
    const value = scope.row[scope.column.property]

    await axios.patch(`/reports/${props.report.id}?` + qs.stringify({
        nav_field_pos: navField.field_pos,
        nav_value: navValue,
        field_pos: upsertField.field_pos,
        value: value
    }))

    emits('updateStamp') // update all the reports data in the current page.
}

</script>
<template>
    <el-table v-if="showTable" :data="tableData" class="w-full" :max-height="400" stripe>
        <el-table-column v-for="field in report.fields" :prop="field.name" :label="field.name"
            :min-width="findWidth(field)">
            <template #header>
                <el-icon v-if="field.field_name != null && field.field_pos != 0">
                    <EditPen />
                </el-icon>
                {{ field.name }}
            </template>
            <template #default="scope">
                <el-input v-if="tableRowEditIndex === scope.$index && tableColumnEditIndex == scope.column.id"
                    ref="tableRowInputRef" v-model="scope.row[scope.column.property]" @blur="onInputTableBlur(scope)"
                    @keyup.enter="(e: any) => e.target.blur()" />
                <div v-else class=" h-8" @dblclick="dbClickCell(scope)">
                    <p>
                        {{ scope.row[scope.column.property] }}
                    </p>
                </div>
            </template>
        </el-table-column>
    </el-table>
</template>