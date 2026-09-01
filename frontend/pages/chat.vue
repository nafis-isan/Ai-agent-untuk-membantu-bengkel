<template>
  <div class="p-8">
    <h3 class="text-2xl font-bold text-slate-900 mb-6">AI Assistant Chat</h3>

    <div class="max-w-3xl">
      <div class="bg-white rounded-lg shadow h-96 flex flex-col">
        <!-- Chat Messages -->
        <div class="flex-1 overflow-y-auto p-6 space-y-4">
          <div v-for="(message, index) in chatStore.messages" :key="index">
            <!-- User Message -->
            <div v-if="message.role === 'user'" class="flex justify-end">
              <div class="bg-blue-600 text-white px-4 py-3 rounded-lg max-w-xs">
                <p>{{ message.content }}</p>
              </div>
            </div>

            <!-- Assistant Message -->
            <div v-else class="flex justify-start">
              <div class="bg-slate-100 text-slate-900 px-4 py-3 rounded-lg max-w-xs">
                <p>{{ message.content }}</p>
              </div>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="chatStore.loading" class="flex justify-start">
            <div class="bg-slate-100 text-slate-900 px-4 py-3 rounded-lg">
              <p class="text-sm">Sedang mengetik...</p>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <div class="border-t border-slate-200 p-4">
          <form @submit.prevent="sendMessage" class="flex gap-2">
            <input
              v-model="messageInput"
              type="text"
              placeholder="Tanyakan sesuatu ke BengkelAI..."
              :disabled="chatStore.loading"
              class="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-slate-100"
            />
            <button
              type="submit"
              :disabled="chatStore.loading || !messageInput.trim()"
              class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition disabled:bg-slate-400"
            >
              <Icon name="lucide:send" class="w-5 h-5" />
            </button>
          </form>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="mt-6">
        <p class="text-sm text-slate-600 mb-3">Perintah cepat:</p>
        <div class="grid grid-cols-2 gap-3">
          <button
            @click="messageInput = 'Cari kendaraan dengan plat D 1234 ABC'"
            class="text-left p-3 bg-blue-50 hover:bg-blue-100 rounded-lg transition text-sm text-blue-700 font-medium"
          >
            🔍 Cari Kendaraan
          </button>
          <button
            @click="messageInput = 'Data pelanggan terbaru'"
            class="text-left p-3 bg-green-50 hover:bg-green-100 rounded-lg transition text-sm text-green-700 font-medium"
          >
            👥 Info Pelanggan
          </button>
          <button
            @click="messageInput = 'Riwayat servis hari ini'"
            class="text-left p-3 bg-orange-50 hover:bg-orange-100 rounded-lg transition text-sm text-orange-700 font-medium"
          >
            🔧 Servis Hari Ini
          </button>
          <button
            @click="messageInput = 'Suku cadang dengan stok rendah'"
            class="text-left p-3 bg-red-50 hover:bg-red-100 rounded-lg transition text-sm text-red-700 font-medium"
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

const sendMessage = async () => {
  if (!messageInput.value.trim()) return

  try {
    await chatStore.sendMessage(messageInput.value)
    messageInput.value = ''
  } catch (error) {
    console.error('Error sending message:', error)
  }
}

onMounted(() => {
  // Initialize with welcome message
  if (chatStore.messages.length === 0) {
    chatStore.messages.push({
      role: 'assistant',
      content: 'Halo! Saya BengkelAI, siap membantu Anda mengelola operasional bengkel. Apa yang bisa saya bantu?'
    })
  }
})
</script>
