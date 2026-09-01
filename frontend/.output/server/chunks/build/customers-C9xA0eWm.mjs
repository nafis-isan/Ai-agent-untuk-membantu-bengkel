import { t as components_default } from './components-Cd10hOdb.mjs';
import { u as useCustomerStore } from './customers-D_qYtUuR.mjs';
import { defineComponent, ref, computed, mergeProps, unref, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderComponent, ssrRenderAttr, ssrRenderList, ssrInterpolate } from 'vue/server-renderer';
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

//#region pages/customers.vue?vue&type=script&setup=true&lang.ts
var customers_vue_vue_type_script_setup_true_lang_default = /*@__PURE__*/ defineComponent({
	__name: "customers",
	__ssrInlineRender: true,
	setup(__props) {
		const customerStore = useCustomerStore();
		const searchQuery = ref("");
		const showForm = ref(false);
		const editingId = ref(null);
		const formData = ref({
			name: "",
			phone: "",
			email: "",
			address: ""
		});
		const filteredCustomers = computed(() => {
			return customerStore.customers.filter((customer) => customer.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || customer.phone.includes(searchQuery.value));
		});
		return (_ctx, _push, _parent, _attrs) => {
			const _component_Icon = components_default;
			_push(`<div${ssrRenderAttrs(mergeProps({ class: "p-8" }, _attrs))}><div class="flex justify-between items-center mb-6"><h3 class="text-2xl font-bold text-slate-900">Daftar Pelanggan</h3><button class="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:plus",
				class: "w-5 h-5"
			}, null, _parent));
			_push(` Tambah Pelanggan </button></div><div class="mb-6"><input${ssrRenderAttr("value", unref(searchQuery))} type="text" placeholder="Cari pelanggan..." class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div>`);
			if (unref(customerStore).loading) _push(`<div class="text-center py-8"><p class="text-slate-600">Memuat data...</p></div>`);
			else {
				_push(`<div class="bg-white rounded-lg shadow overflow-hidden"><table class="w-full"><thead class="bg-slate-50 border-b border-slate-200"><tr><th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Nama</th><th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">No. Telepon</th><th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Email</th><th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Alamat</th><th class="px-6 py-3 text-left text-sm font-semibold text-slate-900">Aksi</th></tr></thead><tbody class="divide-y divide-slate-200"><!--[-->`);
				ssrRenderList(unref(filteredCustomers), (customer) => {
					_push(`<tr class="hover:bg-slate-50"><td class="px-6 py-4 text-sm text-slate-900">${ssrInterpolate(customer.name)}</td><td class="px-6 py-4 text-sm text-slate-600">${ssrInterpolate(customer.phone)}</td><td class="px-6 py-4 text-sm text-slate-600">${ssrInterpolate(customer.email)}</td><td class="px-6 py-4 text-sm text-slate-600">${ssrInterpolate(customer.address)}</td><td class="px-6 py-4 text-sm"><button class="text-blue-600 hover:text-blue-700 mr-4"> Edit </button><button class="text-red-600 hover:text-red-700"> Hapus </button></td></tr>`);
				});
				_push(`<!--]--></tbody></table></div>`);
			}
			if (unref(showForm)) _push(`<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"><div class="bg-white rounded-lg shadow-lg p-6 w-96"><h3 class="text-lg font-bold text-slate-900 mb-4">${ssrInterpolate(unref(editingId) ? "Edit Pelanggan" : "Tambah Pelanggan")}</h3><form class="space-y-4"><div><label class="block text-sm font-medium text-slate-700 mb-1">Nama</label><input${ssrRenderAttr("value", unref(formData).name)} type="text" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">No. Telepon</label><input${ssrRenderAttr("value", unref(formData).phone)} type="tel" required class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Email</label><input${ssrRenderAttr("value", unref(formData).email)} type="email" class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"></div><div><label class="block text-sm font-medium text-slate-700 mb-1">Alamat</label><textarea class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">${ssrInterpolate(unref(formData).address)}</textarea></div><div class="flex gap-3"><button type="submit" class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"> Simpan </button><button type="button" class="flex-1 bg-slate-300 text-slate-900 px-4 py-2 rounded-lg hover:bg-slate-400 transition"> Batal </button></div></form></div></div>`);
			else _push(`<!---->`);
			_push(`</div>`);
		};
	}
});
//#endregion
//#region pages/customers.vue
var _sfc_setup = customers_vue_vue_type_script_setup_true_lang_default.setup;
customers_vue_vue_type_script_setup_true_lang_default.setup = (props, ctx) => {
	const ssrContext = useSSRContext();
	(ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/customers.vue");
	return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
var customers_default = customers_vue_vue_type_script_setup_true_lang_default;

export { customers_default as default };
//# sourceMappingURL=customers-C9xA0eWm.mjs.map
