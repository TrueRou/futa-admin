import HomeView from '@/components/HomeView.vue'
import PageView from '@/components/PageView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/:pageId',
      name: 'Page',
      component: PageView
    }
  ]
})

export default router
