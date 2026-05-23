<template>
  <div>
    <div class="mb-6">
      <p class="text-sm text-gray-500">Vacantes disponibles para servicio social</p>
    </div>

    <div v-if="loading" class="text-center py-12 text-gray-400">
      <svg class="animate-spin h-8 w-8 mx-auto mb-3" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
      </svg>
      Cargando vacantes...
    </div>

    <div v-else-if="items.length === 0" class="text-center py-12 text-gray-400">
      No hay vacantes disponibles en este momento.
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="item in items" :key="item.id" class="bg-white rounded-xl border border-gray-200 hover:shadow-md transition-shadow p-5 flex flex-col">
        <div class="flex items-start justify-between mb-3">
          <h3 class="font-semibold text-gray-800">{{ item.titulo }}</h3>
          <span :class="statusClass(item.status)" class="text-xs font-medium px-2 py-0.5 rounded-full shrink-0 ml-2">{{ item.status }}</span>
        </div>
        <p class="text-sm text-gray-500 mb-3 flex-1">{{ item.descripcion?.substring(0, 120) }}{{ item.descripcion?.length > 120 ? '...' : '' }}</p>
        <div class="space-y-1.5 text-xs text-gray-400 mb-4">
          <div class="flex items-center gap-2">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
            {{ item.empresa_nombre || item.empresa?.nombre || 'Empresa' }}
          </div>
          <div class="flex items-center gap-2">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            {{ item.ubicacion || 'No especificada' }}
          </div>
        </div>
        <router-link :to="`/alumno/vacantes/${item.id}`" class="w-full text-center py-2 bg-slate-900 text-white rounded-lg text-sm font-medium hover:bg-slate-800 transition-colors">
          Ver detalle
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import client from '../../api/client'

const items = ref([])
const loading = ref(true)

onMounted(async () => {
  const { data } = await client.get('/alumno/vacantes')
  items.value = data
  loading.value = false
})

function statusClass(status) {
  if (!status) return 'bg-gray-100 text-gray-600'
  const s = status.toLowerCase()
  if (s === 'abierta' || s === 'activa' || s === 'open') return 'bg-emerald-100 text-emerald-700'
  if (s === 'cerrada' || s === 'closed') return 'bg-red-100 text-red-700'
  if (s === 'pausada' || s === 'paused') return 'bg-amber-100 text-amber-700'
  return 'bg-gray-100 text-gray-600'
}
</script>
