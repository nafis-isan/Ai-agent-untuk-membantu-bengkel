<template>
  <div class="p-8">
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-2xl font-bold text-slate-900">Manajemen Suku Cadang</h3>
      <button
        @click="showForm = true"
        class="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
      >
        <Icon name="lucide:plus" class="w-5 h-5" />
        Tambah Suku Cadang
      </button>
    </div>

    <div class="mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Cari suku cadang..."
        class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <div v-if="sparepartStore.loading" class="text-center py-8">
      <p class="text-slate-600">Memuat data...</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="part in filteredParts"
        :key="part.id"
        class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
      >
        <div class="flex items-start justify-between mb-4">
          <div>
            <h4 class="text-lg font-bold text-slate-900">{{ part.name }}</h4>
            <p class="text-sm text-slate-600">{{ part.part_number }}</p>
          </div>
          <Icon name="lucide:package" class="w-8 h-8 text-orange-500 opacity-40" />
        </div>

        <div class="space-y-2 mb-4 pb-4 border-b border-slate-200">
          <p class="text-sm">
            <span class="text-slate-600">Merk:</span>
            <span class="font-semibold text-slate-900">{{ part.brand || '-' }}</span>
          </p>
          <p class="text-sm">
            <span class="text-slate-600">Harga:</span>
            <span class="font-semibold text-slate-900">Rp {{ Number(part.price).toLocaleString('id-ID') }}</span>
          </p>
          <p class="text-sm">
            <span class="text-slate-600">Stok:</span>
            <span :class="`font-semibold ${getStockColor(part.stock, part.minimum_stock)}`">
              {{ part.stock }} unit
            </span>
          </p>
        </div>

        <div class="flex gap-2">
          <button
            @click="editPart(part)"
            class="flex-1 text-sm bg-blue-50 text-blue-600 px-3 py-2 rounded hover:bg-blue-100 transition"
          >
            Edit
          </button>
          <button
            @click="deletePartHandler(part.id)"
            class="flex-1 text-sm bg-slate-100 text-slate-700 px-3 py-2 rounded hover:bg-slate-200 transition"
          >
            Hapus
          </button>
        </div>
      </div>
    </div>

    <div v-if="showForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-96">
        <h3 class="text-lg font-bold text-slate-900 mb-4">
          {{ editingId ? 'Edit Suku Cadang' : 'Tambah Suku Cadang' }}
        </h3>

        <form @submit.prevent="submitForm" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Nomor Part</label>
            <input v-model="formData.part_number" type="text" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Nama</label>
            <input v-model="formData.name" type="text" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Merk</label>
            <input v-model="formData.brand" type="text" class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Harga</label>
            <input v-model.number="formData.price" type="number" min="0" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Stok</label>
              <input v-model.number="formData.stock" type="number" min="0" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Minimum</label>
              <input v-model.number="formData.minimum_stock" type="number" min="0" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
          </div>

          <div class="flex gap-3">
            <button type="submit" class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">Simpan</button>
            <button type="button" @click="closeForm" class="flex-1 bg-slate-300 text-slate-900 px-4 py-2 rounded-lg hover:bg-slate-400 transition">Batal</button>
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

const sparepartStore = useSparepartStore()
const searchQuery = ref('')
const showForm = ref(false)
const editingId = ref<number | null>(null)

const emptyForm = () => ({
  part_number: '',
  name: '',
  brand: '',
  price: 0,
  stock: 0,
  minimum_stock: 0
})

const formData = ref(emptyForm())

const filteredParts = computed(() => {
  return sparepartStore.spareparts.filter(part =>
    part.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    part.part_number.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

onMounted(() => {
  sparepartStore.fetchSpareparts()
})

const submitForm = async () => {
  try {
    if (editingId.value) {
      await sparepartStore.updateSparepart(editingId.value, formData.value)
    } else {
      await sparepartStore.createSparepart(formData.value)
    }
    closeForm()
  } catch (error) {
    console.error('Error:', error)
  }
}

const editPart = (part: any) => {
  editingId.value = part.id
  formData.value = { ...part }
  showForm.value = true
}

const deletePartHandler = async (id: number) => {
  if (confirm('Apakah Anda yakin ingin menghapus suku cadang ini?')) {
    try {
      await sparepartStore.deleteSparepart(id)
    } catch (error) {
      console.error('Error:', error)
    }
  }
}

const closeForm = () => {
  showForm.value = false
  editingId.value = null
  formData.value = emptyForm()
}

const getStockColor = (stock: number, minimum: number) => {
  if (stock < minimum) return 'text-red-600'
  if (stock < minimum + 5) return 'text-yellow-600'
  return 'text-green-600'
}
</script>
