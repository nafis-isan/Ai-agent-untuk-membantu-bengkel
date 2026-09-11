import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppointmentStore = defineStore('appointment', () => {
  const config = useRuntimeConfig()
  const appointments = ref<any[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchAppointments = async () => {
    loading.value = true
    try {
      appointments.value = await apiFetch(`${config.public.apiBase}/appointments/`)
      error.value = null
    } catch (err: any) {
      error.value = err?.data?.detail || err?.message || 'Appointment gagal dimuat'
    } finally {
      loading.value = false
    }
  }

  const createAppointment = async (payload: any) => {
    loading.value = true
    try {
      const result = await apiFetch(`${config.public.apiBase}/appointments/`, { method: 'POST', body: payload })
      appointments.value.push(result)
      return result
    } catch (err: any) {
      error.value = err?.data?.detail || err?.message || 'Appointment gagal dibuat'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateStatus = async (id: number, status: string) => {
    const result = await apiFetch(`${config.public.apiBase}/appointments/${id}/status`, { method: 'PATCH', body: { status } })
    const index = appointments.value.findIndex((item) => item.id === id)
    if (index > -1) appointments.value[index] = result
    return result
  }

  return { appointments, loading, error, fetchAppointments, createAppointment, updateStatus }
})
