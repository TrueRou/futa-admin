<template>
    <el-card shadow="never" class="h-full border-0" body-class="h-full">
        <template #header>
            <div class="flex justify-between">
                <span class="font-semibold flex items-center">SQL编辑</span>
                <el-select v-model="fontSize" placeholder="选择字体大小" style="width: 120px" @change="handleFontSizeChange">
                    <el-option v-for="size in fontSizes" :key="size" :label="`${size}px`" :value="size" />
                </el-select>
            </div>
        </template>

        <b-ace-editor v-model="model" lang="sql" width="100%" height="460px" theme="chrome" :font-size="fontSize" />
    </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElSelect, ElOption } from 'element-plus'

const model = defineModel()
const fontSizes = [12, 14, 16, 18, 20]
const fontSize = ref(16)

onMounted(() => {
    const savedSize = localStorage.getItem('editorFontSize')
    if (savedSize) {
        fontSize.value = parseInt(savedSize)
    }
})

const handleFontSizeChange = (newSize) => {
    localStorage.setItem('editorFontSize', newSize)
}
</script>