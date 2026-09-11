import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSparepartStore = defineStore('sparepart', () => {
  const config = useRuntimeConfig()
  const spareparts = ref<any[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchSpareparts = async () => {
    loading.value = true
    try {
      const response = await apiFetch(`${config.public.apiBase}/spareparts/`)
      spareparts.value = response
      error.value = null
    } catch (err: any) {
      error.value = err?.message || 'Error fetching spareparts'
    } finally {
      loading.value = false
    }
  }

  const createSparepart = async (sparepart: any) => {
    try {
      const response = await apiFetch(`${config.public.apiBase}/spareparts/`, {
        method: 'POST',
        body: sparepart
      })
      spareparts.value.push(response)
      return response
    } catch (err: any) {
      error.value = err?.message || 'Error creating sparepart'
      throw err
    }
  }

  const updateSparepart = async (id: number, sparepart: any) => {
    try {
      const response = await apiFetch(`${config.public.apiBase}/spareparts/${id}`, {
        method: 'PUT',
        body: sparepart
      })
      const index = spareparts.value.findIndex((item) => item.id === id)
      if (index > -1) {
        spareparts.value[index] = response
      }
      return response
    } catch (err: any) {
      error.value = err?.message || 'Error updating sparepart'
      throw err
    }
  }

  const deleteSparepart = async (id: number) => {
    try {
      await apiFetch(`${config.public.apiBase}/spareparts/${id}`, {
        method: 'DELETE'
      })
      spareparts.value = spareparts.value.filter((item) => item.id !== id)
    } catch (err: any) {
      error.value = err?.message || 'Error deleting sparepart'
      throw err
    }
  }

  return {
    spareparts,
    loading,
    error,
    fetchSpareparts,
    createSparepart,
    updateSparepart,
    deleteSparepart,
  }
})
