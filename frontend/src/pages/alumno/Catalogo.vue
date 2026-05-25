<template>
  <div>
    <div class="mb-6">
      <p class="text-sm text-gray-500">Tus postulaciones y asignaciones</p>
    </div>

    <div v-if="loading" class="text-center py-12 text-gray-400">
      <svg class="animate-spin h-8 w-8 mx-auto mb-3" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
      Cargando...
    </div>

    <div v-else class="space-y-6">
      <!-- Pending -->
      <div v-if="data.pendientes && data.pendientes.length > 0" class="bg-white rounded-xl border border-gray-200 p-5">
        <h3 class="font-semibold text-gray-800 mb-4">Postulaciones pendientes</h3>
        <div v-for="p in data.pendientes" :key="p.id" class="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
          <div>
            <p class="text-sm font-medium text-gray-800">{{ p.vacante_titulo || 'Vacante' }}</p>
            <p class="text-xs text-gray-400 mt-0.5">{{ p.empresa_nombre }}</p>
          </div>
          <span class="text-xs text-amber-700 bg-amber-100 px-2 py-0.5 rounded-full">Pendiente</span>
        </div>
        <div v-if="data.pendientes.length === 0" class="text-sm text-gray-400 py-4 text-center">No tienes postulaciones pendientes.</div>
      </div>

      <!-- Offers to confirm -->
      <div v-if="data.por_confirmar && data.por_confirmar.length > 0" class="bg-white rounded-xl border border-gray-200 p-5">
        <h3 class="font-semibold text-gray-800 mb-4">Ofertas por confirmar</h3>
        <div v-for="p in data.por_confirmar" :key="p.id" class="py-3 border-b border-gray-100 last:border-0">
          <div class="flex items-center justify-between mb-2">
            <div>
              <p class="text-sm font-medium text-gray-800">{{ p.vacante_titulo || 'Vacante' }}</p>
              <p class="text-xs text-gray-400">{{ p.empresa_nombre }}</p>
            </div>
            <span class="text-xs text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-full">Aceptado</span>
          </div>
          <p v-if="p.fecha_limite" class="text-xs text-gray-400 mb-2">Vence: {{ new Date(p.fecha_limite).toLocaleDateString() }}</p>
          <div class="flex gap-2">
            <input v-model="confirmCodes[p.id]" placeholder="Código de confirmación" class="flex-1 px-3 py-1.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent font-mono" />
            <button @click="doConfirm(p)" class="px-3 py-1.5 bg-slate-900 text-white rounded-lg text-sm font-medium hover:bg-slate-800 transition-colors shrink-0">Confirmar</button>
          </div>
        </div>
      </div>

      <!-- Confirmed assignment -->
      <div v-if="data.confirmada" class="bg-white rounded-xl border border-emerald-200 p-5">
        <div class="flex items-center gap-3 mb-1">
          <div class="w-10 h-10 bg-emerald-50 rounded-lg flex items-center justify-center text-emerald-600 shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <div>
            <p class="text-sm text-gray-500 font-medium">Asignación confirmada</p>
            <p class="text-lg font-bold text-gray-900">{{ data.confirmada.vacante_titulo }}</p>
          </div>
        </div>
        <p class="text-sm text-gray-500 mt-2 ml-13">{{ data.confirmada.empresa_nombre }}</p>
        <p class="text-xs font-mono text-gray-400 mt-1 ml-13">Código: {{ data.confirmada.codigo_confirmacion }}</p>
      </div>

      <!-- Cancelled -->
      <div v-if="data.cancelada" class="bg-white rounded-xl border border-red-200 p-5">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-red-50 rounded-lg flex items-center justify-center text-red-600 shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
          </div>
          <div>
            <p class="text-sm text-red-600 font-medium">Cancelado</p>
            <p class="text-sm text-gray-600">{{ data.cancelada.vacante_titulo }} — {{ data.cancelada.empresa_nombre }}</p>
          </div>
        </div>
      </div>

      <!-- Rejected -->
      <div v-if="data.rechazadas && data.rechazadas.length > 0" class="bg-white rounded-xl border border-gray-200 p-5">
        <h3 class="font-semibold text-gray-800 mb-4">Postulaciones rechazadas</h3>
        <div v-for="r in data.rechazadas" :key="r.id" class="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
          <div>
            <p class="text-sm font-medium text-gray-800">{{ r.vacante_titulo || 'Vacante' }}</p>
            <p class="text-xs text-gray-400 mt-0.5">{{ r.empresa_nombre }}</p>
          </div>
          <span class="text-xs text-red-700 bg-red-100 px-2 py-0.5 rounded-full">Rechazado</span>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="!data.pendientes?.length && !data.por_confirmar?.length && !data.confirmada && !data.cancelada && !data.rechazadas?.length" class="text-center py-12 text-gray-400">
        <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        <p>No tienes postulaciones aún.</p>
        <router-link to="/alumno/dashboard" class="text-sm text-blue-600 hover:underline mt-2 inline-block">Ver vacantes disponibles</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import client from '../../api/client'

const data = ref({})
const loading = ref(true)
const confirmCodes = reactive({})

onMounted(async () => {
  const { data: res } = await client.get('/alumno/vacantes')
  data.value = res
  if (res.por_confirmar) {
    res.por_confirmar.forEach(o => { confirmCodes[o.id] = '' })
  }
  loading.value = false
})

async function doConfirm(p) {
  const code = confirmCodes[p.id]
  if (!code) return
  try {
    await client.post(`/alumno/solicitudes/${p.id}/confirmar`, { codigo_confirmacion: code })
    const { data: res } = await client.get('/alumno/vacantes')
    data.value = res
  } catch (e) {
    const detail = e.response?.data?.detail
    alert(typeof detail === 'string' ? detail : 'Error al confirmar')
  }
}
</script>
