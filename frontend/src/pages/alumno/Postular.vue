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
        <p class="text-sm text-gray-500 mt-1">Completa los datos para enviar tu solicitud</p>
      </div>

      <form @submit.prevent="submit" enctype="multipart/form-data" class="space-y-4">
        <div v-if="errorMsg" class="p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">{{ errorMsg }}</div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Carta de presentación (PDF)</label>
          <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-slate-400 transition-colors cursor-pointer" @click="fileInput?.click()">
            <div class="text-center">
              <svg class="mx-auto h-10 w-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/></svg>
              <p class="mt-2 text-sm text-gray-500">
                <span class="font-medium text-slate-700">Haz clic para subir</span> o arrastra un archivo
              </p>
              <p class="text-xs text-gray-400 mt-1">PDF hasta 5 MB</p>
              <p v-if="selectedFile" class="text-xs text-emerald-600 font-medium mt-2">{{ selectedFile.name }}</p>
            </div>
            <input ref="fileInput" type="file" accept=".pdf" class="hidden" @change="onFileChange" />
          </div>
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
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import client from '../../api/client'

const route = useRoute()
const vacanteId = route.params.id
const selectedFile = ref(null)
const fileInput = ref(null)
const loading = ref(false)
const errorMsg = ref('')
const result = ref(null)

function onFileChange(e) {
  selectedFile.value = e.target.files[0] || null
}

async function submit() {
  if (!selectedFile.value) {
    errorMsg.value = 'Debes seleccionar un archivo PDF.'
    return
  }
  loading.value = true
  errorMsg.value = ''
  const formData = new FormData()
  formData.append('archivo', selectedFile.value)
  try {
    const { data } = await client.post(`/alumno/vacantes/${vacanteId}/postular`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    result.value = data
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Error al enviar postulación.'
  } finally {
    loading.value = false
  }
}
</script>
