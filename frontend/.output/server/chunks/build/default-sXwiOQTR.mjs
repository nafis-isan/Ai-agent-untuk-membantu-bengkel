import { t as components_default } from './components-Cd10hOdb.mjs';
import { a as useRoute$1, N as NuxtLink } from '../virtual/entry.mjs';
import { defineComponent, computed, mergeProps, withCtx, createVNode, unref, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderComponent, ssrInterpolate, ssrRenderSlot } from 'vue/server-renderer';
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
import 'pinia';
import 'tailwindcss/colors';

//#region layouts/default.vue?vue&type=script&setup=true&lang.ts
var default_vue_vue_type_script_setup_true_lang_default = /*@__PURE__*/ defineComponent({
	__name: "default",
	__ssrInlineRender: true,
	setup(__props) {
		const route = useRoute$1();
		const pageTitle = computed(() => {
			return {
				"/": "Dashboard",
				"/customers": "Manajemen Pelanggan",
				"/vehicles": "Tracking Kendaraan",
				"/services": "Riwayat Servis",
				"/spareparts": "Manajemen Suku Cadang",
				"/chat": "AI Assistant"
			}[route.path] || "BengkelAI";
		});
		return (_ctx, _push, _parent, _attrs) => {
			const _component_NuxtLink = NuxtLink;
			const _component_Icon = components_default;
			_push(`<div${ssrRenderAttrs(mergeProps({ class: "flex h-screen bg-slate-50" }, _attrs))}><div class="w-64 bg-white border-r border-slate-200"><div class="p-6"><h1 class="text-2xl font-bold text-blue-600">BengkelAI</h1><p class="text-sm text-slate-500 mt-1">Workshop Management</p></div><nav class="mt-6 space-y-2 px-3">`);
			_push(ssrRenderComponent(_component_NuxtLink, {
				to: "/",
				class: "flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-50 text-slate-700 hover:text-blue-600 transition"
			}, {
				default: withCtx((_, _push, _parent, _scopeId) => {
					if (_push) {
						_push(ssrRenderComponent(_component_Icon, {
							name: "lucide:home",
							class: "w-5 h-5"
						}, null, _parent, _scopeId));
						_push(`<span${_scopeId}>Dashboard</span>`);
					} else return [createVNode(_component_Icon, {
						name: "lucide:home",
						class: "w-5 h-5"
					}), createVNode("span", null, "Dashboard")];
				}),
				_: 1
			}, _parent));
			_push(ssrRenderComponent(_component_NuxtLink, {
				to: "/customers",
				class: "flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-50 text-slate-700 hover:text-blue-600 transition"
			}, {
				default: withCtx((_, _push, _parent, _scopeId) => {
					if (_push) {
						_push(ssrRenderComponent(_component_Icon, {
							name: "lucide:users",
							class: "w-5 h-5"
						}, null, _parent, _scopeId));
						_push(`<span${_scopeId}>Pelanggan</span>`);
					} else return [createVNode(_component_Icon, {
						name: "lucide:users",
						class: "w-5 h-5"
					}), createVNode("span", null, "Pelanggan")];
				}),
				_: 1
			}, _parent));
			_push(ssrRenderComponent(_component_NuxtLink, {
				to: "/vehicles",
				class: "flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-50 text-slate-700 hover:text-blue-600 transition"
			}, {
				default: withCtx((_, _push, _parent, _scopeId) => {
					if (_push) {
						_push(ssrRenderComponent(_component_Icon, {
							name: "lucide:car",
							class: "w-5 h-5"
						}, null, _parent, _scopeId));
						_push(`<span${_scopeId}>Kendaraan</span>`);
					} else return [createVNode(_component_Icon, {
						name: "lucide:car",
						class: "w-5 h-5"
					}), createVNode("span", null, "Kendaraan")];
				}),
				_: 1
			}, _parent));
			_push(ssrRenderComponent(_component_NuxtLink, {
				to: "/services",
				class: "flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-50 text-slate-700 hover:text-blue-600 transition"
			}, {
				default: withCtx((_, _push, _parent, _scopeId) => {
					if (_push) {
						_push(ssrRenderComponent(_component_Icon, {
							name: "lucide:wrench",
							class: "w-5 h-5"
						}, null, _parent, _scopeId));
						_push(`<span${_scopeId}>Layanan</span>`);
					} else return [createVNode(_component_Icon, {
						name: "lucide:wrench",
						class: "w-5 h-5"
					}), createVNode("span", null, "Layanan")];
				}),
				_: 1
			}, _parent));
			_push(ssrRenderComponent(_component_NuxtLink, {
				to: "/spareparts",
				class: "flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-50 text-slate-700 hover:text-blue-600 transition"
			}, {
				default: withCtx((_, _push, _parent, _scopeId) => {
					if (_push) {
						_push(ssrRenderComponent(_component_Icon, {
							name: "lucide:package",
							class: "w-5 h-5"
						}, null, _parent, _scopeId));
						_push(`<span${_scopeId}>Suku Cadang</span>`);
					} else return [createVNode(_component_Icon, {
						name: "lucide:package",
						class: "w-5 h-5"
					}), createVNode("span", null, "Suku Cadang")];
				}),
				_: 1
			}, _parent));
			_push(ssrRenderComponent(_component_NuxtLink, {
				to: "/chat",
				class: "flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-50 text-slate-700 hover:text-blue-600 transition"
			}, {
				default: withCtx((_, _push, _parent, _scopeId) => {
					if (_push) {
						_push(ssrRenderComponent(_component_Icon, {
							name: "lucide:message-circle",
							class: "w-5 h-5"
						}, null, _parent, _scopeId));
						_push(`<span${_scopeId}>AI Chat</span>`);
					} else return [createVNode(_component_Icon, {
						name: "lucide:message-circle",
						class: "w-5 h-5"
					}), createVNode("span", null, "AI Chat")];
				}),
				_: 1
			}, _parent));
			_push(`</nav></div><div class="flex-1 flex flex-col"><div class="bg-white border-b border-slate-200 px-8 py-4"><div class="flex justify-between items-center"><h2 class="text-xl font-semibold text-slate-900">${ssrInterpolate(unref(pageTitle))}</h2><div class="flex items-center gap-4"><button class="p-2 hover:bg-slate-100 rounded-lg" aria-label="Notifikasi">`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:bell",
				class: "w-5 h-5 text-slate-600"
			}, null, _parent));
			_push(`</button></div></div></div><div class="flex-1 overflow-auto">`);
			ssrRenderSlot(_ctx.$slots, "default", {}, null, _push, _parent);
			_push(`</div></div></div>`);
		};
	}
});
//#endregion
//#region layouts/default.vue
var _sfc_setup = default_vue_vue_type_script_setup_true_lang_default.setup;
default_vue_vue_type_script_setup_true_lang_default.setup = (props, ctx) => {
	const ssrContext = useSSRContext();
	(ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("layouts/default.vue");
	return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
var default_default = default_vue_vue_type_script_setup_true_lang_default;

export { default_default as default };
//# sourceMappingURL=default-sXwiOQTR.mjs.map
