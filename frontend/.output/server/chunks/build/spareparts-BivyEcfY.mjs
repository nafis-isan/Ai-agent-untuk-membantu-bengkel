import { t as components_default } from './components-Cd10hOdb.mjs';
import { u as useRuntimeConfig } from '../virtual/entry.mjs';
import { defineComponent, ref, computed, mergeProps, unref, useSSRContext } from 'vue';
import { $ as $fetch } from '../_/nitro.mjs';
import { defineStore } from 'pinia';
import { ssrRenderAttrs, ssrRenderComponent, ssrRenderAttr, ssrRenderList, ssrInterpolate, ssrRenderClass } from 'vue/server-renderer';
import '@iconify/vue';
import '@iconify/utils/lib/css/icon';
import 'nostics';
import 'nostics/formatters/ansi';
import 'unhead/utils';
import '../routes/renderer.mjs';
import 'unhead/server';
import 'unhead/legacy';
import 'unhead/plugins';
import 'vue-bundle-renderer/runtime';
import 'devalue';
import 'vue-router';
import '@vue/shared';
import 'tailwindcss/colors';
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

//#region stores/spareparts.ts
var useSparepartStore = defineStore("sparepart", () => {
	const config = useRuntimeConfig();
	const spareparts = ref([]);
	const loading = ref(false);
	const error = ref(null);
	const fetchSpareparts = async () => {
		loading.value = true;
		try {
			const response = await $fetch(`${config.public.apiBase}/spareparts/`);
			spareparts.value = response;
			error.value = null;
		} catch (err) {
			error.value = err?.message || "Error fetching spareparts";
		} finally {
			loading.value = false;
		}
	};
	const createSparepart = async (sparepart) => {
		try {
			const response = await $fetch(`${config.public.apiBase}/spareparts/`, {
				method: "POST",
				body: sparepart
			});
			spareparts.value.push(response);
			return response;
		} catch (err) {
			error.value = err?.message || "Error creating sparepart";
			throw err;
		}
	};
	const updateSparepart = async (id, sparepart) => {
		try {
			const response = await $fetch(`${config.public.apiBase}/spareparts/${id}`, {
				method: "PUT",
				body: sparepart
			});
			const index = spareparts.value.findIndex((item) => item.id === id);
			if (index > -1) spareparts.value[index] = response;
			return response;
		} catch (err) {
			error.value = err?.message || "Error updating sparepart";
			throw err;
		}
	};
	const deleteSparepart = async (id) => {
		try {
			await $fetch(`${config.public.apiBase}/spareparts/${id}`, { method: "DELETE" });
			spareparts.value = spareparts.value.filter((item) => item.id !== id);
		} catch (err) {
			error.value = err?.message || "Error deleting sparepart";
			throw err;
		}
	};
	return {
		spareparts,
		loading,
		error,
		fetchSpareparts,
		createSparepart,
		updateSparepart,
		deleteSparepart
	};
});
//#endregion
//#region pages/spareparts.vue?vue&type=script&setup=true&lang.ts
var spareparts_vue_vue_type_script_setup_true_lang_default = /*@__PURE__*/ defineComponent({
	__name: "spareparts",
	__ssrInlineRender: true,
	setup(__props) {
		const sparepartStore = useSparepartStore();
		const searchQuery = ref("");
		const showForm = ref(false);
		const editingId = ref(null);
		const emptyForm = () => ({
			part_number: "",
			name: "",
			brand: "",
			price: 0,
			stock: 0,
			minimum_stock: 0
		});
		const formData = ref(emptyForm());
		const filteredParts = computed(() => {
			return sparepartStore.spareparts.filter((part) => part.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || part.part_number.toLowerCase().includes(searchQuery.value.toLowerCase()));
		});
		const getStockColor = (stock, minimum) => {
			if (stock < minimum) return "text-red-600";
			if (stock < minimum + 5) return "text-yellow-600";
			return "text-green-600";
		};
		return (_ctx, _push, _parent, _attrs) => {
			const _component_Icon = components_default;
			_push(`<div${ssrRenderAttrs(mergeProps({ class: "p-8" }, _attrs))}><div class="flex justify-between items-center mb-6"><h3 class="text-2xl font-bold text-slate-900">Manajemen Suku Cadang</h3><button class="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:plus",
				class: "w-5 h-5"
			}, null, _parent));
			_push(` Tambah Suku Cadang </button></div><div class="mb-6"><input${ssrRenderAttr("value", unref(searchQuery))} type="text" placeholder="Cari suku cadang..." class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div>`);
			if (unref(sparepartStore).loading) _push(`<div class="text-center py-8"><p class="text-slate-600">Memuat data...</p></div>`);
			else {
				_push(`<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"><!--[-->`);
				ssrRenderList(unref(filteredParts), (part) => {
					_push(`<div class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"><div class="flex items-start justify-between mb-4"><div><h4 class="text-lg font-bold text-slate-900">${ssrInterpolate(part.name)}</h4><p class="text-sm text-slate-600">${ssrInterpolate(part.part_number)}</p></div>`);
					_push(ssrRenderComponent(_component_Icon, {
						name: "lucide:package",
						class: "w-8 h-8 text-orange-500 opacity-40"
					}, null, _parent));
					_push(`</div><div class="space-y-2 mb-4 pb-4 border-b border-slate-200"><p class="text-sm"><span class="text-slate-600">Merk:</span><span class="font-semibold text-slate-900">${ssrInterpolate(part.brand || "-")}</span></p><p class="text-sm"><span class="text-slate-600">Harga:</span><span class="font-semibold text-slate-900">Rp ${ssrInterpolate(Number(part.price).toLocaleString("id-ID"))}</span></p><p class="text-sm"><span class="text-slate-600">Stok:</span><span class="${ssrRenderClass(`font-semibold ${getStockColor(part.stock, part.minimum_stock)}`)}">${ssrInterpolate(part.stock)} unit </span></p></div><div class="flex gap-2"><button class="flex-1 text-sm bg-blue-50 text-blue-600 px-3 py-2 rounded hover:bg-blue-100 transition"> Edit </button><button class="flex-1 text-sm bg-slate-100 text-slate-700 px-3 py-2 rounded hover:bg-slate-200 transition"> Hapus </button></div></div>`);
				});
				_push(`<!--]--></div>`);
			}
			if (unref(showForm)) _push(`<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"><div class="bg-white rounded-lg shadow-lg p-6 w-96"><h3 class="text-lg font-bold text-slate-900 mb-4">${ssrInterpolate(unref(editingId) ? "Edit Suku Cadang" : "Tambah Suku Cadang")}</h3><form class="space-y-4"><div><label class="block text-sm font-medium text-slate-700 mb-1">Nomor Part</label><input${ssrRenderAttr("value", unref(formData).part_number)} type="text" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Nama</label><input${ssrRenderAttr("value", unref(formData).name)} type="text" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Merk</label><input${ssrRenderAttr("value", unref(formData).brand)} type="text" class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Harga</label><input${ssrRenderAttr("value", unref(formData).price)} type="number" min="0" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div class="grid grid-cols-2 gap-3"><div><label class="block text-sm font-medium text-slate-700 mb-1">Stok</label><input${ssrRenderAttr("value", unref(formData).stock)} type="number" min="0" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Minimum</label><input${ssrRenderAttr("value", unref(formData).minimum_stock)} type="number" min="0" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div></div><div class="flex gap-3"><button type="submit" class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">Simpan</button><button type="button" class="flex-1 bg-slate-300 text-slate-900 px-4 py-2 rounded-lg hover:bg-slate-400 transition">Batal</button></div></form></div></div>`);
			else _push(`<!---->`);
			_push(`</div>`);
		};
	}
});
//#endregion
//#region pages/spareparts.vue
var _sfc_setup = spareparts_vue_vue_type_script_setup_true_lang_default.setup;
spareparts_vue_vue_type_script_setup_true_lang_default.setup = (props, ctx) => {
	const ssrContext = useSSRContext();
	(ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/spareparts.vue");
	return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
var spareparts_default = spareparts_vue_vue_type_script_setup_true_lang_default;

export { spareparts_default as default };
//# sourceMappingURL=spareparts-BivyEcfY.mjs.map
