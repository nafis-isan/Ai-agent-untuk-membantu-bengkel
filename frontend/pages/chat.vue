<template>
  <div class="mx-auto max-w-6xl space-y-6">
      <div class="flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div><p class="mb-2 text-sm font-semibold text-blue-600">AI Assistant</p><h2 class="text-3xl font-extrabold tracking-tight text-slate-900">BengkelAI siap membantu</h2><p class="mt-2 text-sm text-slate-500">Tanyakan kondisi kendaraan, stok, atau operasional bengkel Anda.</p></div>
        <div class="inline-flex w-fit items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs font-bold text-emerald-700"><span class="h-2 w-2 rounded-full bg-emerald-500"></span>Online sekarang</div>
      </div>

      <div class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-[0_8px_30px_rgb(15_23_42/0.05)]">
        <div class="border-b border-slate-200 bg-white px-5 py-4">
          <div class="flex items-center justify-between gap-3">
            <div class="flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-sm font-bold text-white shadow-sm"><Icon name="lucide:sparkles" class="h-5 w-5" /></div>
              <div>
                <p class="text-sm font-semibold text-slate-800">BengkelAI</p>
                <p class="text-xs text-slate-500">Asisten operasional bengkel</p>
              </div>
            </div>
          </div>
        </div>

        <div ref="chatListRef" class="h-[520px] overflow-y-auto bg-[#f8fafc] p-4 md:p-6">
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
                    : 'border border-slate-200 bg-white text-slate-700 rounded-bl-md'"
                >
                  <p class="text-sm leading-relaxed break-words whitespace-pre-line">{{ formatMessage(message.content) }}</p>
                  <div v-if="message.actions?.length" class="mt-4 space-y-2 border-t border-slate-200 pt-3">
                    <p class="text-xs font-semibold text-slate-500">Konfirmasi tindakan</p>
                    <button v-for="action in message.actions" :key="action.type" class="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-3 py-2 text-xs font-bold text-white hover:bg-blue-700" @click="confirmAction(action)">
                      <Icon name="lucide:check" class="h-3.5 w-3.5" />{{ action.label }}
                    </button>
                  </div>
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
          <form @submit.prevent="sendMessage" class="flex items-end gap-3">
            <div class="relative flex-1">
              <textarea
                v-model="messageInput"
                rows="1"
                placeholder="Tanyakan sesuatu kepada BengkelAI..."
                :disabled="chatStore.loading"
                class="min-h-14 w-full resize-none rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4 text-sm text-slate-800 placeholder:text-slate-400 focus:border-blue-500 focus:bg-white focus:outline-none focus:ring-4 focus:ring-blue-100 disabled:bg-slate-100"
                @keydown.enter.exact.prevent="sendMessage"
              ></textarea>
            </div>
            <button
              type="submit"
              :disabled="chatStore.loading || !messageInput.trim()"
              class="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-blue-600 text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
            >
              <Icon name="lucide:send" class="h-5 w-5" />
            </button>
          </form>
          <p v-if="chatStore.error" class="mt-2 text-sm text-rose-600">
            Gagal mengirim pesan: {{ chatStore.error }}
          </p>
        </div>
      </div>

      <div>
        <div class="mb-3 flex items-center gap-2"><Icon name="lucide:zap" class="h-4 w-4 text-amber-500" /><p class="text-sm font-bold text-slate-800">Mulai dari sini</p></div>
        <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 md:grid-cols-4">
          <button
            @click="messageInput = 'Cari kendaraan dengan plat D 1234 ABC'"
            class="group rounded-xl border border-slate-200 bg-white px-4 py-4 text-left text-sm font-semibold text-slate-700 shadow-sm hover:-translate-y-0.5 hover:border-blue-200 hover:text-blue-700"
          >
            <Icon name="lucide:car-front" class="mb-3 h-5 w-5 text-blue-600" /><span class="block">Cari Kendaraan</span><span class="mt-1 block text-xs font-normal text-slate-400">Temukan data kendaraan</span>
          </button>
          <button
            @click="messageInput = 'Data pelanggan terbaru'"
            class="group rounded-xl border border-slate-200 bg-white px-4 py-4 text-left text-sm font-semibold text-slate-700 shadow-sm hover:-translate-y-0.5 hover:border-emerald-200 hover:text-emerald-700"
          >
            <Icon name="lucide:users" class="mb-3 h-5 w-5 text-emerald-600" /><span class="block">Info Pelanggan</span><span class="mt-1 block text-xs font-normal text-slate-400">Lihat data pelanggan</span>
          </button>
          <button
            @click="messageInput = 'Riwayat servis hari ini'"
            class="group rounded-xl border border-slate-200 bg-white px-4 py-4 text-left text-sm font-semibold text-slate-700 shadow-sm hover:-translate-y-0.5 hover:border-amber-200 hover:text-amber-700"
          >
            <Icon name="lucide:wrench" class="mb-3 h-5 w-5 text-amber-600" /><span class="block">Servis Hari Ini</span><span class="mt-1 block text-xs font-normal text-slate-400">Cek antrean pekerjaan</span>
          </button>
          <button
            @click="messageInput = 'Suku cadang dengan stok rendah'"
            class="group rounded-xl border border-slate-200 bg-white px-4 py-4 text-left text-sm font-semibold text-slate-700 shadow-sm hover:-translate-y-0.5 hover:border-rose-200 hover:text-rose-700"
          >
            <Icon name="lucide:package-open" class="mb-3 h-5 w-5 text-rose-600" /><span class="block">Stok Rendah</span><span class="mt-1 block text-xs font-normal text-slate-400">Periksa kebutuhan restock</span>
          </button>
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

const formatMessage = (content: unknown) => String(content || '')
  .replace(/\*\*(.*?)\*\*/g, '$1')
  .replace(/^\s*[*-]\s+/gm, '')
  .replace(/^\s*#{1,6}\s+/gm, '')
  .replace(/\*([^*]+)\*/g, '$1')

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

const confirmAction = async (action: { type: string; label: string; payload: Record<string, unknown>; confirmation_token: string }) => {
  await chatStore.sendMessage(`Konfirmasi: ${action.label}`, action)
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
