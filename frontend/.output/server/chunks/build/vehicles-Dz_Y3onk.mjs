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

export { useVehicleStore as u };
//# sourceMappingURL=vehicles-Dz_Y3onk.mjs.map
