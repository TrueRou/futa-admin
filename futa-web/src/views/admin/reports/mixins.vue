<script setup lang="ts">
import axios from 'axios';
import { ElMessage, type FormInstance } from 'element-plus';
import { ref, onMounted } from 'vue';
import type { ReportMixin, ReportSimple } from '@/types';

const props = defineProps<{
    report?: ReportSimple
}>();

const mixins = ref<ReportMixin[]>([]);
const formShow = ref(false);
const formTitle = ref('');
const formType = ref<'add' | 'edit'>('add');
const formModel = ref<Partial<ReportMixin>>({});
const formRef = ref<FormInstance>();
const formRules = {
    ref_variable: [{ required: true, message: '请输入引用变量', trigger: 'blur' }],
    values: [{ required: true, message: '请输入变量值', trigger: 'blur' }],
};

onMounted(async () => {
    await fetchMixins();
});

const fetchMixins = async () => {
    const response = await axios.get('/mixins?report_id=' + props.report!.id);
    mixins.value = response.data;
};

const showAddForm = () => {
    formType.value = 'add';
    formTitle.value = '新增混合器';
    formShow.value = true;
    formModel.value = {
        ref_variable: '',
        values: ''
    };
};

const showEditForm = (mixin: ReportMixin) => {
    formType.value = 'edit';
    formTitle.value = '编辑混合器';
    formShow.value = true;
    formModel.value = { ...mixin };
};

const confirmForm = async (formRef: FormInstance | undefined) => {
    await formRef?.validate(async (valid) => {
        if (!valid) return;

        if (formType.value === 'add') {
            const response = await axios.post('/mixins?report_id=' + props.report!.id, formModel.value);
            mixins.value.push(response.data);
            ElMessage.success('新增成功');
        } else {
            await axios.patch(`/mixins/${formModel.value.id}`, formModel.value);
            const index = mixins.value.findIndex(m => m.id === formModel.value.id);
            if (index !== -1) {
                mixins.value[index] = { ...mixins.value[index], ...formModel.value };
            }
            ElMessage.success('修改成功');
        }
        formShow.value = false;
        await fetchMixins();
    });
};

const deleteMixin = async (mixin: ReportMixin) => {
    try {
        await axios.delete(`/mixins/${mixin.id}`);
        mixins.value = mixins.value.filter(m => m.id !== mixin.id);
        ElMessage.success('删除成功');
    } catch (e) {
        ElMessage.error('删除失败');
    }
};
</script>

<template>
    <el-card shadow="never" class="h-full border-0" body-class="h-full">
        <template #header>
            <div class="flex justify-between">
                <span class="font-semibold flex items-center">混合器管理</span>
                <el-button type="primary" @click="showAddForm">新增混合器</el-button>
            </div>
        </template>

        <el-table :data="mixins" row-key="id" class="h-full">
            <el-table-column prop="ref_variable" label="引用变量" width="200" />
            <el-table-column prop="values" label="变量值" />
            <el-table-column label="操作" width="174" fixed="right">
                <template #default="scope">
                    <div class="flex gap-2">
                        <el-button type="primary" @click="showEditForm(scope.row)">编辑</el-button>
                        <el-button type="danger" @click="deleteMixin(scope.row)">删除</el-button>
                    </div>
                </template>
            </el-table-column>
        </el-table>
    </el-card>

    <el-dialog v-model="formShow" :title="formTitle" width="600px">
        <el-form ref="formRef" :model="formModel" :rules="formRules" label-width="100px">
            <el-form-item label="引用变量" prop="ref_variable">
                <el-input v-model="formModel.ref_variable!" placeholder="请输入变量引用名称" />
            </el-form-item>

            <el-form-item label="混合值" prop="values">
                <b-ace-editor v-model="formModel.values!" lang="json" width="100%" height="200px" theme="chrome" />
            </el-form-item>
        </el-form>

        <template #footer>
            <el-button @click="formShow = false">取消</el-button>
            <el-button type="primary" @click="confirmForm(formRef)">确认</el-button>
        </template>
    </el-dialog>
</template>