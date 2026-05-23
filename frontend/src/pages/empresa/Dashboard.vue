<template>
  <div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 font-medium">Vacantes</p>
            <p class="text-2xl font-bold mt-1">{{ stats.vacantes ?? '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center text-blue-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 font-medium">Abiertas</p>
            <p class="text-2xl font-bold mt-1 text-emerald-600">{{ stats.abiertas ?? '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-emerald-50 rounded-lg flex items-center justify-center text-emerald-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 font-medium">Postulantes</p>
            <p class="text-2xl font-bold mt-1">{{ stats.postulantes ?? '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-purple-50 rounded-lg flex items-center justify-center text-purple-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 font-medium">Aceptados</p>
            <p class="text-2xl font-bold mt-1 text-emerald-600">{{ stats.aceptados ?? '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-emerald-50 rounded-lg flex items-center justify-center text-emerald-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 font-medium">Rechazados</p>
            <p class="text-2xl font-bold mt-1 text-red-600">{{ stats.rechazados ?? '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-red-50 rounded-lg flex items-center justify-center text-red-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-xl border border-gray-200 p-5">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-semibold text-gray-800">Tus vacantes</h3>
        <router-link to="/empresa/vacantes" class="text-sm font-medium text-slate-700 hover:text-slate-900 transition-colors">Ver todas</router-link>
      </div>
      <div v-if="stats.vacantes_lista && stats.vacantes_lista.length > 0">
        <div v-for="v in stats.vacantes_lista.slice(0, 5)" :key="v.id" class="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
          <div>
            <p class="text-sm font-medium text-gray-800">{{ v.titulo }}</p>
            <p class="text-xs text-gray-400 mt-0.5">{{ v.postulantes_count || 0 }} postulantes</p>
          </div>
          <span :class="v.status === 'abierta' ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-600'" class="text-xs font-medium px-2 py-0.5 rounded-full">{{ v.status }}</span>
        </div>
      </div>
      <div v-else class="text-sm text-gray-400 py-6 text-center">
        No tienes vacantes registradas.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import client from '../../api/client'

const stats = ref({})

onMounted(async () => {
  const { data } = await client.get('/empresa/dashboard')
  stats.value = data
})
</script>
