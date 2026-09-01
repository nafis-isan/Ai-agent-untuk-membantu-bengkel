<template>
  <div class="flex h-screen bg-slate-50">
    <!-- Sidebar -->
    <div class="w-64 bg-white border-r border-slate-200">
      <div class="p-6">
        <h1 class="text-2xl font-bold text-blue-600">BengkelAI</h1>
        <p class="text-sm text-slate-500 mt-1">Workshop Management</p>
      </div>

      <nav class="mt-6 space-y-2 px-3">
        <NuxtLink
          to="/"
          class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-50 text-slate-700 hover:text-blue-600 transition"
        >
          <Icon name="lucide:home" class="w-5 h-5" />
          <span>Dashboard</span>
        </NuxtLink>

        <NuxtLink
          to="/customers"
          class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-50 text-slate-700 hover:text-blue-600 transition"
        >
          <Icon name="lucide:users" class="w-5 h-5" />
          <span>Pelanggan</span>
        </NuxtLink>

        <NuxtLink
          to="/vehicles"
          class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-50 text-slate-700 hover:text-blue-600 transition"
        >
          <Icon name="lucide:car" class="w-5 h-5" />
          <span>Kendaraan</span>
        </NuxtLink>

        <NuxtLink
          to="/services"
          class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-50 text-slate-700 hover:text-blue-600 transition"
        >
          <Icon name="lucide:wrench" class="w-5 h-5" />
          <span>Layanan</span>
        </NuxtLink>

        <NuxtLink
          to="/spareparts"
          class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-50 text-slate-700 hover:text-blue-600 transition"
        >
          <Icon name="lucide:package" class="w-5 h-5" />
          <span>Suku Cadang</span>
        </NuxtLink>

        <NuxtLink
          to="/chat"
          class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-50 text-slate-700 hover:text-blue-600 transition"
        >
          <Icon name="lucide:message-circle" class="w-5 h-5" />
          <span>AI Chat</span>
        </NuxtLink>
      </nav>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col">
      <!-- Top Bar -->
      <div class="bg-white border-b border-slate-200 px-8 py-4">
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-semibold text-slate-900">{{ pageTitle }}</h2>
          <div class="flex items-center gap-4">
            <button class="p-2 hover:bg-slate-100 rounded-lg" aria-label="Notifikasi">
              <Icon name="lucide:bell" class="w-5 h-5 text-slate-600" />
            </button>
          </div>
        </div>
      </div>

      <!-- Page Content -->
      <div class="flex-1 overflow-auto">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()

const pageTitle = computed(() => {
  const titles: Record<string, string> = {
    '/': 'Dashboard',
    '/customers': 'Manajemen Pelanggan',
    '/vehicles': 'Tracking Kendaraan',
    '/services': 'Riwayat Servis',
    '/spareparts': 'Manajemen Suku Cadang',
    '/chat': 'AI Assistant'
  }
  return titles[route.path] || 'BengkelAI'
})
</script>
