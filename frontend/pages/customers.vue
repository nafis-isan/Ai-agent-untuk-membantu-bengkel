<template>
  <div class="p-8">
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-2xl font-bold text-slate-900">Daftar Pelanggan</h3>
      <button
        @click="showForm = true"
        class="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
      >
        <Icon name="lucide:plus" class="w-5 h-5" />
        Tambah Pelanggan
      </button>
    </div>

    <!-- Search Bar -->
    <div class="mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Cari pelanggan..."
        class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Loading State -->
    <div v-if="customerStore.loading" class="text-center py-8">
      <p class="text-slate-600">Memuat data...</p>
    </div>

    <!-- Customers Table -->
    <div v-else class="bg-white rounded-lg shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-slate-50 border-b border-slate-200">
          <tr>
            <th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Nama</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">No. Telepon</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Email</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Alamat</th>
            <th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200">
          <tr v-for="customer in filteredCustomers" :key="customer.id" class="hover:bg-slate-50">
            <td class="px-6 py-4 text-sm text-slate-900">{{ customer.name }}</td>
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
    <div v-if="showForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-96">
        <h3 class="text-lg font-bold text-slate-900 mb-4">
          {{ editingId ? 'Edit Pelanggan' : 'Tambah Pelanggan' }}
        </h3>

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
