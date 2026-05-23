import { defineStore } from 'pinia'
import client from '../api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    role: localStorage.getItem('role') || null,
    user: null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    async login(username, password) {
      const { data } = await client.post('/auth/login', { username, password })
      this.token = data.access_token
      this.role = data.role
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('role', data.role)
      return data.role
    },
    logout() {
      this.token = null
      this.role = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('role')
    },
    async fetchMe() {
      const { data } = await client.get('/auth/me')
      this.user = data
      return data
    },
  },
})
