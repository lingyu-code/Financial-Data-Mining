import { createRouter, createWebHistory } from 'vue-router'
import main from '../components/main.vue'
import paper from '../components/paper.vue'
import paperAnalysis from '../components/paper-analysis.vue'
import rawdata from '../components/rawdata.vue'
import visualization from '../components/visualization.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: main
    },
    {
      path: '/paper',
      name: 'paper',
      component: paper
    },
    {
      path: '/paper-analysis',
      name: 'paper-analysis',
      component: paperAnalysis
    },
    {
      path: '/rawdata',
      name: 'rawdata',
      component: rawdata
    },
    {
      path: '/visualization',
      name: 'visualization',
      component: visualization
    },
  ],
})

export default router
