<template>
  <div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 font-medium">Vacantes abiertas</p>
            <p class="text-2xl font-bold mt-1">{{ stats.vacantes_abiertas ?? '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center text-blue-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 font-medium">Mis postulaciones</p>
            <p class="text-2xl font-bold mt-1">{{ stats.mis_postulaciones ?? '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-emerald-50 rounded-lg flex items-center justify-center text-emerald-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 font-medium">Aceptadas</p>
            <p class="text-2xl font-bold mt-1 text-emerald-600">{{ stats.aceptadas ?? '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-emerald-50 rounded-lg flex items-center justify-center text-emerald-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-500 font-medium">Rechazadas</p>
            <p class="text-2xl font-bold mt-1 text-red-600">{{ stats.rechazadas ?? '-' }}</p>
          </div>
          <div class="w-10 h-10 bg-red-50 rounded-lg flex items-center justify-center text-red-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <h3 class="font-semibold text-gray-800 mb-4">Postulaciones pendientes</h3>
        <div v-if="pending.length === 0" class="text-sm text-gray-400 py-8 text-center">
          No tienes postulaciones pendientes.
        </div>
        <div v-for="p in pending" :key="p.id" class="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
          <div>
            <p class="text-sm font-medium text-gray-800">{{ p.vacante_titulo || 'Vacante' }}</p>
            <p class="text-xs text-gray-400 mt-0.5">{{ p.status }} · {{ p.created_at ? new Date(p.created_at).toLocaleDateString() : '' }}</p>
          </div>
          <span v-if="p.codigo_confirmacion" class="text-xs font-mono bg-amber-50 text-amber-700 px-2 py-1 rounded-md border border-amber-200">
            Código: {{ p.codigo_confirmacion }}
          </span>
        </div>
      </div>

      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <h3 class="font-semibold text-gray-800 mb-4">Asignaciones confirmadas</h3>
        <div v-if="confirmed.length === 0" class="text-sm text-gray-400 py-8 text-center">
          No tienes asignaciones confirmadas.
        </div>
        <div v-for="p in confirmed" :key="p.id" class="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
          <div>
            <p class="text-sm font-medium text-gray-800">{{ p.vacante_titulo || 'Vacante' }}</p>
            <p class="text-xs text-gray-400 mt-0.5">Confirmado</p>
          </div>
          <span class="text-xs font-mono bg-emerald-50 text-emerald-700 px-2 py-1 rounded-md border border-emerald-200">
            {{ p.codigo_confirmacion }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import client from '../../api/client'

const stats = ref({})
const pending = ref([])
const confirmed = ref([])

onMounted(async () => {
  const { data } = await client.get('/alumno/dashboard')
  stats.value = data
  pending.value = data.postulaciones_pendientes || []
  confirmed.value = data.asignaciones_confirmadas || []
})
</script>
