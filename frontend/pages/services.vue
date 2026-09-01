<template>
  <div class="p-8">
    <h3 class="text-2xl font-bold text-slate-900 mb-6">Riwayat Servis</h3>

    <!-- Timeline -->
    <div class="max-w-4xl">
      <div v-for="(service, index) in services" :key="index" class="flex gap-6 mb-8">
        <div class="flex flex-col items-center">
          <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
            <Icon name="lucide:wrench" class="w-6 h-6 text-blue-600" />
          </div>
          <div v-if="index < services.length - 1" class="w-1 h-24 bg-blue-100 my-2"></div>
        </div>

        <div class="flex-1 pb-6">
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex justify-between items-start mb-3">
              <div>
                <h4 class="text-lg font-bold text-slate-900">{{ service.vehicle }}</h4>
                <p class="text-sm text-slate-600">{{ service.plate }}</p>
              </div>
              <span :class="`px-3 py-1 text-xs font-semibold rounded-full ${service.statusColor}`">
                {{ service.status }}
              </span>
            </div>

            <p class="text-slate-700 mb-4">{{ service.description }}</p>

            <div class="grid grid-cols-2 gap-4 mb-4 pb-4 border-b border-slate-200">
              <div>
                <p class="text-sm text-slate-600">Tanggal Servis</p>
                <p class="font-semibold text-slate-900">{{ service.date }}</p>
              </div>
              <div>
                <p class="text-sm text-slate-600">Biaya</p>
                <p class="font-semibold text-slate-900">{{ service.cost }}</p>
              </div>
            </div>

            <div class="flex gap-2">
              <button class="text-sm text-blue-600 hover:text-blue-700 font-medium">Lihat Detail</button>
              <button class="text-sm text-slate-600 hover:text-slate-700 font-medium">Cetak Invoice</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

const services = ref([
  {
    vehicle: 'Honda Civic',
    plate: 'D 1234 ABC',
    description: 'Ganti oli, filter udara, dan pemeriksaan sistem pengereman',
    date: '15 Agustus 2026',
    cost: 'Rp 450.000',
    status: 'Selesai',
    statusColor: 'bg-green-100 text-green-700'
  },
  {
    vehicle: 'Toyota Avanza',
    plate: 'D 5678 DEF',
    description: 'Perbaikan sistem AC dan isi freon',
    date: '12 Agustus 2026',
    cost: 'Rp 600.000',
    status: 'Selesai',
    statusColor: 'bg-green-100 text-green-700'
  },
  {
    vehicle: 'Suzuki Ertiga',
    plate: 'D 9012 GHI',
    description: 'Service rutin dan penggantian kampas rem',
    date: '10 Agustus 2026',
    cost: 'Rp 750.000',
    status: 'Selesai',
    statusColor: 'bg-green-100 text-green-700'
  }
])
</script>
