<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <p class="text-sm text-gray-500">Total: {{ items.length }} vacantes</p>
      <button @click="openCreate" class="px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-medium hover:bg-slate-800 transition-colors flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        Nueva vacante
      </button>
    </div>

    <div v-if="errors.length" class="mb-4 p-4 rounded-lg bg-red-50 border border-red-200 text-red-800 text-sm">
      <div class="font-medium mb-1">Se encontraron los siguientes errores:</div>
      <ul class="list-disc list-inside space-y-0.5">
        <li v-for="(err, i) in errors" :key="i">{{ err }}</li>
      </ul>
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
              <span :class="item.status === 'abierta' ? 'bg-emerald-100 text-emerald-700' : item.status === 'finalizada' ? 'bg-gray-100 text-gray-600' : 'bg-red-100 text-red-700'" class="text-xs font-medium px-2 py-0.5 rounded-full">{{ item.status }}</span>
            </div>
            <p class="text-sm text-gray-500 mt-1">{{ item.descripcion?.substring(0, 150) }}{{ item.descripcion?.length > 150 ? '...' : '' }}</p>
          </div>
          <div class="flex items-center gap-2 ml-4 shrink-0">
            <button @click="openPostulantes(item)" class="px-3 py-1.5 text-xs font-medium bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors flex items-center gap-1">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              Postulantes ({{ item.solicitudes_count || 0 }})
            </button>
            <button v-if="!item.finalizada && item.status !== 'finalizada'" @click="doFinalizar(item)" class="px-3 py-1.5 text-xs font-medium bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors flex items-center gap-1" title="Marcar como finalizada">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
              Finalizar
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
          <span>Cupo: {{ item.cupo_maximo }}</span>
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
                <input v-model="form.ubicacion" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" required />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Horario</label>
                <input v-model="form.horario" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" required />
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Cupo máximo</label>
                <input v-model.number="form.cupo_maximo" type="number" min="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" required />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Límite registros</label>
                <input v-model.number="form.limite_registros" type="number" min="1" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" required />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Requisitos</label>
              <textarea v-model="form.requisitos" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" required></textarea>
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
          <div v-for="p in postulantes" :key="p.id" class="py-3 border-b border-gray-100 last:border-0">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-800">{{ p.alumno_nombre || 'Alumno' }}</p>
                <p class="text-xs text-gray-400 mt-0.5">{{ p.alumno_carrera || '' }}</p>
              </div>
              <div class="flex items-center gap-2">
                <span :class="p.estatus === 'aceptado' ? 'bg-emerald-100 text-emerald-700' : p.estatus === 'rechazado' ? 'bg-red-100 text-red-700' : p.estatus === 'cancelado' ? 'bg-gray-100 text-gray-600' : 'bg-amber-100 text-amber-700'" class="text-xs font-medium px-2 py-0.5 rounded-full">{{ p.estatus }}</span>
                <button v-if="p.estatus === 'pendiente'" @click="aceptar(p)" class="px-3 py-1 text-xs font-medium bg-emerald-50 text-emerald-700 rounded-lg hover:bg-emerald-100 transition-colors">Aceptar</button>
                <button v-if="p.estatus === 'pendiente'" @click="rechazar(p)" class="px-3 py-1 text-xs font-medium bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors">Rechazar</button>
                <button v-if="p.estatus === 'aceptado' && p.confirmada" @click="cancelar(p)" class="px-3 py-1 text-xs font-medium bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors">Cancelar</button>
              </div>
            </div>
            <div v-if="p.tiene_cv || p.tiene_carta || p.tiene_historial" class="flex gap-3 mt-2 ml-1">
              <button v-if="p.tiene_cv" @click="openPdf(p.id, 'cv')" class="text-xs text-blue-600 hover:underline flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
                CV
              </button>
              <button v-if="p.tiene_carta" @click="openPdf(p.id, 'carta')" class="text-xs text-blue-600 hover:underline flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
                Carta
              </button>
              <button v-if="p.tiene_historial" @click="openPdf(p.id, 'historial')" class="text-xs text-blue-600 hover:underline flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
                Historial
              </button>
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
const editingId = ref(null)
const errors = ref([])
const deleteTarget = ref(null)
const postulantesModal = ref(false)
const postulantes = ref([])
const postulantesVacante = ref(null)
const form = ref({ titulo: '', descripcion: '', ubicacion: '', horario: '', cupo_maximo: null, limite_registros: null, requisitos: '' })

onMounted(async () => {
  try {
    const { data } = await client.get('/empresa/vacantes')
    items.value = data
  } catch (e) {
    errors.value = [e.response?.data?.detail || 'Error al cargar vacantes']
  } finally {
    loading.value = false
  }
})

function openCreate() {
  editing.value = false
  editingId.value = null
  errors.value = []
  form.value = { titulo: '', descripcion: '', ubicacion: '', horario: '', cupo_maximo: null, limite_registros: null, requisitos: '' }
  showModal.value = true
}

function openEdit(item) {
  editing.value = true
  editingId.value = item.id
  errors.value = []
  form.value = {
    titulo: item.titulo,
    descripcion: item.descripcion,
    ubicacion: item.ubicacion,
    horario: item.horario,
    cupo_maximo: item.cupo_maximo,
    limite_registros: item.limite_registros,
    requisitos: item.requisitos,
  }
  showModal.value = true
}

async function save() {
  errors.value = []

  if (!form.value.cupo_maximo || !form.value.limite_registros) {
    errors.value.push('Cupo máximo y límite de registros son requeridos')
    return
  }

  try {
    const payload = {
      titulo: form.value.titulo,
      descripcion: form.value.descripcion,
      ubicacion: form.value.ubicacion,
      horario: form.value.horario,
      cupo_maximo: form.value.cupo_maximo,
      limite_registros: form.value.limite_registros,
      requisitos: form.value.requisitos,
    }
    if (editing.value) {
      const { data } = await client.put(`/empresa/vacantes/${editingId.value}`, payload)
      Object.assign(items.value.find(i => i.id === editingId.value), data)
      flash.value = 'Vacante actualizada correctamente'
    } else {
      const { data } = await client.post('/empresa/vacantes', payload)
      items.value.push(data)
      flash.value = 'Vacante creada correctamente'
    }
    showModal.value = false
  } catch (e) {
    const detail = e.response?.data?.detail
    if (Array.isArray(detail)) {
      errors.value = detail.map(d => d.msg || JSON.stringify(d))
    } else if (typeof detail === 'string') {
      errors.value = [detail]
    } else {
      errors.value = ['Error al guardar']
    }
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
    const detail = e.response?.data?.detail
    if (Array.isArray(detail)) {
      errors.value = detail.map(d => d.msg || JSON.stringify(d))
    } else if (typeof detail === 'string') {
      errors.value = [detail]
    } else {
      errors.value = ['Error al eliminar']
    }
  }
}

async function openPostulantes(item) {
  postulantesVacante.value = item
  const { data } = await client.get(`/empresa/vacantes/${item.id}/postulantes`)
  postulantes.value = data
  postulantesModal.value = true
}

async function aceptar(p) {
  try {
    await client.post(`/empresa/solicitudes/${p.id}/aceptar`)
    p.estatus = 'aceptado'
    flash.value = 'Postulante aceptado'
  } catch (e) {
    const detail = e.response?.data?.detail
    errors.value = [detail || 'Error al aceptar postulante']
  }
}

async function rechazar(p) {
  try {
    await client.post(`/empresa/solicitudes/${p.id}/rechazar`)
    p.estatus = 'rechazado'
    flash.value = 'Postulante rechazado'
  } catch (e) {
    const detail = e.response?.data?.detail
    errors.value = [detail || 'Error al rechazar postulante']
  }
}

async function cancelar(p) {
  if (!confirm(`¿Cancelar la asignación de ${p.alumno_nombre}?`)) return
  try {
    await client.post(`/empresa/solicitudes/${p.id}/cancelar`)
    p.estatus = 'cancelado'
    flash.value = 'Servicio social cancelado'
  } catch (e) {
    const detail = e.response?.data?.detail
    if (Array.isArray(detail)) {
      errors.value = detail.map(d => d.msg || JSON.stringify(d))
    } else if (typeof detail === 'string') {
      errors.value = [detail]
    } else {
      errors.value = ['Error al cancelar']
    }
  }
}

async function doFinalizar(item) {
  if (!confirm(`¿Marcar "${item.titulo}" como finalizada? Esta acción no se puede deshacer.`)) return
  try {
    const { data } = await client.post(`/empresa/vacantes/${item.id}/finalizar`)
    Object.assign(item, data)
    flash.value = 'Vacante marcada como finalizada'
  } catch (e) {
    const detail = e.response?.data?.detail
    if (Array.isArray(detail)) {
      errors.value = detail.map(d => d.msg || JSON.stringify(d))
    } else if (typeof detail === 'string') {
      errors.value = [detail]
    } else {
      errors.value = ['Error al finalizar']
    }
  }
}

async function openPdf(solicitudId, doc) {
  try {
    const { data, headers } = await client.get(`/empresa/solicitudes/${solicitudId}/documentos/${doc}`, {
      responseType: 'blob',
    })
    const url = window.URL.createObjectURL(new Blob([data], { type: headers['content-type'] || 'application/pdf' }))
    window.open(url, '_blank')
  } catch (e) {
    error.value = 'Error al abrir el documento'
  }
}
</script>
