<template>
  <div class="space-y-6">
    <div class="flex flex-col justify-between gap-4 md:flex-row md:items-end"><div><p class="mb-2 text-sm font-semibold text-blue-600">Aktivitas bengkel</p><h2 class="text-3xl font-extrabold tracking-tight text-slate-900">Riwayat Servis</h2><p class="mt-2 text-sm text-slate-500">Pantau pekerjaan dan riwayat layanan kendaraan pelanggan.</p></div><button @click="openForm" class="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 text-sm font-bold text-white shadow-sm hover:bg-blue-700"><Icon name="lucide:plus" class="h-4 w-4" />Buat Servis Baru</button></div>

    <div class="max-w-4xl">
      <div v-if="serviceStore.loading" class="space-y-4">
        <div v-for="item in 3" :key="item" class="h-48 animate-pulse rounded-2xl border border-slate-200 bg-white"></div>
      </div>

      <div v-else-if="serviceStore.error" class="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-sm text-rose-700">
        <div class="flex items-center gap-3"><Icon name="lucide:circle-alert" class="h-5 w-5" /><span>Data riwayat servis tidak dapat dimuat saat ini.</span></div>
        <button class="mt-4 rounded-lg bg-white px-3 py-2 text-xs font-bold text-rose-700 shadow-sm" @click="serviceStore.fetchServices">Coba lagi</button>
      </div>

      <div v-else-if="!serviceStore.services.length" class="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center">
        <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50 text-blue-600"><Icon name="lucide:wrench" class="h-6 w-6" /></div>
        <h3 class="mt-4 text-base font-bold text-slate-900">Belum ada riwayat servis</h3>
        <p class="mx-auto mt-2 max-w-sm text-sm leading-6 text-slate-500">Data layanan dari backend akan muncul di sini setelah servis dibuat.</p>
      </div>

      <div v-else v-for="(service, index) in serviceStore.services" :key="service.id" class="group flex gap-4 md:gap-6">
        <div class="flex flex-col items-center">
          <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-blue-100 bg-blue-50">
            <Icon name="lucide:wrench" class="w-6 h-6 text-blue-600" />
          </div>
          <div v-if="index < serviceStore.services.length - 1" class="my-2 h-full w-px bg-slate-200"></div>
        </div>

        <div class="flex-1 pb-6">
          <div class="mb-6 rounded-2xl border border-slate-200 bg-white p-5 shadow-[0_4px_20px_rgb(15_23_42/0.03)] transition hover:-translate-y-0.5 hover:shadow-md md:p-6">
            <div class="flex justify-between items-start mb-3">
              <div>
                <h4 class="text-lg font-bold text-slate-900">{{ vehicleLabel(service.vehicle_id) }}</h4>
                <p class="text-sm text-slate-600">ID Servis #{{ service.id }}</p>
              </div>
              <span :class="`rounded-full px-3 py-1 text-xs font-semibold ${statusClass(service.status)}`">
                {{ statusLabel(service.status) }}
              </span>
            </div>

            <p class="mb-4 text-slate-700">{{ service.complaint || 'Tidak ada keluhan yang dicatat.' }}</p>

            <div class="grid grid-cols-2 gap-4 mb-4 pb-4 border-b border-slate-200">
              <div>
                <p class="text-sm text-slate-600">Tanggal Servis</p>
                <p class="font-semibold text-slate-900">{{ formatDate(service.created_at) }}</p>
              </div>
              <div>
                <p class="text-sm text-slate-600">Biaya</p>
                <p class="font-semibold text-slate-900">{{ formatCurrency(service.total_cost) }}</p>
              </div>
            </div>

            <div class="flex gap-2">
              <button @click="openDetail(service)" class="inline-flex items-center gap-1.5 text-sm font-semibold text-blue-600 hover:text-blue-700"><Icon name="lucide:eye" class="h-4 w-4" />Lihat Detail</button>
              <button
                v-if="nextStatus(service.status)"
                :disabled="serviceStore.loading"
                @click="advanceService(service)"
                class="inline-flex items-center gap-1.5 rounded-lg bg-emerald-600 px-3 py-2 text-sm font-semibold text-white hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-slate-300"
              >
                <Icon :name="service.status === 'in_progress' ? 'lucide:check-circle-2' : 'lucide:play'" class="h-4 w-4" />
                {{ nextStatusLabel(service.status) }}
              </button>
              <button class="inline-flex items-center gap-1.5 text-sm font-semibold text-slate-500 hover:text-slate-700"><Icon name="lucide:printer" class="h-4 w-4" />Cetak Invoice</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showDetail && selectedService" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4 backdrop-blur-sm">
      <div class="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl">
        <div class="mb-6 flex items-start justify-between"><div><p class="text-xs font-semibold text-blue-600">Detail order servis</p><h3 class="mt-1 text-xl font-extrabold text-slate-900">Servis #{{ selectedService.id }}</h3><p class="mt-1 text-sm text-slate-500">{{ vehicleLabel(selectedService.vehicle_id) }}</p></div><button class="rounded-lg p-2 text-slate-400 hover:bg-slate-100" aria-label="Tutup" @click="closeDetail"><Icon name="lucide:x" class="h-5 w-5" /></button></div>
        <div class="grid grid-cols-2 gap-3"><div class="rounded-xl bg-slate-50 p-3"><p class="text-xs text-slate-400">Status</p><span class="mt-2 inline-flex rounded-full px-2.5 py-1 text-xs font-bold" :class="statusClass(selectedService.status)">{{ statusLabel(selectedService.status) }}</span></div><div class="rounded-xl bg-slate-50 p-3"><p class="text-xs text-slate-400">Tanggal</p><p class="mt-2 text-sm font-bold text-slate-800">{{ formatDate(selectedService.created_at) }}</p></div></div>
        <div class="mt-4 space-y-4"><div><p class="text-xs font-bold uppercase tracking-wider text-slate-400">Keluhan</p><p class="mt-1 text-sm leading-6 text-slate-700">{{ selectedService.complaint || '-' }}</p></div><div><p class="text-xs font-bold uppercase tracking-wider text-slate-400">Diagnosa</p><p class="mt-1 text-sm leading-6 text-slate-700">{{ selectedService.diagnosis || 'Belum ada diagnosa.' }}</p></div><div class="flex items-center justify-between border-t border-slate-100 pt-4"><span class="text-sm font-semibold text-slate-500">Total biaya</span><span class="text-lg font-extrabold text-slate-900">{{ formatCurrency(selectedService.total_cost) }}</span></div></div>
      </div>
    </div>

    <div v-if="showForm" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4 backdrop-blur-sm">
      <div class="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl">
        <div class="mb-6 flex items-start justify-between">
          <div><p class="text-xs font-semibold text-blue-600">Order servis baru</p><h3 class="mt-1 text-xl font-extrabold text-slate-900">Buat Servis Baru</h3><p class="mt-1 text-sm text-slate-500">Masukkan keluhan kendaraan untuk membuat antrean servis.</p></div>
          <button type="button" class="rounded-lg p-2 text-slate-400 hover:bg-slate-100" aria-label="Tutup" @click="closeForm"><Icon name="lucide:x" class="h-5 w-5" /></button>
        </div>

        <form class="space-y-4" @submit.prevent="submitService">
          <div><label class="mb-1.5 block text-sm font-semibold text-slate-700">Kendaraan</label><select v-model.number="formData.vehicle_id" required class="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-3 text-sm outline-none focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-50"><option :value="0" disabled>Pilih kendaraan</option><option v-for="vehicle in vehicleStore.vehicles" :key="vehicle.id" :value="vehicle.id">{{ vehicle.brand }} {{ vehicle.model }} - {{ vehicle.plate_number }}</option></select><p v-if="!vehicleStore.vehicles.length" class="mt-1 text-xs text-amber-600">Belum ada kendaraan. Tambahkan kendaraan terlebih dahulu.</p></div>
          <div><label class="mb-1.5 block text-sm font-semibold text-slate-700">Keluhan</label><textarea v-model="formData.complaint" required rows="3" placeholder="Contoh: Mesin sulit dinyalakan saat pagi hari" class="w-full resize-none rounded-xl border border-slate-200 bg-slate-50 px-3 py-3 text-sm outline-none placeholder:text-slate-400 focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-50"></textarea></div>
          <div><label class="mb-1.5 block text-sm font-semibold text-slate-700">Diagnosa awal <span class="font-normal text-slate-400">(opsional)</span></label><textarea v-model="formData.diagnosis" rows="2" placeholder="Catatan pemeriksaan awal" class="w-full resize-none rounded-xl border border-slate-200 bg-slate-50 px-3 py-3 text-sm outline-none placeholder:text-slate-400 focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-50"></textarea></div>
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2"><div><label class="mb-1.5 block text-sm font-semibold text-slate-700">Status</label><select v-model="formData.status" class="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-3 text-sm outline-none focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-50"><option value="waiting">Menunggu</option><option value="scheduled">Terjadwal</option></select></div><div><label class="mb-1.5 block text-sm font-semibold text-slate-700">Estimasi biaya</label><input v-model.number="formData.total_cost" type="number" min="0" step="1000" placeholder="0" class="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-3 text-sm outline-none focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-50" /></div></div>
          <p v-if="formError" class="rounded-xl bg-rose-50 px-3 py-2 text-sm text-rose-700">{{ formError }}</p>
          <div class="flex gap-3 pt-2"><button type="button" class="flex-1 rounded-xl border border-slate-200 px-4 py-3 text-sm font-bold text-slate-600 hover:bg-slate-50" @click="closeForm">Batal</button><button type="submit" :disabled="serviceStore.loading || !vehicleStore.vehicles.length" class="flex-1 rounded-xl bg-blue-600 px-4 py-3 text-sm font-bold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"><span v-if="serviceStore.loading">Menyimpan...</span><span v-else>Simpan Servis</span></button></div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const serviceStore = useServiceStore()
const vehicleStore = useVehicleStore()
const showForm = ref(false)
const showDetail = ref(false)
const selectedService = ref<any | null>(null)
const formError = ref('')
const formData = ref({
  vehicle_id: 0,
  mechanic_id: null as number | null,
  complaint: '',
  diagnosis: '',
  status: 'waiting',
  total_cost: 0
})

const vehicleLabel = (vehicleId: number) => {
  const vehicle = vehicleStore.vehicles.find((item: any) => item.id === vehicleId)
  return vehicle ? `${vehicle.brand} ${vehicle.model} - ${vehicle.plate_number}` : `Kendaraan #${vehicleId}`
}

const formatDate = (value: string) => new Intl.DateTimeFormat('id-ID', { dateStyle: 'long' }).format(new Date(value))
const formatCurrency = (value: number) => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(value || 0)
const statusLabel = (status: string) => ({ draft: 'Draft', waiting: 'Antrean', in_progress: 'Diproses', scheduled: 'Terjadwal', completed: 'Selesai', cancelled: 'Dibatalkan' }[status] || status)
const statusClass = (status: string) => ({ draft: 'bg-slate-100 text-slate-600', waiting: 'bg-amber-50 text-amber-700', in_progress: 'bg-blue-50 text-blue-700', scheduled: 'bg-indigo-50 text-indigo-700', completed: 'bg-emerald-50 text-emerald-700', cancelled: 'bg-rose-50 text-rose-700' }[status] || 'bg-slate-100 text-slate-600')
const nextStatus = (status: string) => ({ draft: 'waiting', scheduled: 'waiting', waiting: 'in_progress', in_progress: 'completed' }[status] || '')
const nextStatusLabel = (status: string) => ({ draft: 'Masukkan Antrean', scheduled: 'Masukkan Antrean', waiting: 'Mulai Servis', in_progress: 'Selesaikan Servis' }[status] || '')

const openDetail = (service: any) => {
  selectedService.value = service
  showDetail.value = true
}

const closeDetail = () => {
  selectedService.value = null
  showDetail.value = false
}

const advanceService = async (service: any) => {
  const status = nextStatus(service.status)
  if (!status) return
  if (status === 'completed' && !confirm('Tandai servis ini sebagai selesai?')) return

  try {
    await serviceStore.updateServiceStatus(service.id, status)
    if (selectedService.value?.id === service.id) selectedService.value = { ...service, status }
  } catch (error: any) {
    formError.value = error?.data?.detail || 'Status servis gagal diperbarui.'
  }
}

const openForm = () => {
  formError.value = ''
  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
  formError.value = ''
  formData.value = { vehicle_id: 0, mechanic_id: null, complaint: '', diagnosis: '', status: 'waiting', total_cost: 0 }
}

const submitService = async () => {
  formError.value = ''
  try {
    await serviceStore.createService(formData.value)
    closeForm()
  } catch (error: any) {
    formError.value = error?.data?.detail || 'Servis gagal disimpan. Periksa data dan coba lagi.'
  }
}

onMounted(async () => {
  await Promise.all([serviceStore.fetchServices(), vehicleStore.fetchVehicles()])
})
</script>
