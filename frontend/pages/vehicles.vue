<template>
  <div class="p-8">
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-2xl font-bold text-slate-900">Tracking Kendaraan</h3>
      <button
        @click="showForm = true"
        class="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
      >
        <Icon name="lucide:plus" class="w-5 h-5" />
        Tambah Kendaraan
      </button>
    </div>

    <!-- Search Bar -->
    <div class="mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Cari kendaraan (plat nomor)..."
        class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Vehicles Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="vehicle in filteredVehicles"
        :key="vehicle.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
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
          <button class="flex-1 text-sm bg-blue-50 text-blue-600 px-3 py-2 rounded hover:bg-blue-100 transition">
            Lihat Riwayat
          </button>
          <button class="flex-1 text-sm bg-slate-100 text-slate-700 px-3 py-2 rounded hover:bg-slate-200 transition">
            Edit
          </button>
        </div>
      </div>
    </div>

    <!-- Form Modal -->
    <div v-if="showForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-96">
        <h3 class="text-lg font-bold text-slate-900 mb-4">Tambah Kendaraan</h3>

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
              Simpan
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
const searchQuery = ref('')
const showForm = ref(false)

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

onMounted(() => {
  vehicleStore.fetchVehicles()
})

const submitForm = async () => {
  try {
    await vehicleStore.createVehicle(formData.value)
    showForm.value = false
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
</script>
