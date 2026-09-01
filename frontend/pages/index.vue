<template>
  <div class="p-8">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- Stats Cards -->
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-slate-600 text-sm">Total Pelanggan</p>
            <h3 class="text-3xl font-bold text-slate-900 mt-2">150</h3>
          </div>
          <Icon name="lucide:users" class="w-12 h-12 text-blue-500 opacity-20" />
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-slate-600 text-sm">Kendaraan Terdaftar</p>
            <h3 class="text-3xl font-bold text-slate-900 mt-2">280</h3>
          </div>
          <Icon name="lucide:car" class="w-12 h-12 text-green-500 opacity-20" />
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-slate-600 text-sm">Servis Bulan Ini</p>
            <h3 class="text-3xl font-bold text-slate-900 mt-2">45</h3>
          </div>
          <Icon name="lucide:wrench" class="w-12 h-12 text-orange-500 opacity-20" />
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-slate-600 text-sm">Pendapatan</p>
            <h3 class="text-3xl font-bold text-slate-900 mt-2">Rp 45M</h3>
          </div>
          <Icon name="lucide:trending-up" class="w-12 h-12 text-purple-500 opacity-20" />
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-slate-900 mb-4">Servis Terbaru</h3>
        <div class="space-y-4">
          <div class="flex items-center justify-between pb-4 border-b border-slate-200">
            <div>
              <p class="font-medium text-slate-900">Honda Civic - D 1234 ABC</p>
              <p class="text-sm text-slate-500">Ganti oli dan filter</p>
            </div>
            <span class="text-sm font-semibold text-green-600">Selesai</span>
          </div>
          <div class="flex items-center justify-between pb-4 border-b border-slate-200">
            <div>
              <p class="font-medium text-slate-900">Toyota Avanza - D 5678 DEF</p>
              <p class="text-sm text-slate-500">Perbaikan AC</p>
            </div>
            <span class="text-sm font-semibold text-blue-600">Proses</span>
          </div>
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-slate-900">Suzuki Ertiga - D 9012 GHI</p>
              <p class="text-sm text-slate-500">Service rutin</p>
            </div>
            <span class="text-sm font-semibold text-yellow-600">Menunggu</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-slate-900 mb-4">Suku Cadang Low Stock</h3>
        <div class="space-y-4">
          <div class="flex items-center justify-between pb-4 border-b border-slate-200">
            <div>
              <p class="font-medium text-slate-900">Filter Oli</p>
              <p class="text-sm text-slate-500">Stok: 5 unit</p>
            </div>
            <span class="px-3 py-1 bg-red-100 text-red-700 text-xs font-semibold rounded-full">Kritis</span>
          </div>
          <div class="flex items-center justify-between pb-4 border-b border-slate-200">
            <div>
              <p class="font-medium text-slate-900">Air Filter</p>
              <p class="text-sm text-slate-500">Stok: 8 unit</p>
            </div>
            <span class="px-3 py-1 bg-yellow-100 text-yellow-700 text-xs font-semibold rounded-full">Rendah</span>
          </div>
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-slate-900">Aki 12V</p>
              <p class="text-sm text-slate-500">Stok: 12 unit</p>
            </div>
            <span class="px-3 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded-full">Normal</span>
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
</script>
