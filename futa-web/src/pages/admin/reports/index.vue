<script setup lang="ts">
import { ReportType, type ReportSimple } from '@/types';
import axios from 'axios';
import { ElMessage, type FormInstance } from 'element-plus';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const reports = ref<ReportSimple[]>([]);
const formShow = ref(false);
const formModel = ref<ReportSimple>();
const formRef = ref<FormInstance>()
const formRules = {
    label: [{ required: true, message: '请输入名称', trigger: 'blur' }],
    type: [{ required: true, message: '请选择类型', trigger: 'blur' }],
    appendable: [{ required: true, message: '请选择是否可插入', trigger: 'blur' }],
};
reports.value = (await axios.get(`/reports`)).data;

const deleteReport = async (report: ReportSimple) => {
    await axios.delete(`/reports/${report.id}`);
    reports.value = reports.value.filter((r) => r.id !== report.id);
    ElMessage.success("删除成功: " + report.label);
}

const editReport = async (report: ReportSimple) => {
    router.push(`/admin/reports/${report.id}`);
}

const showAddForm = () => {
    formShow.value = true;
    formModel.value = { label: "", type: ReportType.FORM, appendable: false, linked_table: null, id: -1 }
}

const confirmForm = async (formRef: FormInstance | undefined) => {
    await formRef?.validate(async (valid, fields) => {
        if (!valid) return;
        const resp = await axios.post(`/reports`, formModel.value);
        reports.value.push(resp.data);
        ElMessage.success("新建成功: " + formModel.value!.label);
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
                <span class="font-semibold flex items-center">图表定义</span>
                <el-button type="primary" @click="showAddForm">新建图表</el-button>
            </div>
        </template>
        <el-table :data="reports" :stripe="true" class="h-full">
            <el-table-column :show-overflow-tooltip="false" prop="id" label="ID" width="100" />
            <el-table-column :show-overflow-tooltip="true" prop="label" label="图表名称" />
            <el-table-column :show-overflow-tooltip="true" prop="linked_table" label="关联数据表" width="300" />
            <el-table-column width="165" fixed="right" label="操作">
                <template #default="scope">
                    <div class="flex">
                        <el-button type="info" @click="editReport(scope.row)">编辑</el-button>
                        <el-button type="danger" @click="deleteReport(scope.row)">删除</el-button>
                    </div>
                </template>
            </el-table-column>
        </el-table>
    </el-card>
    <el-dialog v-model="formShow" title="创建图表" width="30%" draggable align-center>
        <template #default>
            <el-form ref="formRef" :model="formModel" status-icon :rules="formRules" v-if="formModel">
                <el-form-item label="图表标签" prop="label">
                    <el-input v-model="formModel.label" autocomplete="off" />
                </el-form-item>

                <el-form-item label="图表类型" prop="type">
                    <el-select v-model="formModel.type" placeholder="请选择类型">
                        <el-option label="表格" :value="ReportType.FORM"></el-option>
                        <el-option label="折线图" :value="ReportType.LINE_CHART"></el-option>
                        <el-option label="柱状图" :value="ReportType.BAR_CHART"></el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="允许插入" prop="appendable">
                    <el-switch v-model="formModel.appendable" />
                </el-form-item>
            </el-form>
        </template>
        <template #footer>
            <span>
                <el-button @click="cancelForm()">取消</el-button>
                <el-button type="primary" @click="confirmForm(formRef)">确认</el-button>
            </span>
        </template>
    </el-dialog>
</template>