<template>
  <div>
    <!-- Service completed -->
    <div v-if="stats.servicio_completado" class="bg-white rounded-xl border border-gray-200 p-6 text-center">
      <div class="w-14 h-14 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-7 h-7 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
      </div>
      <p class="text-xl font-bold text-emerald-700">Servicio social completado</p>
      <p class="text-sm text-gray-500 mt-2">Has completado tu servicio social exitosamente.</p>
    </div>

    <!-- Has confirmed assignment -->
    <div v-else-if="misPost.confirmada" class="space-y-6">
      <div class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-center gap-3 mb-1">
          <div class="w-10 h-10 bg-emerald-50 rounded-lg flex items-center justify-center text-emerald-600 shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <div>
            <p class="text-sm text-gray-500 font-medium">Asignación actual</p>
            <p class="text-lg font-bold text-gray-900">{{ misPost.confirmada.vacante_titulo }}</p>
          </div>
        </div>
        <p class="text-sm text-gray-500 mt-2 ml-13">{{ misPost.confirmada.empresa_nombre }}</p>
        <p class="text-xs text-gray-400 mt-1 ml-13">Código: {{ misPost.confirmada.codigo_confirmacion }}</p>
      </div>
    </div>

    <!-- Service cancelled -->
    <div v-else-if="stats.servicio_cancelado" class="space-y-6">
      <div class="bg-white rounded-xl border border-red-200 p-5">
        <div class="flex items-center gap-3 mb-1">
          <div class="w-10 h-10 bg-red-50 rounded-lg flex items-center justify-center text-red-600 shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
          </div>
          <div>
            <p class="text-sm text-red-600 font-medium">Servicio social cancelado</p>
            <p class="text-sm text-gray-600 mt-0.5">Tu servicio social en <strong>{{ misPost.cancelada?.vacante_titulo }}</strong> fue cancelado por la empresa.</p>
          </div>
        </div>
      </div>

      <div v-if="stats.vacantes_disponibles && stats.vacantes_disponibles.length > 0">
        <h3 class="font-semibold text-gray-800 mb-4">Vacantes disponibles</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="item in stats.vacantes_disponibles" :key="item.id" class="bg-white rounded-xl border border-gray-200 p-5 flex flex-col hover:shadow-md transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h3 class="font-semibold text-gray-800">{{ item.titulo }}</h3>
              <span class="bg-emerald-100 text-emerald-700 text-xs font-medium px-2 py-0.5 rounded-full shrink-0 ml-2">{{ item.status }}</span>
            </div>
            <p class="text-sm text-gray-500 mb-3 flex-1">{{ item.descripcion?.substring(0, 120) }}{{ item.descripcion?.length > 120 ? '...' : '' }}</p>
            <div class="space-y-1.5 text-xs text-gray-400 mb-4">
              <div class="flex items-center gap-2">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
                {{ item.empresa_nombre || 'Empresa' }}
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
      <div v-else class="text-center py-12 text-gray-400">
        No hay vacantes disponibles en este momento.
      </div>
    </div>

    <!-- Default: browsing + postulations -->
    <div v-else class="space-y-8">
      <div v-if="stats.vacantes_disponibles && stats.vacantes_disponibles.length > 0">
        <h3 class="font-semibold text-gray-800 mb-4">Vacantes disponibles</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="item in stats.vacantes_disponibles" :key="item.id" class="bg-white rounded-xl border border-gray-200 p-5 flex flex-col hover:shadow-md transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h3 class="font-semibold text-gray-800">{{ item.titulo }}</h3>
              <span class="bg-emerald-100 text-emerald-700 text-xs font-medium px-2 py-0.5 rounded-full shrink-0 ml-2">{{ item.status }}</span>
            </div>
            <p class="text-sm text-gray-500 mb-3 flex-1">{{ item.descripcion?.substring(0, 120) }}{{ item.descripcion?.length > 120 ? '...' : '' }}</p>
            <div class="space-y-1.5 text-xs text-gray-400 mb-4">
              <div class="flex items-center gap-2">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
                {{ item.empresa_nombre || 'Empresa' }}
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
      <div v-else class="text-center py-12 text-gray-400">
        No hay vacantes disponibles en este momento.
      </div>

      <!-- Pending postulations -->
      <div v-if="misPost.pendientes && misPost.pendientes.length > 0" class="bg-white rounded-xl border border-gray-200 p-5">
        <h3 class="font-semibold text-gray-800 mb-4">Postulaciones pendientes</h3>
        <div v-for="p in misPost.pendientes" :key="p.id" class="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
          <div>
            <p class="text-sm font-medium text-gray-800">{{ p.vacante_titulo || 'Vacante' }}</p>
            <p class="text-xs text-gray-400 mt-0.5">{{ p.empresa_nombre }}</p>
          </div>
          <span class="text-xs text-amber-700 bg-amber-100 px-2 py-0.5 rounded-full">Pendiente</span>
        </div>
      </div>

      <!-- Rejected -->
      <div v-if="misPost.rechazadas && misPost.rechazadas.length > 0" class="bg-white rounded-xl border border-gray-200 p-5">
        <h3 class="font-semibold text-gray-800 mb-4">Postulaciones rechazadas</h3>
        <div v-for="r in misPost.rechazadas" :key="r.id" class="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
          <div>
            <p class="text-sm font-medium text-gray-800">{{ r.vacante_titulo || 'Vacante' }}</p>
            <p class="text-xs text-gray-400 mt-0.5">{{ r.empresa_nombre }}</p>
          </div>
          <span class="text-xs text-red-700 bg-red-100 px-2 py-0.5 rounded-full">Rechazado</span>
        </div>
      </div>

      <!-- Offers to confirm -->
      <div v-if="misPost.por_confirmar && misPost.por_confirmar.length > 0" class="bg-white rounded-xl border border-gray-200 p-5">
        <h3 class="font-semibold text-gray-800 mb-4">Ofertas por confirmar</h3>
        <div v-for="p in misPost.por_confirmar" :key="p.id" class="py-3 border-b border-gray-100 last:border-0">
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
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import client from '../../api/client'

const stats = ref({})
const misPost = ref({ pendientes: [], por_confirmar: [], confirmada: null, cancelada: null, rechazadas: [] })
const confirmCodes = reactive({})

onMounted(async () => {
  const { data } = await client.get('/alumno/dashboard')
  stats.value = data
    misPost.value = data.mis_postulaciones || { pendientes: [], por_confirmar: [], confirmada: null, cancelada: null, rechazadas: [] }
  if (misPost.value.por_confirmar) {
    misPost.value.por_confirmar.forEach(o => { confirmCodes[o.id] = '' })
  }
})

async function doConfirm(p) {
  const code = confirmCodes[p.id]
  if (!code) return
  try {
    await client.post(`/alumno/solicitudes/${p.id}/confirmar`, { codigo_confirmacion: code })
    const { data } = await client.get('/alumno/dashboard')
    stats.value = data
    misPost.value = data.mis_postulaciones || { pendientes: [], por_confirmar: [], confirmada: null, cancelada: null, rechazadas: [] }
  } catch (e) {
    const detail = e.response?.data?.detail
    alert(typeof detail === 'string' ? detail : 'Error al confirmar')
  }
}
</script>
