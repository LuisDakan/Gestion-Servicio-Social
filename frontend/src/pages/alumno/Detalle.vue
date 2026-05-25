<template>
  <div v-if="item" class="max-w-2xl">
    <router-link to="/alumno/dashboard" class="inline-flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-800 mb-6 transition-colors">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
      Volver al dashboard
    </router-link>

    <div class="bg-white rounded-xl border border-gray-200 p-6">
      <div class="flex items-start justify-between mb-4">
        <h2 class="text-xl font-bold text-gray-900">{{ item.titulo }}</h2>
        <span :class="item.status === 'abierta' ? 'bg-emerald-100 text-emerald-700' : item.status === 'finalizada' ? 'bg-gray-100 text-gray-600' : 'bg-red-100 text-red-700'" class="text-xs font-medium px-2.5 py-1 rounded-full shrink-0 ml-3">{{ item.status }}</span>
      </div>

      <div class="grid grid-cols-2 gap-4 mb-6 pb-6 border-b border-gray-100">
        <div>
          <p class="text-xs text-gray-400 uppercase tracking-wider font-medium">Empresa</p>
          <p class="text-sm font-medium text-gray-800 mt-1">{{ item.empresa_nombre || '-' }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-400 uppercase tracking-wider font-medium">Ubicación</p>
          <p class="text-sm font-medium text-gray-800 mt-1">{{ item.ubicacion || 'No especificada' }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-400 uppercase tracking-wider font-medium">Cupo máximo</p>
          <p class="text-sm font-medium text-gray-800 mt-1">{{ item.cupo_maximo || '-' }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-400 uppercase tracking-wider font-medium">Horario</p>
          <p class="text-sm font-medium text-gray-800 mt-1">{{ item.horario || '-' }}</p>
        </div>
      </div>

      <div class="mb-6">
        <h4 class="text-sm font-semibold text-gray-800 mb-2">Descripción</h4>
        <p class="text-sm text-gray-600 leading-relaxed">{{ item.descripcion || 'Sin descripción' }}</p>
      </div>

      <div v-if="item.requisitos" class="mb-6">
        <h4 class="text-sm font-semibold text-gray-800 mb-2">Requisitos</h4>
        <p class="text-sm text-gray-600 leading-relaxed">{{ item.requisitos }}</p>
      </div>

      <div class="mt-8 pt-6 border-t border-gray-100 flex gap-3">
        <div v-if="item.ha_aplicado" :class="item.status_aplicacion === 'aceptado' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : item.status_aplicacion === 'cancelado' ? 'bg-gray-100 text-gray-600 border-gray-200' : 'bg-amber-50 text-amber-700 border-amber-200'" class="px-6 py-2.5 rounded-lg text-sm font-medium border">
          Ya aplicaste · {{ item.status_aplicacion }}
        </div>
        <div v-else-if="item.status !== 'abierta'" class="px-6 py-2.5 text-gray-500 bg-gray-50 rounded-lg text-sm font-medium border border-gray-200">
          {{ item.status === 'finalizada' ? 'Vacante finalizada' : 'Vacante cerrada' }}
        </div>
        <router-link v-else :to="`/alumno/vacantes/${item.id}/postular`" class="px-6 py-2.5 bg-slate-900 text-white rounded-lg text-sm font-medium hover:bg-slate-800 transition-colors">
          Postularme
        </router-link>
        <router-link to="/alumno/dashboard" class="px-6 py-2.5 border border-gray-300 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">
          Cancelar
        </router-link>
      </div>
    </div>
  </div>

  <div v-else class="text-center py-12 text-gray-400">
    <svg class="animate-spin h-8 w-8 mx-auto mb-3" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
    </svg>
    Cargando...
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import client from '../../api/client'

const route = useRoute()
const item = ref(null)

onMounted(async () => {
  const { data } = await client.get(`/alumno/vacantes/${route.params.id}`)
  item.value = data
})
</script>
