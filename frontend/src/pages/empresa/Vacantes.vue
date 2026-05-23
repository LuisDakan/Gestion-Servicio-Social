<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <p class="text-sm text-gray-500">Total: {{ items.length }} vacantes</p>
      <button @click="openCreate" class="px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-medium hover:bg-slate-800 transition-colors flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        Nueva vacante
      </button>
    </div>

    <div v-if="loading" class="text-center py-12 text-gray-400">
      <svg class="animate-spin h-8 w-8 mx-auto mb-3" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
      </svg>
      Cargando vacantes...
    </div>

    <div v-else class="space-y-4">
      <div v-for="item in items" :key="item.id" class="bg-white rounded-xl border border-gray-200 p-5">
        <div class="flex items-start justify-between mb-3">
          <div class="flex-1">
            <div class="flex items-center gap-3">
              <h3 class="font-semibold text-gray-800">{{ item.titulo }}</h3>
              <span :class="statusClass(item.status)" class="text-xs font-medium px-2 py-0.5 rounded-full">{{ item.status }}</span>
            </div>
            <p class="text-sm text-gray-500 mt-1">{{ item.descripcion?.substring(0, 150) }}{{ item.descripcion?.length > 150 ? '...' : '' }}</p>
          </div>
          <div class="flex items-center gap-2 ml-4 shrink-0">
            <button @click="openPostulantes(item)" class="px-3 py-1.5 text-xs font-medium bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors flex items-center gap-1">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              Postulantes ({{ item.postulantes_count || 0 }})
            </button>
            <button @click="openEdit(item)" class="p-1.5 text-gray-400 hover:text-blue-600 transition-colors" title="Editar">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            </button>
            <button @click="confirmDelete(item)" class="p-1.5 text-gray-400 hover:text-red-600 transition-colors" title="Eliminar">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            </button>
          </div>
        </div>
        <div class="flex flex-wrap gap-4 text-xs text-gray-400">
          <span>{{ item.ubicacion || 'Sin ubicación' }}</span>
          <span>{{ item.duracion || item.duracion_meses ? `Duración: ${item.duracion_meses || item.duracion} meses` : '' }}</span>
          <span>{{ item.horario || '' }}</span>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50" @click.self="showModal = false">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-lg mx-4 p-6">
        <h3 class="text-lg font-semibold mb-4">{{ editing ? 'Editar vacante' : 'Nueva vacante' }}</h3>
        <form @submit.prevent="save">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Título</label>
              <input v-model="form.titulo" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
              <textarea v-model="form.descripcion" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" required></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Ubicación</label>
                <input v-model="form.ubicacion" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Duración (meses)</label>
                <input v-model.number="form.duracion_meses" type="number" min="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" />
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Horario</label>
                <input v-model="form.horario" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
                <select v-model="form.status" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent">
                  <option value="abierta">Abierta</option>
                  <option value="cerrada">Cerrada</option>
                </select>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Requisitos</label>
              <textarea v-model="form.requisitos" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Actividades</label>
              <textarea v-model="form.actividades" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent"></textarea>
            </div>
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button type="button" @click="showModal = false" class="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 transition-colors">Cancelar</button>
            <button type="submit" class="px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-medium hover:bg-slate-800 transition-colors">
              {{ editing ? 'Guardar' : 'Crear' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="deleteTarget" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50" @click.self="deleteTarget = null">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-sm mx-4 p-6 text-center">
        <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
        </div>
        <h3 class="text-lg font-semibold mb-2">Eliminar vacante</h3>
        <p class="text-sm text-gray-500 mb-6">¿Eliminar "{{ deleteTarget.titulo }}"? Esta acción no se puede deshacer.</p>
        <div class="flex justify-center gap-3">
          <button @click="deleteTarget = null" class="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 transition-colors">Cancelar</button>
          <button @click="doDelete" class="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors">Eliminar</button>
        </div>
      </div>
    </div>

    <div v-if="postulantesModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50" @click.self="postulantesModal = false">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-2xl mx-4 p-6 max-h-[80vh] flex flex-col">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">Postulantes — {{ postulantesVacante?.titulo }}</h3>
          <button @click="postulantesModal = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
        <div class="overflow-y-auto flex-1">
          <div v-if="postulantes.length === 0" class="text-center py-8 text-gray-400 text-sm">
            No hay postulantes para esta vacante.
          </div>
          <div v-for="p in postulantes" :key="p.id" class="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
            <div>
              <p class="text-sm font-medium text-gray-800">{{ p.alumno_nombre || p.alumno?.nombre || 'Alumno' }}</p>
              <p class="text-xs text-gray-400 mt-0.5">
                {{ p.alumno_carrera || p.alumno?.carrera?.nombre || '' }}
                <span v-if="p.created_at"> · {{ new Date(p.created_at).toLocaleDateString() }}</span>
              </p>
              <a v-if="p.archivo_url" :href="p.archivo_url" target="_blank" class="text-xs text-blue-600 hover:underline mt-1 inline-block">Ver carta</a>
            </div>
            <div class="flex items-center gap-2">
              <span :class="p.status === 'aceptada' ? 'bg-emerald-100 text-emerald-700' : p.status === 'rechazada' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'" class="text-xs font-medium px-2 py-0.5 rounded-full">{{ p.status }}</span>
              <button v-if="p.status === 'pendiente'" @click="aceptar(p)" class="px-3 py-1 text-xs font-medium bg-emerald-50 text-emerald-700 rounded-lg hover:bg-emerald-100 transition-colors">Aceptar</button>
              <button v-if="p.status === 'pendiente'" @click="rechazar(p)" class="px-3 py-1 text-xs font-medium bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors">Rechazar</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, onMounted } from 'vue'
import client from '../../api/client'

const flash = inject('flash')
const error = inject('error')
const items = ref([])
const loading = ref(true)
const showModal = ref(false)
const editing = ref(false)
const deleteTarget = ref(null)
const postulantesModal = ref(false)
const postulantes = ref([])
const postulantesVacante = ref(null)
const form = ref({ titulo: '', descripcion: '', ubicacion: '', duracion_meses: null, horario: '', status: 'abierta', requisitos: '', actividades: '' })

onMounted(async () => {
  const { data } = await client.get('/empresa/vacantes')
  items.value = data
  loading.value = false
})

function openCreate() {
  editing.value = false
  form.value = { titulo: '', descripcion: '', ubicacion: '', duracion_meses: null, horario: '', status: 'abierta', requisitos: '', actividades: '' }
  showModal.value = true
}

function openEdit(item) {
  editing.value = true
  form.value = { ...item }
  showModal.value = true
}

async function save() {
  try {
    if (editing.value) {
      const { data } = await client.put(`/empresa/vacantes/${form.value.id}`, form.value)
      Object.assign(items.value.find(i => i.id === form.value.id), data)
      flash.value = 'Vacante actualizada correctamente'
    } else {
      const { data } = await client.post('/empresa/vacantes', form.value)
      items.value.push(data)
      flash.value = 'Vacante creada correctamente'
    }
    showModal.value = false
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al guardar'
  }
}

function confirmDelete(item) {
  deleteTarget.value = item
}

async function doDelete() {
  try {
    await client.delete(`/empresa/vacantes/${deleteTarget.value.id}`)
    items.value = items.value.filter(i => i.id !== deleteTarget.value.id)
    flash.value = 'Vacante eliminada correctamente'
    deleteTarget.value = null
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al eliminar'
  }
}

async function openPostulantes(item) {
  postulantesVacante.value = item
  const { data } = await client.get(`/empresa/vacantes/${item.id}/postulantes`)
  postulantes.value = data
  postulantesModal.value = true
}

async function aceptar(p) {
  await client.put(`/empresa/postulantes/${p.id}/aceptar`)
  p.status = 'aceptada'
  flash.value = 'Postulante aceptado'
}

async function rechazar(p) {
  await client.put(`/empresa/postulantes/${p.id}/rechazar`)
  p.status = 'rechazada'
  flash.value = 'Postulante rechazado'
}

function statusClass(status) {
  if (!status) return 'bg-gray-100 text-gray-600'
  const s = status.toLowerCase()
  if (s === 'abierta' || s === 'activa' || s === 'open') return 'bg-emerald-100 text-emerald-700'
  if (s === 'cerrada' || s === 'closed') return 'bg-red-100 text-red-700'
  return 'bg-gray-100 text-gray-600'
}
</script>
