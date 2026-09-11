import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useServiceStore = defineStore('service', () => {
  const config = useRuntimeConfig()
  const services = ref<any[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchServices = async () => {
    loading.value = true
    try {
      const response = await apiFetch(`${config.public.apiBase}/services/`)
      services.value = response
      error.value = null
    } catch (err: any) {
      error.value = err?.message || 'Error fetching services'
    } finally {
      loading.value = false
    }
  }

  const createService = async (service: any) => {
    loading.value = true
    try {
      const response = await apiFetch(`${config.public.apiBase}/services/`, {
        method: 'POST',
        body: service
      })
      services.value.unshift(response)
      error.value = null
      return response
    } catch (err: any) {
      error.value = err?.data?.detail || err?.message || 'Error creating service'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateServiceStatus = async (id: number, status: string) => {
    loading.value = true
    try {
      const response = await apiFetch(`${config.public.apiBase}/services/${id}/status`, {
        method: 'PATCH',
        body: { status }
      })
      const index = services.value.findIndex((service) => service.id === id)
      if (index > -1) services.value[index] = response
      error.value = null
      return response
    } catch (err: any) {
      error.value = err?.data?.detail || err?.message || 'Error updating service status'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    services,
    loading,
    error,
    fetchServices,
    createService,
    updateServiceStatus
  }
})
