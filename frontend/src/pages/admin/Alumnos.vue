<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <p class="text-sm text-gray-500">Total: {{ items.length }} alumnos</p>
      <button @click="openCreate" class="px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-medium hover:bg-slate-800 transition-colors flex items-center gap-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        Nuevo alumno
      </button>
    </div>

    <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <table class="w-full">
        <thead>
          <tr class="bg-gray-50 border-b border-gray-200">
            <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">No. Cuenta</th>
            <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Nombre</th>
            <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Carrera</th>
            <th class="text-left px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Teléfono</th>
            <th class="text-right px-5 py-3 text-xs font-semibold text-gray-500 uppercase">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="item in items" :key="item.id" class="hover:bg-gray-50 transition-colors">
            <td class="px-5 py-3.5 text-sm font-mono text-gray-800">{{ item.no_cuenta }}</td>
            <td class="px-5 py-3.5 text-sm text-gray-800">{{ item.nombre }}</td>
            <td class="px-5 py-3.5 text-sm text-gray-500">{{ item.carrera_nombre || item.carrera?.nombre || '-' }}</td>
            <td class="px-5 py-3.5 text-sm text-gray-500">{{ item.telefono || item.phone || '-' }}</td>
            <td class="px-5 py-3.5 text-right">
              <button @click="openEdit(item)" class="text-gray-400 hover:text-blue-600 mr-3 transition-colors" title="Editar">
                <svg class="w-4 h-4 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
              </button>
              <button @click="confirmDelete(item)" class="text-gray-400 hover:text-red-600 transition-colors" title="Eliminar">
                <svg class="w-4 h-4 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50" @click.self="showModal = false">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-lg mx-4 p-6">
        <h3 class="text-lg font-semibold mb-4">{{ editing ? 'Editar alumno' : 'Nuevo alumno' }}</h3>
        <form @submit.prevent="save">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">No. Cuenta</label>
              <input v-model="form.no_cuenta" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
              <input v-model="form.nombre" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Carrera</label>
              <select v-model="form.carrera_id" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" required>
                <option value="" disabled>Selecciona carrera</option>
                <option v-for="c in carreras" :key="c.id" :value="c.id">{{ c.nombre }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
              <input v-model="form.telefono" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input v-model="form.email" type="email" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" />
            </div>
            <div v-if="!editing">
              <label class="block text-sm font-medium text-gray-700 mb-1">Contraseña</label>
              <input v-model="form.password" type="password" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-slate-900 focus:border-transparent" :required="!editing" />
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
        <h3 class="text-lg font-semibold mb-2">Eliminar alumno</h3>
        <p class="text-sm text-gray-500 mb-6">¿Eliminar a "{{ deleteTarget.nombre }}"? Esta acción no se puede deshacer.</p>
        <div class="flex justify-center gap-3">
          <button @click="deleteTarget = null" class="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 transition-colors">Cancelar</button>
          <button @click="doDelete" class="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 transition-colors">Eliminar</button>
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
const carreras = ref([])
const showModal = ref(false)
const editing = ref(false)
const deleteTarget = ref(null)
const form = ref({ no_cuenta: '', nombre: '', carrera_id: '', telefono: '', email: '', password: '' })

onMounted(async () => {
  const [alumnosRes, carrerasRes] = await Promise.all([
    client.get('/admin/alumnos'),
    client.get('/admin/carreras'),
  ])
  items.value = alumnosRes.data
  carreras.value = carrerasRes.data
})

function openCreate() {
  editing.value = false
  form.value = { no_cuenta: '', nombre: '', carrera_id: '', telefono: '', email: '', password: '' }
  showModal.value = true
}

function openEdit(item) {
  editing.value = true
  form.value = { ...item, carrera_id: item.carrera_id || item.carrera?.id || '' }
  showModal.value = true
}

async function save() {
  try {
    if (editing.value) {
      const payload = { ...form.value }
      delete payload.password
      const { data } = await client.put(`/admin/alumnos/${form.value.id}`, payload)
      Object.assign(items.value.find(i => i.id === form.value.id), data)
      flash.value = 'Alumno actualizado correctamente'
    } else {
      const { data } = await client.post('/admin/alumnos', form.value)
      items.value.push(data)
      flash.value = 'Alumno creado correctamente'
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
    await client.delete(`/admin/alumnos/${deleteTarget.value.id}`)
    items.value = items.value.filter(i => i.id !== deleteTarget.value.id)
    flash.value = 'Alumno eliminado correctamente'
    deleteTarget.value = null
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al eliminar'
  }
}
</script>
