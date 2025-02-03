<template>
    <div class="editor-container">
        <div class="controls">
            <el-select v-model="fontSize" placeholder="选择字体大小" style="width: 120px" @change="handleFontSizeChange">
                <el-option v-for="size in fontSizes" :key="size" :label="`${size}px`" :value="size" />
            </el-select>
        </div>
        <b-ace-editor ref="editorRef" lang="sql" width="100%" height="460px" theme="chrome" :font-size="fontSize" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElSelect, ElOption } from 'element-plus'

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

<style scoped>
.editor-container {
    position: relative;
    margin: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.controls {
    display: flex;
    justify-content: flex-end;
    padding: 10px 15px;
    background: #f5f7fa;
    border-radius: 8px 8px 0 0;
    border-bottom: 1px solid #ebeef5;
}

:deep(.ace_editor) {
    border-radius: 0 0 8px 8px;
    transition: all 0.3s ease;
}
</style>