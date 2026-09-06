import { u as useRuntimeConfig } from '../virtual/entry.mjs';
import { ref } from 'vue';
import { $ as $fetch } from '../_/nitro.mjs';
import { defineStore } from 'pinia';

//#region stores/vehicles.ts
var useVehicleStore = defineStore("vehicle", () => {
	const config = useRuntimeConfig();
	const vehicles = ref([]);
	const loading = ref(false);
	const error = ref(null);
	const fetchVehicles = async () => {
		loading.value = true;
		try {
			const response = await $fetch(`${config.public.apiBase}/vehicles`);
			vehicles.value = response;
			error.value = null;
		} catch (err) {
			error.value = err.message;
		} finally {
			loading.value = false;
		}
	};
	const createVehicle = async (vehicle) => {
		try {
			const response = await $fetch(`${config.public.apiBase}/vehicles`, {
				method: "POST",
				body: vehicle
			});
			vehicles.value.push(response);
			return response;
		} catch (err) {
			error.value = err.message;
			throw err;
		}
	};
	const searchVehicle = async (plateNumber) => {
		try {
			return await $fetch(`${config.public.apiBase}/vehicles`, { query: { plate_number: plateNumber } });
		} catch (err) {
			error.value = err.message;
			throw err;
		}
	};
	return {
		vehicles,
		loading,
		error,
		fetchVehicles,
		createVehicle,
		searchVehicle
	};
});
//#endregion
//#region stores/services.ts
var useServiceStore = defineStore("service", () => {
	const config = useRuntimeConfig();
	const services = ref([]);
	const loading = ref(false);
	const error = ref(null);
	const fetchServices = async () => {
		loading.value = true;
		try {
			const response = await $fetch(`${config.public.apiBase}/services/`);
			services.value = response;
			error.value = null;
		} catch (err) {
			error.value = err?.message || "Error fetching services";
		} finally {
			loading.value = false;
		}
	};
	const createService = async (service) => {
		loading.value = true;
		try {
			const response = await $fetch(`${config.public.apiBase}/services/`, {
				method: "POST",
				body: service
			});
			services.value.unshift(response);
			error.value = null;
			return response;
		} catch (err) {
			error.value = err?.data?.detail || err?.message || "Error creating service";
			throw err;
		} finally {
			loading.value = false;
		}
	};
	return {
		services,
		loading,
		error,
		fetchServices,
		createService
	};
});

export { useVehicleStore as a, useServiceStore as u };
//# sourceMappingURL=services-a_X5Uxpp.mjs.map
