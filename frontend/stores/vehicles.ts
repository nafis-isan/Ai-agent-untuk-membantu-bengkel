import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useVehicleStore = defineStore('vehicle', () => {
  const config = useRuntimeConfig()
  const vehicles = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchVehicles = async () => {
    loading.value = true
    try {
      const response = await apiFetch(`${config.public.apiBase}/vehicles/`)
      vehicles.value = response
      error.value = null
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const createVehicle = async (vehicle: any) => {
    try {
      const response = await apiFetch(`${config.public.apiBase}/vehicles/`, {
        method: 'POST',
        body: vehicle
      })
      vehicles.value.push(response)
      return response
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const updateVehicle = async (id: number, vehicle: any) => {
    try {
      const response = await apiFetch(`${config.public.apiBase}/vehicles/${id}`, {
        method: 'PUT',
        body: vehicle
      })
      const index = vehicles.value.findIndex((item) => item.id === id)
      if (index > -1) vehicles.value[index] = response
      return response
    } catch (err: any) {
      error.value = err?.message || 'Error updating vehicle'
      throw err
    }
  }

  const deleteVehicle = async (id: number) => {
    try {
      await apiFetch(`${config.public.apiBase}/vehicles/${id}`, { method: 'DELETE' })
      vehicles.value = vehicles.value.filter((item) => item.id !== id)
    } catch (err: any) {
      error.value = err?.message || 'Error deleting vehicle'
      throw err
    }
  }

  const searchVehicle = async (plateNumber: string) => {
    try {
      const response = await apiFetch(`${config.public.apiBase}/vehicles/`, {
        query: { plate_number: plateNumber }
      })
      return response
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  return {
    vehicles,
    loading,
    error,
    fetchVehicles,
    createVehicle,
    updateVehicle,
    deleteVehicle,
    searchVehicle
  }
})
