import { defineStore } from 'pinia'
import { ref } from 'vue'
import { $fetch } from 'ofetch'

export const useVehicleStore = defineStore('vehicle', () => {
  const config = useRuntimeConfig()
  const vehicles = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchVehicles = async () => {
    loading.value = true
    try {
      const response = await $fetch(`${config.public.apiBase}/vehicles`)
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
      const response = await $fetch(`${config.public.apiBase}/vehicles`, {
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

  const searchVehicle = async (plateNumber: string) => {
    try {
      const response = await $fetch(`${config.public.apiBase}/vehicles`, {
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
    searchVehicle
  }
})
