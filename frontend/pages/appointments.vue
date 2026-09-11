<template>
  <div class="space-y-6">
    <div class="flex flex-col justify-between gap-4 md:flex-row md:items-end">
      <div><p class="mb-2 text-sm font-semibold text-blue-600">Jadwal bengkel</p><h2 class="text-3xl font-extrabold tracking-tight text-slate-900">Appointment</h2><p class="mt-2 text-sm text-slate-500">Atur jadwal kedatangan pelanggan sebelum servis dimulai.</p></div>
      <button class="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 text-sm font-bold text-white hover:bg-blue-700" @click="showForm = true"><Icon name="lucide:calendar-plus" class="h-4 w-4" />Buat Appointment</button>
    </div>

    <div v-if="appointmentStore.error" class="rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">{{ appointmentStore.error }}</div>
    <div v-if="appointmentStore.loading && !appointmentStore.appointments.length" class="h-40 animate-pulse rounded-2xl bg-white" />
    <div v-else-if="!appointmentStore.appointments.length" class="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center"><Icon name="lucide:calendar-days" class="mx-auto h-8 w-8 text-slate-400" /><p class="mt-3 font-bold text-slate-800">Belum ada appointment</p></div>
    <div v-else class="overflow-hidden rounded-2xl border border-slate-200 bg-white"><div v-for="item in appointmentStore.appointments" :key="item.id" class="flex flex-col justify-between gap-4 border-b border-slate-100 p-5 last:border-0 md:flex-row md:items-center"><div><p class="font-bold text-slate-900">{{ vehicleLabel(item.vehicle_id) }}</p><p class="mt-1 text-sm text-slate-500">{{ item.complaint }}</p><p class="mt-1 text-xs text-slate-400">{{ formatDate(item.scheduled_at) }}</p></div><div class="flex items-center gap-3"><span class="rounded-full px-3 py-1 text-xs font-bold" :class="statusClass(item.status)">{{ item.status }}</span><button v-if="item.status === 'scheduled'" class="rounded-lg bg-emerald-600 px-3 py-2 text-xs font-bold text-white hover:bg-emerald-700" @click="confirmAppointment(item.id)">Konfirmasi</button><button v-if="['scheduled', 'confirmed'].includes(item.status)" class="rounded-lg bg-rose-50 px-3 py-2 text-xs font-bold text-rose-700 hover:bg-rose-100" @click="cancelAppointment(item.id)">Batalkan</button></div></div></div>

    <div v-if="showForm" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4"><div class="w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl"><div class="mb-5 flex items-start justify-between"><div><p class="text-xs font-semibold text-blue-600">Jadwal baru</p><h3 class="mt-1 text-xl font-extrabold text-slate-900">Buat Appointment</h3></div><button aria-label="Tutup" class="rounded-lg p-2 text-slate-400 hover:bg-slate-100" @click="showForm = false"><Icon name="lucide:x" /></button></div><form class="space-y-4" @submit.prevent="submitForm"><label class="block text-sm font-semibold text-slate-700">Pelanggan<select v-model.number="form.customer_id" required class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-3"><option :value="0" disabled>Pilih pelanggan</option><option v-for="customer in customerStore.customers" :key="customer.id" :value="customer.id">{{ customer.name }} - {{ customer.phone }}</option></select></label><label class="block text-sm font-semibold text-slate-700">Kendaraan<select v-model.number="form.vehicle_id" required class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-3"><option :value="0" disabled>Pilih kendaraan</option><option v-for="vehicle in vehicleStore.vehicles" :key="vehicle.id" :value="vehicle.id">{{ vehicle.brand }} {{ vehicle.model }} - {{ vehicle.plate_number }}</option></select></label><label class="block text-sm font-semibold text-slate-700">Waktu<input v-model="form.scheduled_at" type="datetime-local" required class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-3" /></label><label class="block text-sm font-semibold text-slate-700">Keluhan<textarea v-model="form.complaint" required rows="3" class="mt-1 w-full rounded-xl border border-slate-200 px-3 py-3" placeholder="Keluhan pelanggan" /></label><div class="flex gap-3"><button type="button" class="flex-1 rounded-xl border border-slate-200 px-4 py-3 font-bold" @click="showForm = false">Batal</button><button type="submit" :disabled="appointmentStore.loading" class="flex-1 rounded-xl bg-blue-600 px-4 py-3 font-bold text-white disabled:bg-slate-300">Simpan</button></div></form></div></div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'default' })
const appointmentStore = useAppointmentStore()
const customerStore = useCustomerStore()
const vehicleStore = useVehicleStore()
const showForm = ref(false)
const form = ref({ customer_id: 0, vehicle_id: 0, scheduled_at: '', complaint: '', status: 'scheduled' })
const vehicleLabel = (id: number) => { const item = vehicleStore.vehicles.find((vehicle: any) => vehicle.id === id); return item ? `${item.brand} ${item.model} - ${item.plate_number}` : `Kendaraan #${id}` }
const formatDate = (value: string) => new Intl.DateTimeFormat('id-ID', { dateStyle: 'full', timeStyle: 'short' }).format(new Date(value))
const statusClass = (status: string) => ({ scheduled: 'bg-amber-50 text-amber-700', confirmed: 'bg-emerald-50 text-emerald-700', cancelled: 'bg-rose-50 text-rose-700', completed: 'bg-blue-50 text-blue-700' }[status] || 'bg-slate-100 text-slate-600')
const submitForm = async () => { await appointmentStore.createAppointment({ ...form.value, scheduled_at: new Date(form.value.scheduled_at).toISOString() }); showForm.value = false; form.value = { customer_id: 0, vehicle_id: 0, scheduled_at: '', complaint: '', status: 'scheduled' } }
const confirmAppointment = async (id: number) => { await appointmentStore.updateStatus(id, 'confirmed') }
const cancelAppointment = async (id: number) => { if (confirm('Batalkan appointment ini?')) await appointmentStore.updateStatus(id, 'cancelled') }
onMounted(async () => { await Promise.all([appointmentStore.fetchAppointments(), customerStore.fetchCustomers(), vehicleStore.fetchVehicles()]) })
</script>
