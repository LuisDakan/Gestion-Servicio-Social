<template>
  <div class="min-h-screen flex">
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-slate-900 to-slate-700 items-center justify-center p-12">
      <div class="max-w-md text-white">
        <div class="mb-8">
          <div class="w-16 h-16 bg-white/10 rounded-2xl flex items-center justify-center mb-6">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 14l9-5-9-5-9 5 9 5z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"/>
            </svg>
          </div>
          <h1 class="text-3xl font-bold">Sistema de Servicio Social</h1>
          <p class="mt-3 text-slate-300 leading-relaxed">
            Plataforma de gestión para el servicio social universitario. Conecta alumnos, empresas y administradores en un solo lugar.
          </p>
        </div>
        <div class="space-y-4">
          <div class="flex items-center gap-3 text-slate-300 text-sm">
            <svg class="w-5 h-5 text-emerald-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            Gestión de vacantes y postulaciones
          </div>
          <div class="flex items-center gap-3 text-slate-300 text-sm">
            <svg class="w-5 h-5 text-emerald-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            Seguimiento de solicitudes en tiempo real
          </div>
          <div class="flex items-center gap-3 text-slate-300 text-sm">
            <svg class="w-5 h-5 text-emerald-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            Reportes y código de confirmación
          </div>
        </div>
      </div>
    </div>
    <div class="flex-1 flex items-center justify-center p-8">
      <div class="w-full max-w-sm">
        <div class="lg:hidden mb-8">
          <div class="w-12 h-12 bg-slate-900 rounded-xl flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 14l9-5-9-5-9 5 9 5z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"/>
            </svg>
          </div>
          <h2 class="text-2xl font-bold">Iniciar sesión</h2>
          <p class="text-gray-500 mt-1">Accede al sistema de servicio social</p>
        </div>
        <div class="hidden lg:block mb-8">
          <h2 class="text-2xl font-bold">Iniciar sesión</h2>
          <p class="text-gray-500 mt-1">Ingresa tus credenciales para acceder</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <div v-if="errorMsg" class="p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-sm">
            {{ errorMsg }}
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Usuario</label>
            <input
              v-model="username"
              type="text"
              placeholder="Ingresa tu usuario"
              class="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-transparent transition-shadow"
              required
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Contraseña</label>
            <input
              v-model="password"
              type="password"
              placeholder="Ingresa tu contraseña"
              class="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-transparent transition-shadow"
              required
            />
          </div>
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-2.5 px-4 bg-slate-900 text-white rounded-lg text-sm font-semibold hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
          >
            <svg v-if="loading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            {{ loading ? 'Ingresando...' : 'Ingresar' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function handleLogin() {
  loading.value = true
  errorMsg.value = ''
  try {
    await auth.login(username.value, password.value)
    const routes = { admin: '/admin/dashboard', alumno: '/alumno/dashboard', empresa: '/empresa/dashboard' }
    router.push(routes[auth.role] || '/login')
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Credenciales inválidas. Intenta de nuevo.'
  } finally {
    loading.value = false
  }
}
</script>
