import { createRouter, createWebHistory } from 'vue-router'
import main from '../components/main.vue'
import book from '../components/book.vue'
import rawdata from '../components/rawdata.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: main
    },
    {
      path: '/book',
      name: 'book',
      component: book
    },
    {
      path: '/rawdata',
      name: 'rawdata',
      component: rawdata
    },
  ],
})

export default router
