<template>
  <div class="space-y-6">
    <div class="flex flex-col justify-between gap-4 md:flex-row md:items-end">
      <div><p class="mb-2 text-sm font-semibold text-blue-600">Database pelanggan</p><h2 class="text-3xl font-extrabold tracking-tight text-slate-900">Daftar Pelanggan</h2><p class="mt-2 text-sm text-slate-500">Kelola data pelanggan dan hubungan kendaraan mereka.</p></div>
      <button
        @click="showForm = true"
        class="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 text-sm font-bold text-white shadow-sm hover:bg-blue-700"
      >
        <Icon name="lucide:plus" class="w-5 h-5" />
        Tambah Pelanggan
      </button>
    </div>

    <div class="rounded-2xl border border-slate-200 bg-white p-3 shadow-[0_4px_20px_rgb(15_23_42/0.03)]">
      <div class="relative">
        <Icon name="lucide:search" class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Cari pelanggan..."
        class="w-full rounded-xl border-0 bg-slate-50 py-3 pl-10 pr-4 text-sm text-slate-800 outline-none ring-0 placeholder:text-slate-400 focus:bg-white focus:ring-2 focus:ring-blue-100"
      />
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="customerStore.loading" class="text-center py-8">
      <p class="text-slate-600">Memuat data...</p>
    </div>

    <!-- Customers Table -->
    <div v-else class="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-[0_4px_20px_rgb(15_23_42/0.03)]">
      <table class="w-full min-w-[760px]">
        <thead class="border-b border-slate-100 bg-slate-50/80">
          <tr>
            <th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Nama</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">No. Telepon</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Email</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Alamat</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200">
          <tr v-for="customer in filteredCustomers" :key="customer.id" class="transition hover:bg-slate-50">
            <td class="px-6 py-4 text-sm font-bold text-slate-900">{{ customer.name }}</td>
            <td class="px-6 py-4 text-sm text-slate-600">{{ customer.phone }}</td>
            <td class="px-6 py-4 text-sm text-slate-600">{{ customer.email }}</td>
            <td class="px-6 py-4 text-sm text-slate-600">{{ customer.address }}</td>
            <td class="px-6 py-4 text-sm">
              <button
                @click="editCustomer(customer)"
                class="text-blue-600 hover:text-blue-700 mr-4"
              >
                Edit
              </button>
              <button
                @click="deleteCustomerHandler(customer.id)"
                class="text-red-600 hover:text-red-700"
              >
                Hapus
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Form Modal -->
    <div v-if="showForm" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4 backdrop-blur-sm">
      <div class="max-h-[90vh] w-full max-w-md overflow-y-auto rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl">
        <div class="mb-5 flex items-start justify-between"><div><p class="text-xs font-semibold text-blue-600">Data pelanggan</p><h3 class="mt-1 text-xl font-extrabold text-slate-900">
          {{ editingId ? 'Edit Pelanggan' : 'Tambah Pelanggan' }}
        </h3></div><button @click="closeForm" class="rounded-lg p-2 text-slate-400 hover:bg-slate-100" aria-label="Tutup"><Icon name="lucide:x" class="h-5 w-5" /></button></div>

        <form @submit.prevent="submitForm" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Nama</label>
            <input
              v-model="formData.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">No. Telepon</label>
            <input
              v-model="formData.phone"
              type="tel"
              required
              class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Email</label>
            <input
              v-model="formData.email"
              type="email"
              class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Alamat</label>
            <textarea
              v-model="formData.address"
              class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            ></textarea>
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
              @click="closeForm"
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

const customerStore = useCustomerStore()
const searchQuery = ref('')
const showForm = ref(false)
const editingId = ref(null)

const formData = ref({
  name: '',
  phone: '',
  email: '',
  address: ''
})

const filteredCustomers = computed(() => {
  return customerStore.customers.filter(customer =>
    customer.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    customer.phone.includes(searchQuery.value)
  )
})

onMounted(() => {
  customerStore.fetchCustomers()
})

const submitForm = async () => {
  try {
    if (editingId.value) {
      await customerStore.updateCustomer(editingId.value, formData.value)
    } else {
      await customerStore.createCustomer(formData.value)
    }
    closeForm()
  } catch (error) {
    console.error('Error:', error)
  }
}

const editCustomer = (customer: any) => {
  editingId.value = customer.id
  formData.value = { ...customer }
  showForm.value = true
}

const deleteCustomerHandler = async (id: number) => {
  if (confirm('Apakah Anda yakin ingin menghapus pelanggan ini?')) {
    try {
      await customerStore.deleteCustomer(id)
    } catch (error) {
      console.error('Error:', error)
    }
  }
}

const closeForm = () => {
  showForm.value = false
  editingId.value = null
  formData.value = { name: '', phone: '', email: '', address: '' }
}
</script>
