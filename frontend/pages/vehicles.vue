<template>
  <div class="space-y-6">
    <div class="flex flex-col justify-between gap-4 md:flex-row md:items-end">
      <div><p class="mb-2 text-sm font-semibold text-blue-600">Fleet pelanggan</p><h2 class="text-3xl font-extrabold tracking-tight text-slate-900">Kendaraan</h2><p class="mt-2 text-sm text-slate-500">Kelola seluruh kendaraan yang terdaftar di bengkel.</p></div>
      <button
        @click="showForm = true"
        class="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 text-sm font-bold text-white shadow-sm hover:bg-blue-700"
      >
        <Icon name="lucide:plus" class="w-5 h-5" />
        Tambah Kendaraan
      </button>
    </div>

    <!-- Search Bar -->
    <div class="relative rounded-2xl border border-slate-200 bg-white p-3 shadow-[0_4px_20px_rgb(15_23_42/0.03)]">
      <Icon name="lucide:search" class="absolute left-6 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Cari kendaraan (plat nomor)..."
        class="w-full rounded-xl border-0 bg-slate-50 py-3 pl-10 pr-4 text-sm outline-none placeholder:text-slate-400 focus:bg-white focus:ring-2 focus:ring-blue-100"
      />
    </div>

    <!-- Vehicles Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="vehicle in filteredVehicles"
        :key="vehicle.id"
        class="rounded-2xl border border-slate-200 bg-white p-6 shadow-[0_4px_20px_rgb(15_23_42/0.03)] transition hover:-translate-y-0.5 hover:shadow-md"
      >
        <div class="flex items-start justify-between mb-4">
          <div>
            <h4 class="text-lg font-bold text-slate-900">{{ vehicle.brand }} {{ vehicle.model }}</h4>
            <p class="text-sm text-slate-600">{{ vehicle.year }} • {{ vehicle.vehicle_type }}</p>
          </div>
          <Icon name="lucide:car" class="w-8 h-8 text-blue-500 opacity-40" />
        </div>

        <div class="space-y-2 mb-4 pb-4 border-b border-slate-200">
          <p class="text-sm">
            <span class="text-slate-600">Plat Nomor:</span>
            <span class="font-semibold text-slate-900">{{ vehicle.plate_number }}</span>
          </p>
          <p class="text-sm">
            <span class="text-slate-600">Pemilik ID:</span>
            <span class="font-semibold text-slate-900">#{{ vehicle.customer_id }}</span>
          </p>
        </div>

        <div class="flex gap-2">
          <button @click="openHistory(vehicle)" class="flex-1 text-sm bg-blue-50 text-blue-600 px-3 py-2 rounded hover:bg-blue-100 transition">
            Lihat Riwayat
          </button>
          <button @click="editVehicle(vehicle)" class="flex-1 text-sm bg-slate-100 text-slate-700 px-3 py-2 rounded hover:bg-slate-200 transition">
            Edit
          </button>
          <button @click="deleteVehicleHandler(vehicle.id)" class="rounded bg-rose-50 px-3 py-2 text-rose-600 transition hover:bg-rose-100" aria-label="Hapus kendaraan">
            <Icon name="lucide:trash-2" class="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>

    <div v-if="showHistory" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4 backdrop-blur-sm">
      <div class="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl">
        <div class="mb-6 flex items-start justify-between"><div><p class="text-xs font-semibold text-blue-600">Riwayat kendaraan</p><h3 class="mt-1 text-xl font-extrabold text-slate-900">{{ selectedVehicle?.brand }} {{ selectedVehicle?.model }}</h3><p class="mt-1 text-sm text-slate-500">{{ selectedVehicle?.plate_number }} · {{ selectedVehicle?.year }}</p></div><button class="rounded-lg p-2 text-slate-400 hover:bg-slate-100" aria-label="Tutup" @click="closeHistory"><Icon name="lucide:x" class="h-5 w-5" /></button></div>
        <div v-if="vehicleHistory.length" class="space-y-3"><div v-for="service in vehicleHistory" :key="service.id" class="rounded-xl border border-slate-200 bg-slate-50 p-4"><div class="flex items-start justify-between gap-3"><div><p class="text-sm font-bold text-slate-900">{{ service.complaint }}</p><p class="mt-1 text-xs text-slate-500">{{ formatDate(service.created_at) }} · Servis #{{ service.id }}</p></div><span class="shrink-0 rounded-full px-2.5 py-1 text-[10px] font-bold" :class="statusClass(service.status)">{{ statusLabel(service.status) }}</span></div><div class="mt-3 text-sm font-semibold text-slate-700">{{ formatCurrency(service.total_cost) }}</div></div></div><div v-else class="rounded-xl border border-dashed border-slate-300 p-8 text-center"><Icon name="lucide:history" class="mx-auto h-6 w-6 text-slate-400" /><p class="mt-3 text-sm font-bold text-slate-700">Belum ada riwayat servis</p><p class="mt-1 text-xs text-slate-500">Belum ada order servis untuk kendaraan ini.</p></div>
      </div>
    </div>

    <!-- Form Modal -->
    <div v-if="showForm" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4 backdrop-blur-sm">
      <div class="max-h-[90vh] w-full max-w-md overflow-y-auto rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl">
        <h3 class="text-lg font-bold text-slate-900 mb-4">{{ editingId ? 'Edit Kendaraan' : 'Tambah Kendaraan' }}</h3>

        <form @submit.prevent="submitForm" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Merk</label>
            <input
              v-model="formData.brand"
              type="text"
              required
              class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Model</label>
            <input
              v-model="formData.model"
              type="text"
              required
              class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Tahun</label>
            <input
              v-model="formData.year"
              type="number"
              required
              class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Plat Nomor</label>
            <input
              v-model="formData.plate_number"
              type="text"
              required
              class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Tipe Kendaraan</label>
            <select
              v-model="formData.vehicle_type"
              required
              class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Pilih Tipe</option>
              <option value="Mobil Penumpang">Mobil Penumpang</option>
              <option value="Mobil Barang">Mobil Barang</option>
              <option value="Motor">Motor</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">ID Pelanggan</label>
            <input
              v-model="formData.customer_id"
              type="number"
              required
              class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div class="flex gap-3">
            <button
              type="submit"
              class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
            >
              {{ editingId ? 'Simpan Perubahan' : 'Simpan' }}
            </button>
            <button
              type="button"
              @click="showForm = false"
              class="flex-1 bg-slate-300 text-slate-900 px-4 py-2 rounded-lg hover:bg-slate-400 transition"
            >
              Batal
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const vehicleStore = useVehicleStore()
const serviceStore = useServiceStore()
const searchQuery = ref('')
const showForm = ref(false)
const showHistory = ref(false)
const selectedVehicle = ref<any | null>(null)
const editingId = ref<number | null>(null)

const formData = ref({
  brand: '',
  model: '',
  year: new Date().getFullYear(),
  plate_number: '',
  vehicle_type: '',
  customer_id: 0
})

const filteredVehicles = computed(() => {
  return vehicleStore.vehicles.filter(vehicle =>
    vehicle.plate_number.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    `${vehicle.brand} ${vehicle.model}`.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const vehicleHistory = computed(() => selectedVehicle.value ? serviceStore.services.filter((service: any) => service.vehicle_id === selectedVehicle.value.id) : [])
const statusLabel = (status: string) => ({ waiting: 'Menunggu', in_progress: 'Dikerjakan', scheduled: 'Terjadwal', completed: 'Selesai', cancelled: 'Dibatalkan' }[status] || status)
const statusClass = (status: string) => ({ waiting: 'bg-amber-50 text-amber-700', in_progress: 'bg-blue-50 text-blue-700', scheduled: 'bg-indigo-50 text-indigo-700', completed: 'bg-emerald-50 text-emerald-700', cancelled: 'bg-rose-50 text-rose-700' }[status] || 'bg-slate-100 text-slate-600')
const formatDate = (value: string) => new Intl.DateTimeFormat('id-ID', { dateStyle: 'long' }).format(new Date(value))
const formatCurrency = (value: number) => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(value || 0)

const openHistory = (vehicle: any) => {
  selectedVehicle.value = vehicle
  showHistory.value = true
}

const closeHistory = () => {
  showHistory.value = false
  selectedVehicle.value = null
}

onMounted(async () => {
  await Promise.all([vehicleStore.fetchVehicles(), serviceStore.fetchServices()])
})

const submitForm = async () => {
  try {
    if (editingId.value) {
      await vehicleStore.updateVehicle(editingId.value, formData.value)
    } else {
      await vehicleStore.createVehicle(formData.value)
    }
    showForm.value = false
    editingId.value = null
    formData.value = {
      brand: '',
      model: '',
      year: new Date().getFullYear(),
      plate_number: '',
      vehicle_type: '',
      customer_id: 0
    }
  } catch (error) {
    console.error('Error:', error)
  }
}

const editVehicle = (vehicle: any) => {
  editingId.value = vehicle.id
  formData.value = { ...vehicle }
  showForm.value = true
}

const deleteVehicleHandler = async (id: number) => {
  if (!confirm('Apakah Anda yakin ingin menghapus kendaraan ini?')) return
  try {
    await vehicleStore.deleteVehicle(id)
  } catch (error) {
    console.error('Error:', error)
  }
}
</script>
