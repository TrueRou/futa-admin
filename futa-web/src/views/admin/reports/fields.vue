<script setup lang="ts">
import { ReportFieldType, type ReportField, type ReportSimple } from '@/types';
import axios from 'axios';
import { ElMessage, type FormInstance } from 'element-plus';
import { ref, onMounted } from 'vue';

const props = defineProps<{
    report?: ReportSimple
}>();
const fields = ref<ReportField[]>([]);
const formShow = ref(false);
const formTitle = ref('');
const formType = ref<'add' | 'edit'>('add');
const formModel = ref<Partial<ReportField>>({});
const formRef = ref<FormInstance>();
const formRules = {
    label: [{ required: true, message: '请输入字段标签', trigger: 'blur' }],
    type: [{ required: true, message: '请选择字段类型', trigger: 'change' }],
    order: [{ required: true, message: '请输入排序值', trigger: 'blur' }]
};

onMounted(async () => {
    await fetchFields();
});

const fetchFields = async () => {
    const response = await axios.get('/fields?report_id=' + props.report!.id);
    fields.value = response.data.sort((a: any, b: any) => a.order - b.order);
};

const showAddForm = () => {
    formType.value = 'add';
    formTitle.value = '新增字段';
    formShow.value = true;
    const maxOrder = fields.value.length ? Math.max(...fields.value.map(f => f.order)) : 0;
    formModel.value = {
        order: maxOrder + 1,
        label: '',
        type: ReportFieldType.TEXT,
        linked_field: null
    };
};

const showEditForm = (field: ReportField) => {
    formType.value = 'edit';
    formTitle.value = '编辑字段';
    formShow.value = true;
    formModel.value = { ...field };
};

const confirmForm = async (formRef: FormInstance | undefined) => {
    await formRef?.validate(async (valid) => {
        if (!valid) return;

        if (formType.value === 'add') {
            const response = await axios.post('/fields?report_id=' + props.report!.id, formModel.value);
            fields.value.push(response.data);
            ElMessage.success('新增成功');
        } else {
            await axios.patch(`/fields/${formModel.value.id}`, formModel.value);
            const index = fields.value.findIndex(f => f.id === formModel.value.id);
            if (index !== -1) {
                fields.value[index] = { ...fields.value[index], ...formModel.value };
            }
            ElMessage.success('修改成功');
        }
        await fetchFields();
        formShow.value = false;
    });
};

const deleteField = async (field: ReportField) => {
    await axios.delete(`/fields/${field.id}`);
    fields.value = fields.value.filter(f => f.id !== field.id);
    ElMessage.success('删除成功');
};

const moveField = async (field: ReportField, direction: 'up' | 'down') => {
    const currentIndex = fields.value.findIndex(f => f.id === field.id);
    if (currentIndex === -1) return;

    const targetIndex = direction === 'up' ? currentIndex - 1 : currentIndex + 1;
    if (targetIndex < 0 || targetIndex >= fields.value.length) return;

    await axios.patch(`/fields/${field.id}`, {
        label: null,
        type: null,
        linked_field: null,
        order: fields.value[targetIndex].order
    });
    await fetchFields();
    ElMessage.success('移动成功');
};
</script>

<template>
    <el-card shadow="never" class="h-full border-0" body-class="h-full">
        <template #header>
            <div class="flex justify-between">
                <span class="font-semibold flex items-center">字段管理</span>
                <el-button type="primary" @click="showAddForm">新增字段</el-button>
            </div>
        </template>

        <el-table :data="fields" row-key="id" class="h-full">
            <el-table-column prop="order" label="排序" width="80" />
            <el-table-column prop="label" label="字段标签" width="150" />
            <el-table-column prop="type" label="字段类型" width="120">
                <template #default="{ row }">
                    {{ row.type === ReportFieldType.NUMBER ? '数字' : '文本' }}
                </template>
            </el-table-column>
            <el-table-column prop="linked_field" label="关联字段" />
            <el-table-column label="操作" width="336" fixed="right">
                <template #default="scope">
                    <div class="flex gap-2">
                        <el-button @click="moveField(scope.row, 'up')" :disabled="scope.$index === 0">上移</el-button>
                        <el-button @click="moveField(scope.row, 'down')" :disabled="scope.$index === fields.length - 1">
                            下移
                        </el-button>
                        <el-button type="primary" @click="showEditForm(scope.row)">编辑</el-button>
                        <el-button type="danger" @click="deleteField(scope.row)">删除</el-button>
                    </div>
                </template>
            </el-table-column>
        </el-table>
    </el-card>

    <el-dialog v-model="formShow" :title="formTitle" width="500px">
        <el-form ref="formRef" :model="formModel" :rules="formRules" label-width="80px">
            <el-form-item label="排序" prop="order" v-if="formType === 'add'">
                <el-input-number v-model="formModel.order!" :min="1" />
            </el-form-item>

            <el-form-item label="标签" prop="label">
                <el-input v-model="formModel.label!" />
            </el-form-item>

            <el-form-item label="类型" prop="type">
                <el-select v-model="formModel.type!" placeholder="请选择字段类型">
                    <el-option label="数字" :value="ReportFieldType.NUMBER" />
                    <el-option label="文本" :value="ReportFieldType.TEXT" />
                </el-select>
            </el-form-item>

            <el-form-item label="关联字段">
                <el-input v-model="formModel.linked_field!" placeholder="请输入关联字段名" />
            </el-form-item>
        </el-form>

        <template #footer>
            <el-button @click="formShow = false">取消</el-button>
            <el-button type="primary" @click="confirmForm(formRef)">确认</el-button>
        </template>
    </el-dialog>
</template>