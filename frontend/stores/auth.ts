import { defineStore } from 'pinia'
import { ref } from 'vue'
import { $fetch } from 'ofetch'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const user = ref(null)
  const token = ref('')

  const login = async (email: string, password: string) => {
    const config = useRuntimeConfig()
    const response = await $fetch<{ access_token: string }>(`${config.public.apiBase}/auth/login`, {
      method: 'POST',
      body: { username: email, password }
    })
    token.value = response.access_token
    isAuthenticated.value = true
    user.value = { username: email }
    if (import.meta.client) localStorage.setItem('bengkelai-token', token.value)
  }

  const logout = () => {
    isAuthenticated.value = false
    user.value = null
    token.value = ''
    if (import.meta.client) localStorage.removeItem('bengkelai-token')
  }

  return {
    isAuthenticated,
    user,
    token,
    login,
    logout
  }
})
