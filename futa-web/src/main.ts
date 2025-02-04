import 'element-plus/dist/index.css'
import './assets/base.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import ElementPlus, { ElMessage } from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import Editor from 'bin-editor-next';
import axios from 'axios'
import App from './app.vue'
import router from './router'
import { zhCn } from 'element-plus/es/locales.mjs'

import * as ace from 'brace'
import 'brace/ext/emmet'
import 'brace/ext/language_tools'
import 'brace/mode/sql'
import 'brace/snippets/sql'
import 'brace/theme/chrome'


axios.defaults.baseURL = import.meta.env.VITE_URL;
const app = createApp(App)

app.use(createPinia())
app.component(Editor.name, Editor)
app.use(router)
app.use(ElementPlus, {
    locale: zhCn,
})
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

axios.interceptors.response.use(function (response) {
    return response;
}, function (error) {
    console.log(error);
    ElMessage.error("操作失败: " + error.response.data.detail);
    return Promise.reject(error);
});

app.mount('#app')
