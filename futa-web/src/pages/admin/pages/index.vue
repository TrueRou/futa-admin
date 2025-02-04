<script setup lang="ts">
import type { Page, ReportSimple } from '@/types';
import axios from 'axios';
import { ElMessage, type FormInstance } from 'element-plus';
import { ref } from 'vue';

const pages = ref<Page[]>([]);
const reports = ref<ReportSimple[]>([]);
const formShow = ref(false);
const formTitle = ref("");
const formModel = ref<Page>();
const formModelReports = ref<number[]>([]);
const formRef = ref<FormInstance>()
const formRules = {
    path: [{ required: true, message: "请输入路径", trigger: "blur" }],
    name: [{ required: true, message: "请输入名称", trigger: "blur" }],
    description: [{ required: true, message: "请输入描述", trigger: "blur" }]
}
pages.value = (await axios.get(`/pages`)).data
reports.value = (await axios.get(`/reports`)).data;

const deletePage = async (page: Page) => {
    await axios.delete(`/pages/${page.path}`);
    pages.value = pages.value.filter((p) => p.path !== page.path);
    ElMessage.success("删除成功: /" + page.path);
}

const showAddForm = () => {
    formTitle.value = "新建页面";
    formShow.value = true;
    formModel.value = { path: "", name: "", description: "", reports: [] }
    formModelReports.value = [];
}

const showEditForm = async (page: Page) => {
    formTitle.value = `编辑 /${page.path}`;
    formShow.value = true;
    formModel.value = { ...page };
    formModelReports.value = page.reports.map((r) => r.id);
}

const confirmForm = async (formRef: FormInstance | undefined) => {
    await formRef?.validate(async (valid, fields) => {
        if (!valid) return;
        if (formTitle.value === "新建页面") {
            const resp = await axios.post(`/pages/${formModel.value!.path}`, formModel.value);
            pages.value.push(resp.data);
            ElMessage.success("新建成功: /" + formModel.value!.path);
        } else {
            const editTarget = formTitle.value.split("/")[1];
            const resp = await axios.patch(`/pages/${editTarget}`, formModel.value);
            const index = pages.value.findIndex((p) => p.path === editTarget);
            pages.value[index] = resp.data;
            ElMessage.success("编辑成功: /" + formModel.value!.path);
        }
        const appendReports = formModelReports.value.filter((id) => !formModel.value!.reports.map((r) => r.id).includes(id));
        const removeReports = formModel.value!.reports.filter((r) => !formModelReports.value.includes(r.id));
        for (const id of appendReports) await axios.post(`/pages/${formModel.value!.path}/reports/${id}`);
        for (const report of removeReports) await axios.delete(`/pages/${formModel.value!.path}/reports/${report.id}`);
        const index = pages.value.findIndex((p) => p.path === formModel.value!.path);
        pages.value[index].reports = reports.value.filter((r) => formModelReports.value.includes(r.id));
        formShow.value = false;
    });
}

const cancelForm = () => {
    formShow.value = false;
}
</script>
<template>
    <el-card shadow="never" class="h-full border-0" body-class="h-full">
        <template #header>
            <div class="flex justify-between">
                <span class="font-semibold flex items-center">页面定义</span>
                <el-button type="primary" @click="showAddForm">新建页面</el-button>
            </div>
        </template>
        <el-table :data="pages" :stripe="true" class="h-full">
            <el-table-column :show-overflow-tooltip="false" prop="path" label="路径" width="150" />
            <el-table-column :show-overflow-tooltip="true" prop="name" label="名称" width="150" />
            <el-table-column :show-overflow-tooltip="true" prop="description" label="描述" width="250" />
            <el-table-column :show-overflow-tooltip="true" label="链接图表">
                <template #default="scope">
                    {{ scope.row.reports.map((report: ReportSimple) => report.label).join(', ') }}
                </template>
            </el-table-column>
            <el-table-column width="165" fixed="right" label="操作">
                <template #default="scope">
                    <div class="flex">
                        <el-button type="info" @click="showEditForm(scope.row)">编辑</el-button>
                        <el-button type="danger" @click="deletePage(scope.row)">删除</el-button>
                    </div>
                </template>
            </el-table-column>
        </el-table>
    </el-card>
    <el-dialog v-model="formShow" :title="formTitle" width="600px" draggable align-center>
        <template #default>
            <el-form ref="formRef" :model="formModel" status-icon :rules="formRules" v-if="formModel">
                <el-form-item label="路径" prop="path">
                    <el-input v-model="formModel.path" autocomplete="off" />
                </el-form-item>

                <el-form-item label="名称" prop="name">
                    <el-input v-model="formModel.name" autocomplete="off" />
                </el-form-item>

                <el-form-item label="描述" prop="description">
                    <el-input v-model="formModel.description" autocomplete="off" />
                </el-form-item>

                <el-form-item label="链接图表" prop="report">
                    <el-select filterable v-model="formModelReports" multiple collapse-tags placeholder="请选择链接的图表">
                        <el-option v-for="report in reports" :label="report.label" :value="report.id">
                            <span style="float: left">{{ report.label }}</span>
                            <span style="float: right; color: var(--el-text-color-secondary); font-size: 13px;">
                                {{ report.type }}
                            </span>
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
        </template>
        <template #footer>
            <span>
                <el-button type="primary" @click="confirmForm(formRef)">确认</el-button>
                <el-button @click="cancelForm()">取消</el-button>
            </span>
        </template>
    </el-dialog>
</template>