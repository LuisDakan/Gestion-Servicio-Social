<template>
  <div class="flex h-screen">
    <aside class="w-64 bg-slate-900 text-white flex flex-col shrink-0">
      <div class="h-16 flex items-center px-6 border-b border-slate-700">
        <span class="text-lg font-bold tracking-tight">Servicio Social</span>
      </div>
      <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === item.path ? 'bg-slate-700 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'"
        >
          <span v-html="item.icon" class="w-5 h-5 shrink-0"></span>
          {{ item.label }}
        </router-link>
      </nav>
      <div class="p-4 border-t border-slate-700">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-slate-600 flex items-center justify-center text-sm font-semibold">
            {{ roleInitial }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">{{ user?.name || roleLabel }}</p>
            <p class="text-xs text-slate-400 truncate">{{ roleLabel }}</p>
          </div>
        </div>
      </div>
    </aside>
    <div class="flex-1 flex flex-col overflow-hidden">
      <header class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 shrink-0">
        <h1 class="text-lg font-semibold text-gray-800">{{ pageTitle }}</h1>
        <button @click="logout" class="flex items-center gap-2 text-sm text-gray-500 hover:text-red-600 transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
          Cerrar sesión
        </button>
      </header>
      <main class="flex-1 overflow-y-auto p-6">
        <div v-if="flash" class="mb-4 p-4 rounded-lg bg-green-50 border border-green-200 text-green-800 text-sm flex items-center gap-2">
          <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          {{ flash }}
        </div>
        <div v-if="error" class="mb-4 p-4 rounded-lg bg-red-50 border border-red-200 text-red-800 text-sm flex items-center gap-2">
          <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          {{ error }}
        </div>
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, provide, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import client from '../api/client'

const props = defineProps({
  navItems: { type: Array, required: true },
  pageTitle: { type: String, default: '' },
})

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const flash = ref(null)
const error = ref(null)
const user = ref(null)

provide('flash', flash)
provide('error', error)

const roleLabel = computed(() => ({
  admin: 'Administrador',
  alumno: 'Alumno',
  empresa: 'Empresa',
}[auth.role] || auth.role))

const roleInitial = computed(() => roleLabel.value.charAt(0))

onMounted(async () => {
  try {
    const { data } = await client.get('/auth/me')
    user.value = data
  } catch {}
})

function logout() {
  auth.logout()
  router.push('/login')
}
</script>
