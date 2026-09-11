import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
  const config = useRuntimeConfig()
  const messages = ref<Array<{ role: string; content: string; actions?: Array<{ type: string; label: string; payload: Record<string, unknown> }> }>>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const sessionId = ref('')

  const sendMessage = async (message: string, action?: Record<string, unknown>) => {
    if (!sessionId.value && import.meta.client) {
      sessionId.value = localStorage.getItem('bengkelai-session-id') || crypto.randomUUID()
      localStorage.setItem('bengkelai-session-id', sessionId.value)
    }

    if (message.trim()) messages.value.push({ role: 'user', content: message })
    loading.value = true

    try {
      const response = await apiFetch<{ response?: string; actions?: Array<{ type: string; label: string; payload: Record<string, unknown> }> }>(`${config.public.apiBase}/chat/`, {
        method: 'POST',
        body: { message, session_id: sessionId.value || 'default', action }
      })

      messages.value.push({
        role: 'assistant',
        content: response.response?.trim() || 'AI tidak mengembalikan teks jawaban. Silakan coba pertanyaan lain.',
        actions: response.actions || []
      })
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
