<template>
  <div class="max-w-lg">
    <router-link :to="`/alumno/vacantes/${vacanteId}`" class="inline-flex items-center gap-1.5 text-sm text-gray-500 hover:text-gray-800 mb-6 transition-colors">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
      Volver al detalle
    </router-link>

    <div class="bg-white rounded-xl border border-gray-200 p-6">
      <div class="text-center mb-6">
        <div class="w-14 h-14 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900">Postular a vacante</h2>
        <p class="text-sm text-gray-500 mt-1">Sube los 3 documentos en PDF para enviar tu solicitud</p>
      </div>

      <form @submit.prevent="submit" enctype="multipart/form-data" class="space-y-4">
        <div v-if="errorMsg" class="p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{{ errorMsg }}</div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">CV (PDF)</label>
          <input type="file" accept=".pdf" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" @change="e => files.cv = e.target.files[0]" required />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Carta de presentación (PDF)</label>
          <input type="file" accept=".pdf" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" @change="e => files.carta = e.target.files[0]" required />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Historial académico (PDF)</label>
          <input type="file" accept=".pdf" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" @change="e => files.historial = e.target.files[0]" required />
        </div>

        <button type="submit" :disabled="loading" class="w-full py-2.5 px-4 bg-slate-900 text-white rounded-lg text-sm font-semibold hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2">
          <svg v-if="loading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
          </svg>
          {{ loading ? 'Enviando...' : 'Enviar postulación' }}
        </button>
      </form>

      <div v-if="result" class="mt-6 p-4 bg-emerald-50 border border-emerald-200 rounded-lg text-center">
        <div class="w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-3">
          <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        </div>
        <h3 class="font-semibold text-emerald-800 mb-1">¡Postulación exitosa!</h3>
        <p class="text-sm text-emerald-700 mb-3">Tu código de confirmación es:</p>
        <p class="text-2xl font-mono font-bold text-emerald-900 tracking-widest bg-white rounded-lg py-2 px-4 inline-block border border-emerald-200">{{ result.codigo_confirmacion }}</p>
        <p class="text-xs text-emerald-600 mt-3">Guarda este código para dar seguimiento a tu solicitud.</p>
        <router-link to="/alumno/dashboard" class="mt-4 inline-block text-sm font-medium text-emerald-700 hover:text-emerald-800 underline">Ir al dashboard</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRoute } from 'vue-router'
import client from '../../api/client'

const route = useRoute()
const vacanteId = route.params.id
const files = reactive({ cv: null, carta: null, historial: null })
const loading = ref(false)
const errorMsg = ref('')
const result = ref(null)

async function submit() {
  if (!files.cv || !files.carta || !files.historial) {
    errorMsg.value = 'Debes subir los 3 documentos en PDF.'
    return
  }
  for (const key of ['cv', 'carta', 'historial']) {
    if (files[key].type !== 'application/pdf') {
      errorMsg.value = 'Todos los archivos deben ser PDF.'
      return
    }
  }
  loading.value = true
  errorMsg.value = ''
  const formData = new FormData()
  formData.append('vacante_id', vacanteId)
  formData.append('cv', files.cv)
  formData.append('carta', files.carta)
  formData.append('historial', files.historial)
  try {
    const { data } = await client.post('/alumno/solicitudes', formData)
    result.value = data
  } catch (e) {
    const detail = e.response?.data?.detail
    if (Array.isArray(detail)) {
      errorMsg.value = detail.map(d => d.msg || JSON.stringify(d)).join(', ')
    } else if (typeof detail === 'string') {
      errorMsg.value = detail
    } else {
      errorMsg.value = 'Error al enviar postulación'
    }
  } finally {
    loading.value = false
  }
}
</script>
