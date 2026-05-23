<template>
  <div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 font-medium">Carreras</p>
            <p class="text-2xl font-bold mt-1">{{ stats.carreras ?? '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center text-blue-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 font-medium">Alumnos</p>
            <p class="text-2xl font-bold mt-1">{{ stats.alumnos ?? '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-emerald-50 rounded-lg flex items-center justify-center text-emerald-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 font-medium">Empresas</p>
            <p class="text-2xl font-bold mt-1">{{ stats.empresas ?? '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-amber-50 rounded-lg flex items-center justify-center text-amber-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 font-medium">Solicitudes</p>
            <p class="text-2xl font-bold mt-1">{{ stats.solicitudes ?? '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-purple-50 rounded-lg flex items-center justify-center text-purple-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-xl border border-gray-200 p-6">
      <h3 class="font-semibold text-gray-800 mb-4">Accesos directos</h3>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <router-link to="/admin/carreras" class="flex items-center gap-3 p-3 rounded-lg bg-gray-50 hover:bg-blue-50 transition-colors text-sm font-medium text-gray-700 hover:text-blue-700">
          <span class="w-8 h-8 rounded-lg bg-blue-100 text-blue-600 flex items-center justify-center">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/></svg>
          </span>
          Gestionar carreras
        </router-link>
        <router-link to="/admin/alumnos" class="flex items-center gap-3 p-3 rounded-lg bg-gray-50 hover:bg-emerald-50 transition-colors text-sm font-medium text-gray-700 hover:text-emerald-700">
          <span class="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-600 flex items-center justify-center">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/></svg>
          </span>
          Gestionar alumnos
        </router-link>
        <router-link to="/admin/empresas" class="flex items-center gap-3 p-3 rounded-lg bg-gray-50 hover:bg-amber-50 transition-colors text-sm font-medium text-gray-700 hover:text-amber-700">
          <span class="w-8 h-8 rounded-lg bg-amber-100 text-amber-600 flex items-center justify-center">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/></svg>
          </span>
          Gestionar empresas
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import client from '../../api/client'

const stats = ref({})

onMounted(async () => {
  const { data } = await client.get('/admin/stats')
  stats.value = data
})
</script>
