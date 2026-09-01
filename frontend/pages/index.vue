<template>
  <div class="p-8">
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-slate-600 text-sm">Total Pelanggan</p>
            <h3 class="text-3xl font-bold text-slate-900 mt-2">{{ stats.customers }}</h3>
          </div>
          <Icon name="lucide:users" class="w-12 h-12 text-blue-500 opacity-20" />
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-slate-600 text-sm">Kendaraan Terdaftar</p>
            <h3 class="text-3xl font-bold text-slate-900 mt-2">{{ stats.vehicles }}</h3>
          </div>
          <Icon name="lucide:car" class="w-12 h-12 text-green-500 opacity-20" />
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-slate-600 text-sm">Servis Aktif</p>
            <h3 class="text-3xl font-bold text-slate-900 mt-2">{{ stats.services }}</h3>
          </div>
          <Icon name="lucide:wrench" class="w-12 h-12 text-orange-500 opacity-20" />
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-slate-600 text-sm">Suku Cadang Rendah</p>
            <h3 class="text-3xl font-bold text-slate-900 mt-2">{{ stats.lowStock }}</h3>
          </div>
          <Icon name="lucide:alert-triangle" class="w-12 h-12 text-red-500 opacity-20" />
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-slate-900 mb-4">Servis Terbaru</h3>
        <div v-if="recentServices.length" class="space-y-4">
          <div
            v-for="service in recentServices"
            :key="service.id"
            class="flex items-center justify-between pb-4 border-b border-slate-200 last:border-0 last:pb-0"
          >
            <div>
              <p class="font-medium text-slate-900">{{ getVehicleLabel(service.vehicle_id) }}</p>
              <p class="text-sm text-slate-500">{{ service.complaint || 'Tidak ada keluhan' }}</p>
            </div>
            <span
              class="text-sm font-semibold"
              :class="statusClass(service.status)"
            >
              {{ statusLabel(service.status) }}
            </span>
          </div>
        </div>
        <div v-else class="text-sm text-slate-500">Belum ada data servis.</div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-slate-900 mb-4">Suku Cadang Low Stock</h3>
        <div v-if="lowStockParts.length" class="space-y-4">
          <div
            v-for="item in lowStockParts"
            :key="item.id"
            class="flex items-center justify-between pb-4 border-b border-slate-200 last:border-0 last:pb-0"
          >
            <div>
              <p class="font-medium text-slate-900">{{ item.name }}</p>
              <p class="text-sm text-slate-500">Stok: {{ item.stock }} unit</p>
            </div>
            <span
              class="px-3 py-1 text-xs font-semibold rounded-full"
              :class="item.stock <= item.minimum_stock ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'"
            >
              {{ item.stock <= item.minimum_stock ? 'Kritis' : 'Rendah' }}
            </span>
          </div>
        </div>
        <div v-else class="text-sm text-slate-500">Tidak ada suku cadang low stock.</div>
      </div>
    </div>
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

const stats = computed(() => ({
  customers: customerStore.customers.length,
  vehicles: vehicleStore.vehicles.length,
  services: serviceStore.services.filter((service) => ['waiting', 'in_progress', 'scheduled'].includes(service.status)).length,
  lowStock: sparepartStore.spareparts.filter((item) => item.stock <= item.minimum_stock).length
}))

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

onMounted(async () => {
  await Promise.all([
    customerStore.fetchCustomers(),
    vehicleStore.fetchVehicles(),
    serviceStore.fetchServices(),
    sparepartStore.fetchSpareparts()
  ])
})
</script>
