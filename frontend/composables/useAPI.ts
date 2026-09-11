// https://nuxt.com/docs/api/composables/use-fetch
import { $fetch } from 'ofetch'

const getAuthHeaders = () => {
  if (!import.meta.client) return {}

  const token = localStorage.getItem('bengkelai-token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export const apiFetch = async <T = unknown>(url: string, options: Record<string, any> = {}) => {
  try {
    return await $fetch<T>(url, {
      ...options,
      headers: { ...getAuthHeaders(), ...(options.headers || {}) }
    })
  } catch (error: any) {
    if (import.meta.client && error?.response?.status === 401) {
      localStorage.removeItem('bengkelai-token')
      await navigateTo('/login')
    }
    throw error
  }
}

export const useFetchAPI = (url: string, options = {}) => {
  const config = useRuntimeConfig()
  const headers = getAuthHeaders()
  return useFetch(() => `${config.public.apiBase}${url}`, {
    ...options,
    headers: { ...headers, ...(options as any).headers }
  })
}
