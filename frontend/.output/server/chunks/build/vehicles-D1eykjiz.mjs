import { t as components_default } from './components-Cd10hOdb.mjs';
import { u as useVehicleStore } from './vehicles-Dz_Y3onk.mjs';
import { defineComponent, ref, computed, mergeProps, unref, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderComponent, ssrRenderAttr, ssrRenderList, ssrInterpolate, ssrIncludeBooleanAttr, ssrLooseContain, ssrLooseEqual } from 'vue/server-renderer';
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
		const searchQuery = ref("");
		const showForm = ref(false);
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
		return (_ctx, _push, _parent, _attrs) => {
			const _component_Icon = components_default;
			_push(`<div${ssrRenderAttrs(mergeProps({ class: "p-8" }, _attrs))}><div class="flex justify-between items-center mb-6"><h3 class="text-2xl font-bold text-slate-900">Tracking Kendaraan</h3><button class="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:plus",
				class: "w-5 h-5"
			}, null, _parent));
			_push(` Tambah Kendaraan </button></div><div class="mb-6"><input${ssrRenderAttr("value", unref(searchQuery))} type="text" placeholder="Cari kendaraan (plat nomor)..." class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"><!--[-->`);
			ssrRenderList(unref(filteredVehicles), (vehicle) => {
				_push(`<div class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"><div class="flex items-start justify-between mb-4"><div><h4 class="text-lg font-bold text-slate-900">${ssrInterpolate(vehicle.brand)} ${ssrInterpolate(vehicle.model)}</h4><p class="text-sm text-slate-600">${ssrInterpolate(vehicle.year)} • ${ssrInterpolate(vehicle.vehicle_type)}</p></div>`);
				_push(ssrRenderComponent(_component_Icon, {
					name: "lucide:car",
					class: "w-8 h-8 text-blue-500 opacity-40"
				}, null, _parent));
				_push(`</div><div class="space-y-2 mb-4 pb-4 border-b border-slate-200"><p class="text-sm"><span class="text-slate-600">Plat Nomor:</span><span class="font-semibold text-slate-900">${ssrInterpolate(vehicle.plate_number)}</span></p><p class="text-sm"><span class="text-slate-600">Pemilik ID:</span><span class="font-semibold text-slate-900">#${ssrInterpolate(vehicle.customer_id)}</span></p></div><div class="flex gap-2"><button class="flex-1 text-sm bg-blue-50 text-blue-600 px-3 py-2 rounded hover:bg-blue-100 transition"> Lihat Riwayat </button><button class="flex-1 text-sm bg-slate-100 text-slate-700 px-3 py-2 rounded hover:bg-slate-200 transition"> Edit </button></div></div>`);
			});
			_push(`<!--]--></div>`);
			if (unref(showForm)) _push(`<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"><div class="bg-white rounded-lg shadow-lg p-6 w-96"><h3 class="text-lg font-bold text-slate-900 mb-4">Tambah Kendaraan</h3><form class="space-y-4"><div><label class="block text-sm font-medium text-slate-700 mb-1">Merk</label><input${ssrRenderAttr("value", unref(formData).brand)} type="text" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Model</label><input${ssrRenderAttr("value", unref(formData).model)} type="text" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Tahun</label><input${ssrRenderAttr("value", unref(formData).year)} type="number" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Plat Nomor</label><input${ssrRenderAttr("value", unref(formData).plate_number)} type="text" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Tipe Kendaraan</label><select required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"><option value=""${ssrIncludeBooleanAttr(Array.isArray(unref(formData).vehicle_type) ? ssrLooseContain(unref(formData).vehicle_type, "") : ssrLooseEqual(unref(formData).vehicle_type, "")) ? " selected" : ""}>Pilih Tipe</option><option value="Mobil Penumpang"${ssrIncludeBooleanAttr(Array.isArray(unref(formData).vehicle_type) ? ssrLooseContain(unref(formData).vehicle_type, "Mobil Penumpang") : ssrLooseEqual(unref(formData).vehicle_type, "Mobil Penumpang")) ? " selected" : ""}>Mobil Penumpang</option><option value="Mobil Barang"${ssrIncludeBooleanAttr(Array.isArray(unref(formData).vehicle_type) ? ssrLooseContain(unref(formData).vehicle_type, "Mobil Barang") : ssrLooseEqual(unref(formData).vehicle_type, "Mobil Barang")) ? " selected" : ""}>Mobil Barang</option><option value="Motor"${ssrIncludeBooleanAttr(Array.isArray(unref(formData).vehicle_type) ? ssrLooseContain(unref(formData).vehicle_type, "Motor") : ssrLooseEqual(unref(formData).vehicle_type, "Motor")) ? " selected" : ""}>Motor</option></select></div><div><label class="block text-sm font-medium text-slate-700 mb-1">ID Pelanggan</label><input${ssrRenderAttr("value", unref(formData).customer_id)} type="number" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div class="flex gap-3"><button type="submit" class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"> Simpan </button><button type="button" class="flex-1 bg-slate-300 text-slate-900 px-4 py-2 rounded-lg hover:bg-slate-400 transition"> Batal </button></div></form></div></div>`);
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
//# sourceMappingURL=vehicles-D1eykjiz.mjs.map
