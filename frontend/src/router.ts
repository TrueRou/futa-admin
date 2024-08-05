import Home from '@/views/home.vue'
import Page from '@/views/page.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { useSession } from './store/session'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/:path',
      name: 'Page',
      component: Page
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const session = useSession()
  await session.ensurePages()
  next()
})

export default router
