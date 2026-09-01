import { u as useRuntimeConfig } from '../virtual/entry.mjs';
import { ref } from 'vue';
import { $ as $fetch } from '../_/nitro.mjs';
import { defineStore } from 'pinia';

//#region stores/customers.ts
var useCustomerStore = defineStore("customer", () => {
	const config = useRuntimeConfig();
	const customers = ref([]);
	const loading = ref(false);
	const error = ref(null);
	const fetchCustomers = async () => {
		loading.value = true;
		try {
			const response = await $fetch(`${config.public.apiBase}/customers`);
			customers.value = response;
			error.value = null;
		} catch (err) {
			error.value = err.message;
		} finally {
			loading.value = false;
		}
	};
	const createCustomer = async (customer) => {
		try {
			const response = await $fetch(`${config.public.apiBase}/customers`, {
				method: "POST",
				body: customer
			});
			customers.value.push(response);
			return response;
		} catch (err) {
			error.value = err.message;
			throw err;
		}
	};
	const updateCustomer = async (id, customer) => {
		try {
			const response = await $fetch(`${config.public.apiBase}/customers/${id}`, {
				method: "PUT",
				body: customer
			});
			const index = customers.value.findIndex((c) => c.id === id);
			if (index > -1) customers.value[index] = response;
			return response;
		} catch (err) {
			error.value = err.message;
			throw err;
		}
	};
	const deleteCustomer = async (id) => {
		try {
			await $fetch(`${config.public.apiBase}/customers/${id}`, { method: "DELETE" });
			customers.value = customers.value.filter((c) => c.id !== id);
		} catch (err) {
			error.value = err.message;
			throw err;
		}
	};
	return {
		customers,
		loading,
		error,
		fetchCustomers,
		createCustomer,
		updateCustomer,
		deleteCustomer
	};
});

export { useCustomerStore as u };
//# sourceMappingURL=customers-D_qYtUuR.mjs.map
