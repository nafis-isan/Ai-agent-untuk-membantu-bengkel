import { defineStore } from 'pinia'
import { ref } from 'vue'
import { $fetch } from 'ofetch'

export const useChatStore = defineStore('chat', () => {
  const config = useRuntimeConfig()
  const messages = ref<Array<{ role: string; content: string }>>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const sendMessage = async (message: string) => {
    messages.value.push({ role: 'user', content: message })
    loading.value = true

    try {
      const response = await $fetch(`${config.public.apiBase}/chat/`, {
        method: 'POST',
        body: { message }
      })
      
      messages.value.push({ role: 'assistant', content: response.response })
      error.value = null
    } catch (err: any) {
      error.value = err?.data?.detail || err?.data?.message || err?.message || 'Terjadi kesalahan saat menghubungi server.'
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearMessages = () => {
    messages.value = []
  }

  return {
    messages,
    loading,
    error,
    sendMessage,
    clearMessages
  }
})
