import { t as components_default } from './components-Bfu6e32q.mjs';
import { a as useVehicleStore, u as useServiceStore } from './services-a_X5Uxpp.mjs';
import { defineComponent, ref, computed, mergeProps, unref, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderComponent, ssrRenderAttr, ssrRenderList, ssrInterpolate, ssrRenderClass, ssrIncludeBooleanAttr, ssrLooseContain, ssrLooseEqual } from 'vue/server-renderer';
import '../virtual/entry.mjs';
import 'nostics';
import 'nostics/formatters/ansi';
import 'unhead/utils';
import '../routes/renderer.mjs';
import '../_/nitro.mjs';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:path';
import 'node:crypto';
import 'node:url';
import '@iconify/utils';
import 'consola';
import 'unhead/server';
import 'unhead/legacy';
import 'unhead/plugins';
import 'vue-bundle-renderer/runtime';
import 'devalue';
import 'vue-router';
import '@vue/shared';
import 'pinia';
import '@iconify/vue';
import 'tailwindcss/colors';
import '@iconify/utils/lib/css/icon';

//#region pages/vehicles.vue?vue&type=script&setup=true&lang.ts
var vehicles_vue_vue_type_script_setup_true_lang_default = /*@__PURE__*/ defineComponent({
	__name: "vehicles",
	__ssrInlineRender: true,
	setup(__props) {
		const vehicleStore = useVehicleStore();
		const serviceStore = useServiceStore();
		const searchQuery = ref("");
		const showForm = ref(false);
		const showHistory = ref(false);
		const selectedVehicle = ref(null);
		const formData = ref({
			brand: "",
			model: "",
			year: (/* @__PURE__ */ new Date()).getFullYear(),
			plate_number: "",
			vehicle_type: "",
			customer_id: 0
		});
		const filteredVehicles = computed(() => {
			return vehicleStore.vehicles.filter((vehicle) => vehicle.plate_number.toLowerCase().includes(searchQuery.value.toLowerCase()) || `${vehicle.brand} ${vehicle.model}`.toLowerCase().includes(searchQuery.value.toLowerCase()));
		});
		const vehicleHistory = computed(() => selectedVehicle.value ? serviceStore.services.filter((service) => service.vehicle_id === selectedVehicle.value.id) : []);
		const statusLabel = (status) => ({
			waiting: "Menunggu",
			in_progress: "Dikerjakan",
			scheduled: "Terjadwal",
			completed: "Selesai",
			cancelled: "Dibatalkan"
		})[status] || status;
		const statusClass = (status) => ({
			waiting: "bg-amber-50 text-amber-700",
			in_progress: "bg-blue-50 text-blue-700",
			scheduled: "bg-indigo-50 text-indigo-700",
			completed: "bg-emerald-50 text-emerald-700",
			cancelled: "bg-rose-50 text-rose-700"
		})[status] || "bg-slate-100 text-slate-600";
		const formatDate = (value) => new Intl.DateTimeFormat("id-ID", { dateStyle: "long" }).format(new Date(value));
		const formatCurrency = (value) => new Intl.NumberFormat("id-ID", {
			style: "currency",
			currency: "IDR",
			maximumFractionDigits: 0
		}).format(value || 0);
		return (_ctx, _push, _parent, _attrs) => {
			const _component_Icon = components_default;
			_push(`<div${ssrRenderAttrs(mergeProps({ class: "space-y-6" }, _attrs))}><div class="flex flex-col justify-between gap-4 md:flex-row md:items-end"><div><p class="mb-2 text-sm font-semibold text-blue-600">Fleet pelanggan</p><h2 class="text-3xl font-extrabold tracking-tight text-slate-900">Kendaraan</h2><p class="mt-2 text-sm text-slate-500">Kelola seluruh kendaraan yang terdaftar di bengkel.</p></div><button class="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 text-sm font-bold text-white shadow-sm hover:bg-blue-700">`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:plus",
				class: "w-5 h-5"
			}, null, _parent));
			_push(` Tambah Kendaraan </button></div><div class="relative rounded-2xl border border-slate-200 bg-white p-3 shadow-[0_4px_20px_rgb(15_23_42/0.03)]">`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:search",
				class: "absolute left-6 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
			}, null, _parent));
			_push(`<input${ssrRenderAttr("value", unref(searchQuery))} type="text" placeholder="Cari kendaraan (plat nomor)..." class="w-full rounded-xl border-0 bg-slate-50 py-3 pl-10 pr-4 text-sm outline-none placeholder:text-slate-400 focus:bg-white focus:ring-2 focus:ring-blue-100"></div><div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"><!--[-->`);
			ssrRenderList(unref(filteredVehicles), (vehicle) => {
				_push(`<div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-[0_4px_20px_rgb(15_23_42/0.03)] transition hover:-translate-y-0.5 hover:shadow-md"><div class="flex items-start justify-between mb-4"><div><h4 class="text-lg font-bold text-slate-900">${ssrInterpolate(vehicle.brand)} ${ssrInterpolate(vehicle.model)}</h4><p class="text-sm text-slate-600">${ssrInterpolate(vehicle.year)} • ${ssrInterpolate(vehicle.vehicle_type)}</p></div>`);
				_push(ssrRenderComponent(_component_Icon, {
					name: "lucide:car",
					class: "w-8 h-8 text-blue-500 opacity-40"
				}, null, _parent));
				_push(`</div><div class="space-y-2 mb-4 pb-4 border-b border-slate-200"><p class="text-sm"><span class="text-slate-600">Plat Nomor:</span><span class="font-semibold text-slate-900">${ssrInterpolate(vehicle.plate_number)}</span></p><p class="text-sm"><span class="text-slate-600">Pemilik ID:</span><span class="font-semibold text-slate-900">#${ssrInterpolate(vehicle.customer_id)}</span></p></div><div class="flex gap-2"><button class="flex-1 text-sm bg-blue-50 text-blue-600 px-3 py-2 rounded hover:bg-blue-100 transition"> Lihat Riwayat </button><button class="flex-1 text-sm bg-slate-100 text-slate-700 px-3 py-2 rounded hover:bg-slate-200 transition"> Edit </button></div></div>`);
			});
			_push(`<!--]--></div>`);
			if (unref(showHistory)) {
				_push(`<div class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4 backdrop-blur-sm"><div class="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl"><div class="mb-6 flex items-start justify-between"><div><p class="text-xs font-semibold text-blue-600">Riwayat kendaraan</p><h3 class="mt-1 text-xl font-extrabold text-slate-900">${ssrInterpolate(unref(selectedVehicle)?.brand)} ${ssrInterpolate(unref(selectedVehicle)?.model)}</h3><p class="mt-1 text-sm text-slate-500">${ssrInterpolate(unref(selectedVehicle)?.plate_number)} · ${ssrInterpolate(unref(selectedVehicle)?.year)}</p></div><button class="rounded-lg p-2 text-slate-400 hover:bg-slate-100" aria-label="Tutup">`);
				_push(ssrRenderComponent(_component_Icon, {
					name: "lucide:x",
					class: "h-5 w-5"
				}, null, _parent));
				_push(`</button></div>`);
				if (unref(vehicleHistory).length) {
					_push(`<div class="space-y-3"><!--[-->`);
					ssrRenderList(unref(vehicleHistory), (service) => {
						_push(`<div class="rounded-xl border border-slate-200 bg-slate-50 p-4"><div class="flex items-start justify-between gap-3"><div><p class="text-sm font-bold text-slate-900">${ssrInterpolate(service.complaint)}</p><p class="mt-1 text-xs text-slate-500">${ssrInterpolate(formatDate(service.created_at))} · Servis #${ssrInterpolate(service.id)}</p></div><span class="${ssrRenderClass([statusClass(service.status), "shrink-0 rounded-full px-2.5 py-1 text-[10px] font-bold"])}">${ssrInterpolate(statusLabel(service.status))}</span></div><div class="mt-3 text-sm font-semibold text-slate-700">${ssrInterpolate(formatCurrency(service.total_cost))}</div></div>`);
					});
					_push(`<!--]--></div>`);
				} else {
					_push(`<div class="rounded-xl border border-dashed border-slate-300 p-8 text-center">`);
					_push(ssrRenderComponent(_component_Icon, {
						name: "lucide:history",
						class: "mx-auto h-6 w-6 text-slate-400"
					}, null, _parent));
					_push(`<p class="mt-3 text-sm font-bold text-slate-700">Belum ada riwayat servis</p><p class="mt-1 text-xs text-slate-500">Belum ada order servis untuk kendaraan ini.</p></div>`);
				}
				_push(`</div></div>`);
			} else _push(`<!---->`);
			if (unref(showForm)) _push(`<div class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4 backdrop-blur-sm"><div class="max-h-[90vh] w-full max-w-md overflow-y-auto rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl"><h3 class="text-lg font-bold text-slate-900 mb-4">Tambah Kendaraan</h3><form class="space-y-4"><div><label class="block text-sm font-medium text-slate-700 mb-1">Merk</label><input${ssrRenderAttr("value", unref(formData).brand)} type="text" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Model</label><input${ssrRenderAttr("value", unref(formData).model)} type="text" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Tahun</label><input${ssrRenderAttr("value", unref(formData).year)} type="number" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Plat Nomor</label><input${ssrRenderAttr("value", unref(formData).plate_number)} type="text" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Tipe Kendaraan</label><select required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"><option value=""${ssrIncludeBooleanAttr(Array.isArray(unref(formData).vehicle_type) ? ssrLooseContain(unref(formData).vehicle_type, "") : ssrLooseEqual(unref(formData).vehicle_type, "")) ? " selected" : ""}>Pilih Tipe</option><option value="Mobil Penumpang"${ssrIncludeBooleanAttr(Array.isArray(unref(formData).vehicle_type) ? ssrLooseContain(unref(formData).vehicle_type, "Mobil Penumpang") : ssrLooseEqual(unref(formData).vehicle_type, "Mobil Penumpang")) ? " selected" : ""}>Mobil Penumpang</option><option value="Mobil Barang"${ssrIncludeBooleanAttr(Array.isArray(unref(formData).vehicle_type) ? ssrLooseContain(unref(formData).vehicle_type, "Mobil Barang") : ssrLooseEqual(unref(formData).vehicle_type, "Mobil Barang")) ? " selected" : ""}>Mobil Barang</option><option value="Motor"${ssrIncludeBooleanAttr(Array.isArray(unref(formData).vehicle_type) ? ssrLooseContain(unref(formData).vehicle_type, "Motor") : ssrLooseEqual(unref(formData).vehicle_type, "Motor")) ? " selected" : ""}>Motor</option></select></div><div><label class="block text-sm font-medium text-slate-700 mb-1">ID Pelanggan</label><input${ssrRenderAttr("value", unref(formData).customer_id)} type="number" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div class="flex gap-3"><button type="submit" class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"> Simpan </button><button type="button" class="flex-1 bg-slate-300 text-slate-900 px-4 py-2 rounded-lg hover:bg-slate-400 transition"> Batal </button></div></form></div></div>`);
			else _push(`<!---->`);
			_push(`</div>`);
		};
	}
});
//#endregion
//#region pages/vehicles.vue
var _sfc_setup = vehicles_vue_vue_type_script_setup_true_lang_default.setup;
vehicles_vue_vue_type_script_setup_true_lang_default.setup = (props, ctx) => {
	const ssrContext = useSSRContext();
	(ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/vehicles.vue");
	return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
var vehicles_default = vehicles_vue_vue_type_script_setup_true_lang_default;

export { vehicles_default as default };
//# sourceMappingURL=vehicles-DD5IDuD0.mjs.map
