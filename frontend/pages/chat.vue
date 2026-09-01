<template>
  <div class="p-4 md:p-8">
    <div class="mx-auto max-w-5xl">
      <div class="mb-6 flex items-center justify-between gap-3">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.18em] text-blue-600">AI Assistant</p>
          <h3 class="text-2xl font-bold text-slate-900">Chat BengkelAI</h3>
        </div>
        <div class="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-medium text-emerald-700">
          <span class="h-2 w-2 rounded-full bg-emerald-500"></span>
          Online
        </div>
      </div>

      <div class="overflow-hidden rounded-[22px] border border-slate-200 bg-white shadow-[0_12px_40px_rgba(15,23,42,0.06)]">
        <div class="border-b border-slate-200 bg-slate-50/80 px-5 py-3.5">
          <div class="flex items-center justify-between gap-3">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-sm font-bold text-white">AI</div>
              <div>
                <p class="text-sm font-semibold text-slate-800">BengkelAI</p>
                <p class="text-xs text-slate-500">Membantu operasional bengkel</p>
              </div>
            </div>
          </div>
        </div>

        <div ref="chatListRef" class="h-[520px] overflow-y-auto bg-gradient-to-b from-slate-50 via-white to-slate-50 p-4 md:p-6">
          <div class="space-y-4">
            <div
              v-for="(message, index) in chatStore.messages"
              :key="index"
              class="flex w-full"
              :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
            >
              <div class="max-w-[80%] md:max-w-[72%]">
                <div
                  class="mb-1 text-[10px] font-medium uppercase tracking-wide text-slate-400"
                  :class="message.role === 'user' ? 'text-right' : 'text-left'"
                >
                  {{ message.role === 'user' ? 'Anda' : 'BengkelAI' }}
                </div>
                <div
                  class="rounded-2xl px-4 py-3 shadow-sm"
                  :class="message.role === 'user'
                    ? 'bg-blue-600 text-white rounded-br-md'
                    : 'bg-slate-200 text-slate-800 rounded-bl-md'"
                >
                  <p class="text-sm leading-relaxed break-words whitespace-pre-line">{{ message.content }}</p>
                </div>
              </div>
            </div>

            <div v-if="chatStore.loading" class="flex justify-start">
              <div class="max-w-[70%]">
                <div class="mb-1 text-[10px] font-medium uppercase tracking-wide text-slate-400">BengkelAI</div>
                <div class="rounded-2xl rounded-bl-md bg-slate-200 px-4 py-3 text-slate-700 shadow-sm">
                  <div class="flex items-center gap-2">
                    <span class="h-2 w-2 animate-pulse rounded-full bg-slate-500"></span>
                    <span class="h-2 w-2 animate-pulse rounded-full bg-slate-500 [animation-delay:120ms]"></span>
                    <span class="h-2 w-2 animate-pulse rounded-full bg-slate-500 [animation-delay:240ms]"></span>
                    <span class="text-sm text-slate-600">Sedang mengetik...</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="border-t border-slate-200 bg-white/90 p-3 md:p-4">
          <form @submit.prevent="sendMessage" class="flex items-center gap-3">
            <div class="relative flex-1">
              <input
                v-model="messageInput"
                type="text"
                placeholder="Tanyakan sesuatu ke BengkelAI..."
                :disabled="chatStore.loading"
                class="h-14 w-full rounded-2xl border border-slate-300 bg-slate-50 px-4 pr-12 text-base text-slate-800 placeholder:text-slate-400 focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-blue-100 disabled:bg-slate-100"
              />
            </div>
            <button
              type="submit"
              :disabled="chatStore.loading || !messageInput.trim()"
              class="flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-600 text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              <Icon name="lucide:send" class="h-5 w-5" />
            </button>
          </form>
        </div>
      </div>

      <div class="mt-6">
        <p class="mb-3 text-sm font-medium text-slate-600">Perintah cepat</p>
        <div class="grid grid-cols-2 gap-3 md:grid-cols-4">
          <button
            @click="messageInput = 'Cari kendaraan dengan plat D 1234 ABC'"
            class="rounded-xl border border-blue-100 bg-blue-50 px-3 py-3 text-left text-sm font-medium text-blue-700 transition hover:border-blue-200 hover:bg-blue-100"
          >
            🔍 Cari Kendaraan
          </button>
          <button
            @click="messageInput = 'Data pelanggan terbaru'"
            class="rounded-xl border border-emerald-100 bg-emerald-50 px-3 py-3 text-left text-sm font-medium text-emerald-700 transition hover:border-emerald-200 hover:bg-emerald-100"
          >
            👥 Info Pelanggan
          </button>
          <button
            @click="messageInput = 'Riwayat servis hari ini'"
            class="rounded-xl border border-amber-100 bg-amber-50 px-3 py-3 text-left text-sm font-medium text-amber-700 transition hover:border-amber-200 hover:bg-amber-100"
          >
            🔧 Servis Hari Ini
          </button>
          <button
            @click="messageInput = 'Suku cadang dengan stok rendah'"
            class="rounded-xl border border-rose-100 bg-rose-50 px-3 py-3 text-left text-sm font-medium text-rose-700 transition hover:border-rose-200 hover:bg-rose-100"
          >
            ⚠️ Stok Rendah
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const chatStore = useChatStore()
const messageInput = ref('')
const chatListRef = ref<HTMLElement | null>(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (chatListRef.value) {
      chatListRef.value.scrollTop = chatListRef.value.scrollHeight
    }
  })
}

const sendMessage = async () => {
  const trimmedMessage = messageInput.value.trim()
  if (!trimmedMessage) return

  try {
    messageInput.value = ''
    await chatStore.sendMessage(trimmedMessage)
    scrollToBottom()
  } catch (error) {
    console.error('Error sending message:', error)
  }
}

watch(
  () => chatStore.messages.length,
  () => {
    scrollToBottom()
  }
)

watch(
  () => chatStore.loading,
  () => {
    scrollToBottom()
  }
)

onMounted(() => {
  if (chatStore.messages.length === 0) {
    chatStore.messages.push({
      role: 'assistant',
      content: 'Halo! Saya BengkelAI, siap membantu Anda mengelola operasional bengkel. Apa yang bisa saya bantu?'
    })
  }
  scrollToBottom()
})
</script>
