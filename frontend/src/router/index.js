import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Login from '../pages/Login.vue'

const adminNav = [
  { path: '/admin/dashboard', label: 'Dashboard', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>' },
  { path: '/admin/carreras', label: 'Carreras', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>' },
  { path: '/admin/alumnos', label: 'Alumnos', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>' },
  { path: '/admin/empresas', label: 'Empresas', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>' },
]

const alumnoNav = [
  { path: '/alumno/dashboard', label: 'Dashboard', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>' },
  { path: '/alumno/vacantes', label: 'Mis postulaciones', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>' },
]

const empresaNav = [
  { path: '/empresa/dashboard', label: 'Dashboard', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>' },
  { path: '/empresa/vacantes', label: 'Vacantes', icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>' },
]

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login,
  },
  {
    path: '/admin',
    component: () => import('../pages/admin/Layout.vue'),
    meta: { role: 'admin', nav: adminNav },
    children: [
      { path: '', redirect: { name: 'admin.dashboard' } },
      { path: 'dashboard', name: 'admin.dashboard', component: () => import('../pages/admin/Dashboard.vue'), meta: { title: 'Dashboard' } },
      { path: 'carreras', name: 'admin.carreras', component: () => import('../pages/admin/Carreras.vue'), meta: { title: 'Carreras' } },
      { path: 'alumnos', name: 'admin.alumnos', component: () => import('../pages/admin/Alumnos.vue'), meta: { title: 'Alumnos' } },
      { path: 'empresas', name: 'admin.empresas', component: () => import('../pages/admin/Empresas.vue'), meta: { title: 'Empresas' } },
    ],
  },
  {
    path: '/alumno',
    component: () => import('../pages/alumno/Layout.vue'),
    meta: { role: 'alumno', nav: alumnoNav },
    children: [
      { path: '', redirect: { name: 'alumno.dashboard' } },
      { path: 'dashboard', name: 'alumno.dashboard', component: () => import('../pages/alumno/Dashboard.vue'), meta: { title: 'Mi Panel' } },
      { path: 'vacantes', name: 'alumno.vacantes', component: () => import('../pages/alumno/Catalogo.vue'), meta: { title: 'Vacantes' } },
      { path: 'vacantes/:id', name: 'alumno.vacantes.detalle', component: () => import('../pages/alumno/Detalle.vue'), meta: { title: 'Detalle' } },
      { path: 'vacantes/:id/postular', name: 'alumno.vacantes.postular', component: () => import('../pages/alumno/Postular.vue'), meta: { title: 'Postular' } },
    ],
  },
  {
    path: '/empresa',
    component: () => import('../pages/empresa/Layout.vue'),
    meta: { role: 'empresa', nav: empresaNav },
    children: [
      { path: '', redirect: { name: 'empresa.dashboard' } },
      { path: 'dashboard', name: 'empresa.dashboard', component: () => import('../pages/empresa/Dashboard.vue'), meta: { title: 'Dashboard' } },
      { path: 'vacantes', name: 'empresa.vacantes', component: () => import('../pages/empresa/Vacantes.vue'), meta: { title: 'Vacantes' } },
    ],
  },
  { path: '/:pathMatch(.*)*', redirect: '/login' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _, next) => {
  const auth = useAuthStore()
  if (to.meta.role && (!auth.token || auth.role !== to.meta.role)) {
    return next('/login')
  }
  if (to.name === 'login' && auth.token) {
    const roleRoutes = { admin: '/admin/dashboard', alumno: '/alumno/dashboard', empresa: '/empresa/dashboard' }
    return next(roleRoutes[auth.role] || '/login')
  }
  next()
})

export default router
