import { t as components_default } from './components-CGtk4XIN.mjs';
import { a as useRoute$1, N as NuxtLink } from '../virtual/entry.mjs';
import { u as useAuthStore } from './auth-CgeVtR3d.mjs';
import { _ as _plugin_vue_export_helper_default } from './_plugin-vue_export-helper-BOaGB7Aw.mjs';
import { defineComponent, ref, computed, watch, mergeProps, unref, withCtx, createVNode, toDisplayString, openBlock, createBlock, createCommentVNode, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderClass, ssrRenderComponent, ssrRenderList, ssrInterpolate, ssrRenderSlot } from 'vue/server-renderer';
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
import 'unhead/utils';

//#region layouts/default.vue?vue&type=script&setup=true&lang.ts
var default_vue_vue_type_script_setup_true_lang_default = /*@__PURE__*/ defineComponent({
	__name: "default",
	__ssrInlineRender: true,
	setup(__props) {
		const route = useRoute$1();
		useAuthStore();
		const mobileOpen = ref(false);
		const navItems = [
			{
				to: "/",
				label: "Dashboard",
				icon: "lucide:layout-dashboard"
			},
			{
				to: "/customers",
				label: "Pelanggan",
				icon: "lucide:users"
			},
			{
				to: "/vehicles",
				label: "Kendaraan",
				icon: "lucide:car-front"
			},
			{
				to: "/services",
				label: "Layanan",
				icon: "lucide:wrench"
			},
			{
				to: "/appointments",
				label: "Appointment",
				icon: "lucide:calendar-days"
			},
			{
				to: "/spareparts",
				label: "Suku Cadang",
				icon: "lucide:package"
			},
			{
				to: "/chat",
				label: "AI Assistant",
				icon: "lucide:message-circle"
			}
		];
		const pageTitle = computed(() => {
			return {
				"/": "Dashboard",
				"/customers": "Manajemen Pelanggan",
				"/vehicles": "Tracking Kendaraan",
				"/services": "Riwayat Servis",
				"/appointments": "Appointment",
				"/spareparts": "Manajemen Suku Cadang",
				"/chat": "AI Assistant"
			}[route.path] || "BengkelAI";
		});
		watch(() => route.path, () => {
			mobileOpen.value = false;
		});
		return (_ctx, _push, _parent, _attrs) => {
			const _component_NuxtLink = NuxtLink;
			const _component_Icon = components_default;
			_push(`<div${ssrRenderAttrs(mergeProps({ class: "min-h-screen bg-[#f6f8fb] text-slate-900" }, _attrs))} data-v-f8fea41a>`);
			if (unref(mobileOpen)) _push(`<div class="fixed inset-0 z-40 bg-slate-950/35 lg:hidden" data-v-f8fea41a></div>`);
			else _push(`<!---->`);
			_push(`<aside class="${ssrRenderClass([unref(mobileOpen) ? "translate-x-0" : "", "fixed inset-y-0 left-0 z-50 flex w-[270px] -translate-x-full flex-col border-r border-slate-200 bg-white px-4 py-5 transition-transform duration-200 lg:translate-x-0"])}" data-v-f8fea41a><div class="flex items-center justify-between px-3" data-v-f8fea41a>`);
			_push(ssrRenderComponent(_component_NuxtLink, {
				to: "/",
				class: "flex items-center gap-3",
				onClick: ($event) => mobileOpen.value = false
			}, {
				default: withCtx((_, _push, _parent, _scopeId) => {
					if (_push) {
						_push(`<span class="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-white shadow-sm" data-v-f8fea41a${_scopeId}>`);
						_push(ssrRenderComponent(_component_Icon, {
							name: "lucide:car-front",
							class: "h-5 w-5"
						}, null, _parent, _scopeId));
						_push(`</span><span data-v-f8fea41a${_scopeId}><span class="block text-[15px] font-extrabold tracking-tight text-slate-900" data-v-f8fea41a${_scopeId}>BengkelAI</span><span class="block text-[11px] font-medium text-slate-400" data-v-f8fea41a${_scopeId}>Workshop Management</span></span>`);
					} else return [createVNode("span", { class: "flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-white shadow-sm" }, [createVNode(_component_Icon, {
						name: "lucide:car-front",
						class: "h-5 w-5"
					})]), createVNode("span", null, [createVNode("span", { class: "block text-[15px] font-extrabold tracking-tight text-slate-900" }, "BengkelAI"), createVNode("span", { class: "block text-[11px] font-medium text-slate-400" }, "Workshop Management")])];
				}),
				_: 1
			}, _parent));
			_push(`<button class="rounded-lg p-2 text-slate-400 hover:bg-slate-100 lg:hidden" aria-label="Tutup menu" data-v-f8fea41a>`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:x",
				class: "h-5 w-5"
			}, null, _parent));
			_push(`</button></div><p class="mb-3 mt-10 px-3 text-[10px] font-bold uppercase tracking-[0.16em] text-slate-400" data-v-f8fea41a>Workspace</p><nav class="space-y-1" data-v-f8fea41a><!--[-->`);
			ssrRenderList(navItems, (item) => {
				_push(ssrRenderComponent(_component_NuxtLink, {
					key: item.to,
					to: item.to,
					class: ["sidebar-link", unref(route).path === item.to ? "sidebar-link-active" : ""],
					onClick: ($event) => mobileOpen.value = false
				}, {
					default: withCtx((_, _push, _parent, _scopeId) => {
						if (_push) {
							_push(ssrRenderComponent(_component_Icon, {
								name: item.icon,
								class: "h-[18px] w-[18px]"
							}, null, _parent, _scopeId));
							_push(`<span data-v-f8fea41a${_scopeId}>${ssrInterpolate(item.label)}</span>`);
							if (item.to === "/chat") _push(`<span class="ml-auto rounded-full bg-blue-100 px-2 py-0.5 text-[10px] font-bold text-blue-700" data-v-f8fea41a${_scopeId}>AI</span>`);
							else _push(`<!---->`);
						} else return [
							createVNode(_component_Icon, {
								name: item.icon,
								class: "h-[18px] w-[18px]"
							}, null, 8, ["name"]),
							createVNode("span", null, toDisplayString(item.label), 1),
							item.to === "/chat" ? (openBlock(), createBlock("span", {
								key: 0,
								class: "ml-auto rounded-full bg-blue-100 px-2 py-0.5 text-[10px] font-bold text-blue-700"
							}, "AI")) : createCommentVNode("", true)
						];
					}),
					_: 2
				}, _parent));
			});
			_push(`<!--]--></nav><div class="mt-auto rounded-2xl bg-slate-900 p-4 text-white" data-v-f8fea41a><div class="mb-3 flex items-center gap-2 text-blue-300" data-v-f8fea41a>`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:sparkles",
				class: "h-4 w-4"
			}, null, _parent));
			_push(`<span class="text-xs font-semibold" data-v-f8fea41a>BengkelAI Pro</span></div><p class="text-xs leading-5 text-slate-300" data-v-f8fea41a>Kelola operasional bengkel dengan lebih cepat dan teratur.</p><div class="mt-4 h-1.5 overflow-hidden rounded-full bg-slate-700" data-v-f8fea41a><div class="h-full w-3/4 rounded-full bg-blue-400" data-v-f8fea41a></div></div><p class="mt-2 text-[10px] text-slate-400" data-v-f8fea41a>Workspace aktif</p></div></aside><div class="lg:pl-[270px]" data-v-f8fea41a><header class="sticky top-0 z-30 border-b border-slate-200/80 bg-white/90 px-4 py-3 backdrop-blur md:px-8" data-v-f8fea41a><div class="mx-auto flex max-w-[1440px] items-center justify-between" data-v-f8fea41a><div class="flex items-center gap-3" data-v-f8fea41a><button class="rounded-xl border border-slate-200 p-2 text-slate-600 hover:bg-slate-50 lg:hidden" aria-label="Buka menu" data-v-f8fea41a>`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:menu",
				class: "h-5 w-5"
			}, null, _parent));
			_push(`</button><div data-v-f8fea41a><p class="text-xs font-medium text-slate-400" data-v-f8fea41a>Workspace / <span class="text-slate-600" data-v-f8fea41a>${ssrInterpolate(unref(pageTitle))}</span></p><h1 class="mt-0.5 text-lg font-bold tracking-tight text-slate-900" data-v-f8fea41a>${ssrInterpolate(unref(pageTitle))}</h1></div></div><div class="flex items-center gap-2 md:gap-4" data-v-f8fea41a><button class="relative rounded-xl p-2.5 text-slate-500 transition hover:bg-slate-100 hover:text-slate-900" aria-label="Notifikasi" data-v-f8fea41a>`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:bell",
				class: "h-5 w-5"
			}, null, _parent));
			_push(`<span class="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-blue-600 ring-2 ring-white" data-v-f8fea41a></span></button><div class="hidden h-7 w-px bg-slate-200 md:block" data-v-f8fea41a></div><button class="flex items-center gap-2 rounded-xl p-1.5 pr-2 transition hover:bg-slate-50" aria-label="Keluar" title="Keluar" data-v-f8fea41a><span class="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-100 text-xs font-bold text-blue-700" data-v-f8fea41a>AD</span><span class="hidden text-left md:block" data-v-f8fea41a><span class="block text-xs font-bold text-slate-800" data-v-f8fea41a>Admin Bengkel</span><span class="block text-[10px] text-slate-400" data-v-f8fea41a>Administrator</span></span>`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:log-out",
				class: "h-4 w-4 text-slate-400"
			}, null, _parent));
			_push(`</button></div></div></header><main class="mx-auto max-w-[1440px] px-4 py-6 md:px-8 md:py-8" data-v-f8fea41a>`);
			ssrRenderSlot(_ctx.$slots, "default", {}, null, _push, _parent);
			_push(`</main></div></div>`);
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
var default_default = /*#__PURE__*/ _plugin_vue_export_helper_default(default_vue_vue_type_script_setup_true_lang_default, [["__scopeId", "data-v-f8fea41a"]]);

export { default_default as default };
//# sourceMappingURL=default-rFJtjPzs.mjs.map
