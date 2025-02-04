<script setup lang="ts">
import { ReportFragmentType, ReportTypeMap, type ReportFragment, type ReportSimple } from '@/types';
import axios from 'axios';
import { ElMessage, type FormInstance } from 'element-plus';
import { ref, onMounted } from 'vue';

const props = defineProps<{
    report?: ReportSimple
}>();
const fragments = ref<ReportFragment[]>([]);
const formShow = ref(false);
const formTitle = ref('');
const formType = ref<'add' | 'edit'>('add');
const formModel = ref<Partial<ReportFragment>>({});
const formRef = ref<FormInstance>();
const formRules = {
    trait: [{ required: true, message: '请输入筛选特征', trigger: 'blur' }],
    label: [{ required: true, message: '请输入筛选标签', trigger: 'blur' }],
    type: [{ required: true, message: '请选择筛选类型', trigger: 'change' }],
    sql: [{ required: true, message: '请输入SQL语句', trigger: 'blur' }],
    extends: [{ required: true, message: '请输入自定义选择器配置', trigger: 'blur' }],
};

onMounted(async () => {
    await fetchFragments();
});

const fetchFragments = async () => {
    const response = await axios.get('/fragments?report_id=' + props.report!.id);
    fragments.value = response.data;
};

const showAddForm = () => {
    formType.value = 'add';
    formTitle.value = '新增筛选器';
    formShow.value = true;
    formModel.value = {
        trait: '',
        label: '',
        type: ReportFragmentType.FILTER_DATERANGE,
        sql: '',
        extends: '',
    };
};

const showEditForm = (fragment: ReportFragment) => {
    formType.value = 'edit';
    formTitle.value = '编辑筛选器';
    formShow.value = true;
    formModel.value = { ...fragment };
};

const confirmForm = async (formRef: FormInstance | undefined) => {
    await formRef?.validate(async (valid) => {
        if (!valid) return;

        if (formType.value === 'add') {
            const response = await axios.post('/fragments?report_id=' + props.report!.id, formModel.value);
            fragments.value.push(response.data);
            ElMessage.success('新增成功');
        } else {
            await axios.patch(`/fragments/${formModel.value.id}`, formModel.value);
            const index = fragments.value.findIndex(f => f.id === formModel.value.id);
            if (index !== -1) {
                fragments.value[index] = { ...fragments.value[index], ...formModel.value };
            }
            ElMessage.success('修改成功');
        }
        await fetchFragments();
        formShow.value = false;
    });
};

const deleteFragment = async (fragment: ReportFragment) => {
    await axios.delete(`/fragments/${fragment.id}`);
    fragments.value = fragments.value.filter(f => f.id !== fragment.id);
    ElMessage.success('删除成功');
};
</script>

<template>
    <el-card shadow="never" class="h-full border-0" body-class="h-full">
        <template #header>
            <div class="flex justify-between">
                <span class="font-semibold flex items-center">筛选器管理</span>
                <el-button type="primary" @click="showAddForm">新增筛选器</el-button>
            </div>
        </template>

        <el-table :data="fragments" row-key="id" class="h-full">
            <el-table-column prop="trait" label="筛选特征" width="180" />
            <el-table-column prop="type" label="筛选类型" width="200">
                <template #default="{ row }: { row: ReportFragment }">
                    {{ ReportTypeMap[row.type] }}
                </template>
            </el-table-column>
            <el-table-column prop="name" label="筛选器名称" />
            <el-table-column label="操作" width="174" fixed="right">
                <template #default="scope">
                    <div class="flex gap-2">
                        <el-button type="primary" @click="showEditForm(scope.row)">编辑</el-button>
                        <el-button type="danger" @click="deleteFragment(scope.row)">删除</el-button>
                    </div>
                </template>
            </el-table-column>
        </el-table>
    </el-card>

    <el-dialog v-model="formShow" :title="formTitle" width="600px">
        <el-form ref="formRef" :model="formModel" :rules="formRules" label-width="100px">
            <el-form-item label="筛选特征" prop="trait">
                <el-input v-model="formModel.trait!" placeholder="请输入筛选特征字段" />
            </el-form-item>

            <el-form-item label="筛选标签" prop="label">
                <el-input v-model="formModel.label!" placeholder="请输入筛选标签" />
            </el-form-item>

            <el-form-item label="筛选类型" prop="type">
                <el-select v-model="formModel.type!" placeholder="请选择类型">
                    <el-option label="时段选择器" :value="ReportFragmentType.FILTER_DATERANGE"></el-option>
                    <el-option label="月份选择器" :value="ReportFragmentType.FILTER_DATEMONTH"></el-option>
                    <el-option label="单日选择器" :value="ReportFragmentType.FILTER_DATEDAY"></el-option>
                    <el-option label="自定义选择器" :value="ReportFragmentType.FILTER_SELECT"></el-option>
                </el-select>
            </el-form-item>

            <el-form-item label="自定义配置" prop="extends" v-if="formModel.type === ReportFragmentType.FILTER_SELECT">
                <b-ace-editor v-model="formModel.extends!" lang="json" width="100%" height="200px" theme="chrome" />
            </el-form-item>


            <el-form-item label="SQL语句" prop="sql">
                <b-ace-editor v-model="formModel.sql!" lang="sql" width="100%" height="200px" theme="chrome" />
            </el-form-item>
        </el-form>

        <template #footer>
            <el-button @click="formShow = false">取消</el-button>
            <el-button type="primary" @click="confirmForm(formRef)">确认</el-button>
        </template>
    </el-dialog>
</template>