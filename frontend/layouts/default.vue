<template>
  <div class="min-h-screen bg-[#f6f8fb] text-slate-900">
    <div v-if="mobileOpen" class="fixed inset-0 z-40 bg-slate-950/35 lg:hidden" @click="mobileOpen = false"></div>
    <aside
      class="fixed inset-y-0 left-0 z-50 flex w-[270px] -translate-x-full flex-col border-r border-slate-200 bg-white px-4 py-5 transition-transform duration-200 lg:translate-x-0"
      :class="mobileOpen ? 'translate-x-0' : ''"
    >
      <div class="flex items-center justify-between px-3">
        <NuxtLink to="/" class="flex items-center gap-3" @click="mobileOpen = false">
          <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-white shadow-sm">
            <Icon name="lucide:car-front" class="h-5 w-5" />
          </span>
          <span>
            <span class="block text-[15px] font-extrabold tracking-tight text-slate-900">BengkelAI</span>
            <span class="block text-[11px] font-medium text-slate-400">Workshop Management</span>
          </span>
        </NuxtLink>
        <button class="rounded-lg p-2 text-slate-400 hover:bg-slate-100 lg:hidden" aria-label="Tutup menu" @click="mobileOpen = false">
          <Icon name="lucide:x" class="h-5 w-5" />
        </button>
      </div>

      <p class="mb-3 mt-10 px-3 text-[10px] font-bold uppercase tracking-[0.16em] text-slate-400">Workspace</p>
      <nav class="space-y-1">
        <NuxtLink v-for="item in navItems" :key="item.to" :to="item.to" class="sidebar-link" :class="route.path === item.to ? 'sidebar-link-active' : ''" @click="mobileOpen = false">
          <Icon :name="item.icon" class="h-[18px] w-[18px]" />
          <span>{{ item.label }}</span>
          <span v-if="item.to === '/chat'" class="ml-auto rounded-full bg-blue-100 px-2 py-0.5 text-[10px] font-bold text-blue-700">AI</span>
        </NuxtLink>
      </nav>

      <div class="mt-auto rounded-2xl bg-slate-900 p-4 text-white">
        <div class="mb-3 flex items-center gap-2 text-blue-300"><Icon name="lucide:sparkles" class="h-4 w-4" /><span class="text-xs font-semibold">BengkelAI Pro</span></div>
        <p class="text-xs leading-5 text-slate-300">Kelola operasional bengkel dengan lebih cepat dan teratur.</p>
        <div class="mt-4 h-1.5 overflow-hidden rounded-full bg-slate-700"><div class="h-full w-3/4 rounded-full bg-blue-400"></div></div>
        <p class="mt-2 text-[10px] text-slate-400">Workspace aktif</p>
      </div>
    </aside>

    <div class="lg:pl-[270px]">
      <header class="sticky top-0 z-30 border-b border-slate-200/80 bg-white/90 px-4 py-3 backdrop-blur md:px-8">
        <div class="mx-auto flex max-w-[1440px] items-center justify-between">
          <div class="flex items-center gap-3">
            <button class="rounded-xl border border-slate-200 p-2 text-slate-600 hover:bg-slate-50 lg:hidden" aria-label="Buka menu" @click="mobileOpen = true">
              <Icon name="lucide:menu" class="h-5 w-5" />
            </button>
            <div><p class="text-xs font-medium text-slate-400">Workspace / <span class="text-slate-600">{{ pageTitle }}</span></p><h1 class="mt-0.5 text-lg font-bold tracking-tight text-slate-900">{{ pageTitle }}</h1></div>
          </div>
          <div class="flex items-center gap-2 md:gap-4">
            <button class="relative rounded-xl p-2.5 text-slate-500 transition hover:bg-slate-100 hover:text-slate-900" aria-label="Notifikasi"><Icon name="lucide:bell" class="h-5 w-5" /><span class="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-blue-600 ring-2 ring-white"></span></button>
            <div class="hidden h-7 w-px bg-slate-200 md:block"></div>
            <button class="flex items-center gap-2 rounded-xl p-1.5 pr-2 transition hover:bg-slate-50" aria-label="Keluar" title="Keluar" @click="logout"><span class="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-100 text-xs font-bold text-blue-700">AD</span><span class="hidden text-left md:block"><span class="block text-xs font-bold text-slate-800">Admin Bengkel</span><span class="block text-[10px] text-slate-400">Administrator</span></span><Icon name="lucide:log-out" class="h-4 w-4 text-slate-400" /></button>
          </div>
        </div>
      </header>
      <main class="mx-auto max-w-[1440px] px-4 py-6 md:px-8 md:py-8"><slot /></main>
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
  border-radius: 0.75rem;
  padding: 0.75rem;
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 180ms ease-in-out;
}
.sidebar-link:hover {
  background: #f8fafc;
  color: #0f172a;
}
.sidebar-link-active {
  background: #eff6ff;
  color: #1d4ed8;
  box-shadow: 0 1px 2px rgb(15 23 42 / 0.04);
}
</style>
