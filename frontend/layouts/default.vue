<template>
  <div class="min-h-screen text-[#172126]">
    <div v-if="mobileOpen" class="fixed inset-0 z-40 bg-slate-950/35 lg:hidden" @click="mobileOpen = false"></div>
    <aside
      class="fixed inset-y-0 left-0 z-50 flex w-[270px] -translate-x-full flex-col border-r border-[#314247] bg-[#172126] px-4 py-5 text-white transition-transform duration-200 lg:translate-x-0"
      :class="mobileOpen ? 'translate-x-0' : ''"
    >
      <div class="flex items-center justify-between px-3">
        <NuxtLink to="/" class="flex items-center gap-3" @click="mobileOpen = false">
          <span class="flex h-10 w-10 items-center justify-center rounded-lg bg-[#e9b949] text-[#172126] shadow-[3px_3px_0_#0f7771]">
            <Icon name="lucide:wrench" class="h-5 w-5" />
          </span>
          <span>
            <span class="block text-lg font-bold tracking-wide text-white">BengkelAI</span>
            <span class="block text-[11px] font-medium uppercase tracking-[0.14em] text-[#a7b2ad]">Workshop desk</span>
          </span>
        </NuxtLink>
        <button class="rounded-lg p-2 text-[#a7b2ad] hover:bg-[#26353a] lg:hidden" aria-label="Tutup menu" @click="mobileOpen = false">
          <Icon name="lucide:x" class="h-5 w-5" />
        </button>
      </div>

      <p class="mb-3 mt-10 px-3 text-[10px] font-bold uppercase tracking-[0.2em] text-[#a7b2ad]">Workspace</p>
      <nav class="space-y-1">
        <NuxtLink v-for="item in navItems" :key="item.to" :to="item.to" class="sidebar-link" :class="route.path === item.to ? 'sidebar-link-active' : ''" @click="mobileOpen = false">
          <Icon :name="item.icon" class="h-[18px] w-[18px]" />
          <span>{{ item.label }}</span>
          <span v-if="item.to === '/chat'" class="ml-auto rounded bg-[#e9b949] px-1.5 py-0.5 text-[10px] font-bold text-[#172126]">AI</span>
        </NuxtLink>
      </nav>

      <div class="mt-auto border-t border-[#314247] pt-4">
        <div class="mb-3 flex items-center gap-2 text-[#e9b949]"><Icon name="lucide:radio" class="h-4 w-4" /><span class="text-xs font-bold uppercase tracking-[0.14em]">Shift aktif</span></div>
        <p class="text-xs leading-5 text-[#c0cbc5]">Pantau pekerjaan, stok, dan pelanggan dari satu meja kerja.</p>
        <div class="mt-4 flex items-center gap-2 text-[10px] uppercase tracking-[0.14em] text-[#7f918e]"><span class="h-2 w-2 rounded-full bg-[#8fcf62]"></span> Sistem siap</div>
      </div>
    </aside>

    <div class="lg:pl-[270px]">
      <header class="sticky top-0 z-30 border-b border-[#d9d8d1]/90 bg-[#f3f1eb]/90 px-4 py-3 backdrop-blur md:px-8">
        <div class="mx-auto flex max-w-[1440px] items-center justify-between">
          <div class="flex items-center gap-3">
            <button class="rounded-lg border border-[#d9d8d1] p-2 text-[#172126] hover:bg-white lg:hidden" aria-label="Buka menu" @click="mobileOpen = true">
              <Icon name="lucide:menu" class="h-5 w-5" />
            </button>
            <div><p class="text-[10px] font-bold uppercase tracking-[0.18em] text-[#8a9694]">BengkelAI / <span class="text-[#0f7771]">{{ pageTitle }}</span></p><h1 class="mt-0.5 text-2xl font-bold text-[#172126]">{{ pageTitle }}</h1></div>
          </div>
          <div class="flex items-center gap-2 md:gap-4">
            <button class="relative rounded-lg p-2.5 text-[#6e7a7d] transition hover:bg-white hover:text-[#172126]" aria-label="Notifikasi"><Icon name="lucide:bell" class="h-5 w-5" /><span class="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-[#d96b35] ring-2 ring-[#f3f1eb]"></span></button>
            <div class="hidden h-7 w-px bg-[#d9d8d1] md:block"></div>
            <button class="flex items-center gap-2 rounded-lg p-1.5 pr-2 transition hover:bg-white" aria-label="Keluar" title="Keluar" @click="logout"><span class="flex h-8 w-8 items-center justify-center rounded bg-[#0f7771] text-xs font-bold text-white">AD</span><span class="hidden text-left md:block"><span class="block text-xs font-bold text-[#172126]">Admin Bengkel</span><span class="block text-[10px] text-[#6e7a7d]">Administrator</span></span><Icon name="lucide:log-out" class="h-4 w-4 text-[#6e7a7d]" /></button>
          </div>
        </div>
      </header>
      <main class="mx-auto max-w-[1440px] px-4 py-6 md:px-8 md:py-9"><slot /></main>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const auth = useAuthStore()
const mobileOpen = ref(false)
const navItems = [
  { to: '/', label: 'Dashboard', icon: 'lucide:layout-dashboard' },
  { to: '/customers', label: 'Pelanggan', icon: 'lucide:users' },
  { to: '/vehicles', label: 'Kendaraan', icon: 'lucide:car-front' },
  { to: '/services', label: 'Layanan', icon: 'lucide:wrench' },
  { to: '/appointments', label: 'Appointment', icon: 'lucide:calendar-days' },
  { to: '/spareparts', label: 'Suku Cadang', icon: 'lucide:package' },
  { to: '/chat', label: 'AI Assistant', icon: 'lucide:message-circle' }
]

const pageTitle = computed(() => {
  const titles: Record<string, string> = {
    '/': 'Dashboard',
    '/customers': 'Manajemen Pelanggan',
    '/vehicles': 'Tracking Kendaraan',
    '/services': 'Riwayat Servis',
    '/appointments': 'Appointment',
    '/spareparts': 'Manajemen Suku Cadang',
    '/chat': 'AI Assistant'
  }
  return titles[route.path] || 'BengkelAI'
})

watch(() => route.path, () => { mobileOpen.value = false })

const logout = async () => {
  auth.logout()
  await navigateTo('/login')
}
</script>

<style scoped>
.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-radius: 0.4rem;
  padding: 0.75rem;
  color: #a7b2ad;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 180ms ease-in-out;
}
.sidebar-link:hover {
  background: #26353a;
  color: #ffffff;
}
.sidebar-link-active {
  background: #e9b949;
  color: #172126;
  box-shadow: 3px 3px 0 #0f7771;
}
</style>
