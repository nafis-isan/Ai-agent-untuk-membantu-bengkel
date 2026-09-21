<template>
  <div class="space-y-7">
    <section class="flex flex-col justify-between gap-5 md:flex-row md:items-end">
      <div><p class="mb-2 text-xs font-bold uppercase tracking-[0.2em] text-[#0f7771]">Senin, 21 September 2026 / Shift pagi</p><h2 class="text-4xl font-bold text-[#172126] md:text-5xl">Meja kerja bengkel.</h2><p class="mt-2 max-w-xl text-sm text-[#6e7a7d]">Satu pandangan untuk antrean, kendaraan, dan suku cadang yang perlu dibereskan hari ini.</p></div>
      <NuxtLink to="/services" class="inline-flex items-center justify-center gap-2 rounded-md bg-[#d96b35] px-4 py-3 text-sm font-bold text-white shadow-[4px_4px_0_#172126] hover:translate-x-0.5 hover:translate-y-0.5 hover:shadow-[2px_2px_0_#172126]"><Icon name="lucide:plus" class="h-4 w-4" />Tambah servis</NuxtLink>
    </section>

    <section class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <div v-for="stat in statCards" :key="stat.label" class="border border-[#d9d8d1] bg-[#fbfaf6] p-5 transition hover:-translate-y-0.5 hover:border-[#0f7771] hover:shadow-[4px_4px_0_#d9d8d1]">
        <div class="flex items-start justify-between"><div class="flex h-10 w-10 items-center justify-center rounded-md" :class="stat.iconBg"><Icon :name="stat.icon" class="h-5 w-5" :class="stat.iconColor" /></div><span class="text-[10px] font-bold uppercase tracking-[0.14em] text-[#0f7771]">Live</span></div>
        <p class="mt-5 text-xs font-bold uppercase tracking-[0.12em] text-[#6e7a7d]">{{ stat.label }}</p><p class="mt-1 text-4xl font-bold text-[#172126]">{{ stat.value }}</p><p class="mt-2 text-xs text-[#8a9694]">{{ stat.note }}</p>
      </div>
    </section>

    <section class="border-l-4 border-[#e9b949] bg-[#172126] p-5 text-white md:p-6">
      <div class="flex items-center justify-between"><div><h3 class="text-xl font-bold">Catatan operasional</h3><p class="mt-1 text-xs text-[#a7b2ad]">Ringkasan dari kondisi database bengkel</p></div><Icon name="lucide:clipboard-list" class="h-5 w-5 text-[#e9b949]" /></div>
      <div class="mt-4 grid grid-cols-1 gap-3 md:grid-cols-3"><div v-for="insight in insights" :key="insight.type" class="rounded-xl border p-4" :class="insightClass(insight.tone)"><div class="flex items-start gap-3"><Icon :name="insightIcon(insight.type)" class="mt-0.5 h-4 w-4 shrink-0" /><div><p class="text-sm font-bold">{{ insight.title }}</p><p class="mt-1 text-xs leading-5 opacity-80">{{ insight.description }}</p></div></div></div></div>
    </section>

    <section class="grid grid-cols-1 gap-5 xl:grid-cols-[1.35fr_0.65fr]">
      <div class="border border-[#d9d8d1] bg-[#fbfaf6] p-5 md:p-6">
        <div class="flex items-center justify-between"><div><h3 class="text-base font-bold text-slate-900">Ringkasan servis</h3><p class="mt-1 text-xs text-slate-400">Aktivitas servis dalam 6 periode terakhir</p></div><button class="rounded-lg p-2 text-slate-400 hover:bg-slate-50"><Icon name="lucide:more-horizontal" class="h-5 w-5" /></button></div>
        <div class="mt-8 flex h-48 items-end justify-between gap-3 border-b border-l border-slate-200 px-2 pb-0 pt-4"><div v-for="(height, index) in chartBars" :key="index" class="flex h-full flex-1 flex-col items-center justify-end gap-2"><div class="w-full max-w-10 rounded-t-lg bg-blue-500 transition hover:bg-blue-600" :style="{ height: `${height}%` }"></div><span class="text-[10px] text-slate-400">{{ chartLabels[index] }}</span></div></div>
      </div>
      <div class="bg-[#0f7771] p-6 text-white"><div class="flex items-center gap-2 text-[#e9b949]"><Icon name="lucide:activity" class="h-4 w-4" /><span class="text-xs font-bold uppercase tracking-wider">Operasional</span></div><h3 class="mt-6 text-2xl font-bold">Bengkel bergerak.</h3><p class="mt-2 text-sm leading-6 text-[#d4e2dc]">Jaga stok dan antrean supaya pekerjaan berikutnya tidak tertahan.</p><div class="mt-8 grid grid-cols-2 gap-3"><div class="border border-white/20 bg-white/10 p-3"><p class="text-3xl font-bold">{{ stats.services }}</p><p class="mt-1 text-[11px] text-[#d4e2dc]">Servis aktif</p></div><div class="border border-white/20 bg-white/10 p-3"><p class="text-3xl font-bold">{{ stats.lowStock }}</p><p class="mt-1 text-[11px] text-[#d4e2dc]">Perlu restock</p></div></div></div>
    </section>

    <section class="grid grid-cols-1 gap-5 xl:grid-cols-[1.35fr_0.65fr]">
      <div class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-[0_4px_20px_rgb(15_23_42/0.03)]"><div class="flex items-center justify-between border-b border-slate-100 p-5 md:p-6"><div><h3 class="text-base font-bold text-slate-900">Servis terbaru</h3><p class="mt-1 text-xs text-slate-400">Aktivitas pekerjaan yang baru masuk</p></div><NuxtLink to="/services" class="text-xs font-bold text-blue-600 hover:text-blue-700">Lihat semua</NuxtLink></div><div v-if="recentServices.length" class="divide-y divide-slate-100"><div v-for="service in recentServices" :key="service.id" class="flex items-center justify-between gap-4 p-5 transition hover:bg-slate-50"><div class="flex min-w-0 items-center gap-3"><span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600"><Icon name="lucide:wrench" class="h-4 w-4" /></span><div class="min-w-0"><p class="truncate text-sm font-bold text-slate-800">{{ getVehicleLabel(service.vehicle_id) }}</p><p class="truncate text-xs text-slate-400">{{ service.complaint || 'Tidak ada keluhan' }}</p></div></div><span class="shrink-0 rounded-full px-2.5 py-1 text-[10px] font-bold" :class="statusBadge(service.status)">{{ statusLabel(service.status) }}</span></div></div><div v-else class="p-8 text-center text-sm text-slate-400">Belum ada data servis.</div></div>
      <div class="rounded-2xl border border-slate-200 bg-white shadow-[0_4px_20px_rgb(15_23_42/0.03)]"><div class="border-b border-slate-100 p-5 md:p-6"><h3 class="text-base font-bold text-slate-900">Perlu restock</h3><p class="mt-1 text-xs text-slate-400">Suku cadang di bawah batas minimum</p></div><div v-if="lowStockParts.length" class="divide-y divide-slate-100"><div v-for="item in lowStockParts" :key="item.id" class="p-5"><div class="flex items-center justify-between gap-3"><div class="flex min-w-0 items-center gap-3"><span class="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-50 text-amber-600"><Icon name="lucide:package" class="h-4 w-4" /></span><p class="truncate text-sm font-bold text-slate-800">{{ item.name }}</p></div><span class="text-xs font-bold text-rose-600">{{ item.stock }} tersisa</span></div><div class="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full bg-amber-500" :style="{ width: `${Math.min((item.stock / Math.max(item.minimum_stock, 1)) * 100, 100)}%` }"></div></div></div></div><div v-else class="p-8 text-center text-sm text-slate-400">Stok semua aman.</div></div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useCustomerStore } from '~/stores/customers'
import { useVehicleStore } from '~/stores/vehicles'
import { useServiceStore } from '~/stores/services'
import { useSparepartStore } from '~/stores/spareparts'

definePageMeta({
  layout: 'default'
})

const customerStore = useCustomerStore()
const vehicleStore = useVehicleStore()
const serviceStore = useServiceStore()
const sparepartStore = useSparepartStore()
const config = useRuntimeConfig()
const insights = ref<Array<{ type: string; tone: string; title: string; description: string }>>([])

const stats = computed(() => ({
  customers: customerStore.customers.length,
  vehicles: vehicleStore.vehicles.length,
  services: serviceStore.services.filter((service) => ['waiting', 'in_progress', 'scheduled'].includes(service.status)).length,
  lowStock: sparepartStore.spareparts.filter((item) => item.stock <= item.minimum_stock).length
}))

const statCards = computed(() => [
  { label: 'Total Pelanggan', value: stats.value.customers, note: 'Terdaftar di sistem', icon: 'lucide:users', iconBg: 'bg-blue-50', iconColor: 'text-blue-600' },
  { label: 'Kendaraan Terdaftar', value: stats.value.vehicles, note: 'Kendaraan pelanggan', icon: 'lucide:car-front', iconBg: 'bg-emerald-50', iconColor: 'text-emerald-600' },
  { label: 'Servis Aktif', value: stats.value.services, note: 'Menunggu atau dikerjakan', icon: 'lucide:wrench', iconBg: 'bg-amber-50', iconColor: 'text-amber-600' },
  { label: 'Suku Cadang Low Stock', value: stats.value.lowStock, note: 'Perlu segera direstock', icon: 'lucide:package-open', iconBg: 'bg-rose-50', iconColor: 'text-rose-600' }
])

const chartBars = [42, 68, 54, 82, 64, 91]
const chartLabels = ['Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu']

const recentServices = computed(() => {
  return [...serviceStore.services]
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 3)
})

const lowStockParts = computed(() => {
  return [...sparepartStore.spareparts]
    .filter((item) => item.stock <= item.minimum_stock)
    .slice(0, 3)
})

const getVehicleLabel = (vehicleId: number) => {
  const vehicle = vehicleStore.vehicles.find((item) => item.id === vehicleId)
  if (!vehicle) return 'Kendaraan tidak diketahui'
  return `${vehicle.brand} ${vehicle.model} - ${vehicle.plate_number}`
}

const statusLabel = (status: string) => {
  const map: Record<string, string> = {
    waiting: 'Menunggu',
    in_progress: 'Proses',
    scheduled: 'Terjadwal',
    completed: 'Selesai',
    cancelled: 'Batal'
  }
  return map[status] || status
}

const statusClass = (status: string) => {
  const map: Record<string, string> = {
    waiting: 'text-yellow-600',
    in_progress: 'text-blue-600',
    scheduled: 'text-indigo-600',
    completed: 'text-green-600',
    cancelled: 'text-red-600'
  }
  return map[status] || 'text-slate-600'
}

const statusBadge = (status: string) => ({ waiting: 'bg-amber-50 text-amber-700', in_progress: 'bg-blue-50 text-blue-700', scheduled: 'bg-indigo-50 text-indigo-700', completed: 'bg-emerald-50 text-emerald-700', cancelled: 'bg-rose-50 text-rose-700' }[status] || 'bg-slate-100 text-slate-600')
const insightClass = (tone: string) => ({ blue: 'border-blue-100 bg-blue-50 text-blue-800', amber: 'border-amber-100 bg-amber-50 text-amber-800', rose: 'border-rose-100 bg-rose-50 text-rose-800', emerald: 'border-emerald-100 bg-emerald-50 text-emerald-800' }[tone] || 'border-slate-200 bg-slate-50 text-slate-700')
const insightIcon = (type: string) => ({ active_services: 'lucide:wrench', low_stock: 'lucide:package-open', waiting_services: 'lucide:clock-3', healthy: 'lucide:circle-check' }[type] || 'lucide:info')

onMounted(async () => {
  await Promise.all([
    customerStore.fetchCustomers(),
    vehicleStore.fetchVehicles(),
    serviceStore.fetchServices(),
    sparepartStore.fetchSpareparts(),
    $fetch(`${config.public.apiBase}/insights/`).then((response: any) => { insights.value = response.insights || [] })
  ])
})
</script>
