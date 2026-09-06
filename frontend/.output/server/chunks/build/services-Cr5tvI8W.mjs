import { t as components_default } from './components-Bfu6e32q.mjs';
import { defineComponent, ref, mergeProps, unref, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderList, ssrRenderComponent, ssrInterpolate, ssrRenderClass } from 'vue/server-renderer';
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

//#region pages/services.vue?vue&type=script&setup=true&lang.ts
var services_vue_vue_type_script_setup_true_lang_default = /*@__PURE__*/ defineComponent({
	__name: "services",
	__ssrInlineRender: true,
	setup(__props) {
		const services = ref([
			{
				vehicle: "Honda Civic",
				plate: "D 1234 ABC",
				description: "Ganti oli, filter udara, dan pemeriksaan sistem pengereman",
				date: "15 Agustus 2026",
				cost: "Rp 450.000",
				status: "Selesai",
				statusColor: "bg-green-100 text-green-700"
			},
			{
				vehicle: "Toyota Avanza",
				plate: "D 5678 DEF",
				description: "Perbaikan sistem AC dan isi freon",
				date: "12 Agustus 2026",
				cost: "Rp 600.000",
				status: "Selesai",
				statusColor: "bg-green-100 text-green-700"
			},
			{
				vehicle: "Suzuki Ertiga",
				plate: "D 9012 GHI",
				description: "Service rutin dan penggantian kampas rem",
				date: "10 Agustus 2026",
				cost: "Rp 750.000",
				status: "Selesai",
				statusColor: "bg-green-100 text-green-700"
			}
		]);
		return (_ctx, _push, _parent, _attrs) => {
			const _component_Icon = components_default;
			_push(`<div${ssrRenderAttrs(mergeProps({ class: "p-8" }, _attrs))}><h3 class="text-2xl font-bold text-slate-900 mb-6">Riwayat Servis</h3><div class="max-w-4xl"><!--[-->`);
			ssrRenderList(unref(services), (service, index) => {
				_push(`<div class="flex gap-6 mb-8"><div class="flex flex-col items-center"><div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">`);
				_push(ssrRenderComponent(_component_Icon, {
					name: "lucide:wrench",
					class: "w-6 h-6 text-blue-600"
				}, null, _parent));
				_push(`</div>`);
				if (index < unref(services).length - 1) _push(`<div class="w-1 h-24 bg-blue-100 my-2"></div>`);
				else _push(`<!---->`);
				_push(`</div><div class="flex-1 pb-6"><div class="bg-white rounded-lg shadow p-6"><div class="flex justify-between items-start mb-3"><div><h4 class="text-lg font-bold text-slate-900">${ssrInterpolate(service.vehicle)}</h4><p class="text-sm text-slate-600">${ssrInterpolate(service.plate)}</p></div><span class="${ssrRenderClass(`px-3 py-1 text-xs font-semibold rounded-full ${service.statusColor}`)}">${ssrInterpolate(service.status)}</span></div><p class="text-slate-700 mb-4">${ssrInterpolate(service.description)}</p><div class="grid grid-cols-2 gap-4 mb-4 pb-4 border-b border-slate-200"><div><p class="text-sm text-slate-600">Tanggal Servis</p><p class="font-semibold text-slate-900">${ssrInterpolate(service.date)}</p></div><div><p class="text-sm text-slate-600">Biaya</p><p class="font-semibold text-slate-900">${ssrInterpolate(service.cost)}</p></div></div><div class="flex gap-2"><button class="text-sm text-blue-600 hover:text-blue-700 font-medium">Lihat Detail</button><button class="text-sm text-slate-600 hover:text-slate-700 font-medium">Cetak Invoice</button></div></div></div></div>`);
			});
			_push(`<!--]--></div></div>`);
		};
	}
});
//#endregion
//#region pages/services.vue
var _sfc_setup = services_vue_vue_type_script_setup_true_lang_default.setup;
services_vue_vue_type_script_setup_true_lang_default.setup = (props, ctx) => {
	const ssrContext = useSSRContext();
	(ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/services.vue");
	return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
var services_default = services_vue_vue_type_script_setup_true_lang_default;

export { services_default as default };
//# sourceMappingURL=services-Cr5tvI8W.mjs.map
