import { t as components_default } from './components-CGtk4XIN.mjs';
import { N as NuxtLink } from '../virtual/entry.mjs';
import { u as useCustomerStore } from './customers-DMXT0ivR.mjs';
import { u as useVehicleStore } from './vehicles-D-50B4Vh.mjs';
import { u as useServiceStore } from './services-BhnTR1CI.mjs';
import { u as useSparepartStore } from './spareparts-B86EKxF5.mjs';
import { defineComponent, ref, computed, mergeProps, withCtx, createVNode, createTextVNode, unref, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderComponent, ssrRenderList, ssrRenderClass, ssrInterpolate, ssrRenderStyle } from 'vue/server-renderer';
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
import './useAPI-DRNp7d_T.mjs';

//#region pages/index.vue?vue&type=script&setup=true&lang.ts
var index_vue_vue_type_script_setup_true_lang_default = /*@__PURE__*/ defineComponent({
	__name: "index",
	__ssrInlineRender: true,
	setup(__props) {
		const customerStore = useCustomerStore();
		const vehicleStore = useVehicleStore();
		const serviceStore = useServiceStore();
		const sparepartStore = useSparepartStore();
		const insights = ref([]);
		const stats = computed(() => ({
			customers: customerStore.customers.length,
			vehicles: vehicleStore.vehicles.length,
			services: serviceStore.services.filter((service) => [
				"waiting",
				"in_progress",
				"scheduled"
			].includes(service.status)).length,
			lowStock: sparepartStore.spareparts.filter((item) => item.stock <= item.minimum_stock).length
		}));
		const statCards = computed(() => [
			{
				label: "Total Pelanggan",
				value: stats.value.customers,
				note: "Terdaftar di sistem",
				icon: "lucide:users",
				iconBg: "bg-blue-50",
				iconColor: "text-blue-600"
			},
			{
				label: "Kendaraan Terdaftar",
				value: stats.value.vehicles,
				note: "Kendaraan pelanggan",
				icon: "lucide:car-front",
				iconBg: "bg-emerald-50",
				iconColor: "text-emerald-600"
			},
			{
				label: "Servis Aktif",
				value: stats.value.services,
				note: "Menunggu atau dikerjakan",
				icon: "lucide:wrench",
				iconBg: "bg-amber-50",
				iconColor: "text-amber-600"
			},
			{
				label: "Suku Cadang Low Stock",
				value: stats.value.lowStock,
				note: "Perlu segera direstock",
				icon: "lucide:package-open",
				iconBg: "bg-rose-50",
				iconColor: "text-rose-600"
			}
		]);
		const chartBars = [
			42,
			68,
			54,
			82,
			64,
			91
		];
		const chartLabels = [
			"Mar",
			"Apr",
			"Mei",
			"Jun",
			"Jul",
			"Agu"
		];
		const recentServices = computed(() => {
			return [...serviceStore.services].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()).slice(0, 3);
		});
		const lowStockParts = computed(() => {
			return [...sparepartStore.spareparts].filter((item) => item.stock <= item.minimum_stock).slice(0, 3);
		});
		const getVehicleLabel = (vehicleId) => {
			const vehicle = vehicleStore.vehicles.find((item) => item.id === vehicleId);
			if (!vehicle) return "Kendaraan tidak diketahui";
			return `${vehicle.brand} ${vehicle.model} - ${vehicle.plate_number}`;
		};
		const statusLabel = (status) => {
			return {
				waiting: "Menunggu",
				in_progress: "Proses",
				scheduled: "Terjadwal",
				completed: "Selesai",
				cancelled: "Batal"
			}[status] || status;
		};
		const statusBadge = (status) => ({
			waiting: "bg-amber-50 text-amber-700",
			in_progress: "bg-blue-50 text-blue-700",
			scheduled: "bg-indigo-50 text-indigo-700",
			completed: "bg-emerald-50 text-emerald-700",
			cancelled: "bg-rose-50 text-rose-700"
		})[status] || "bg-slate-100 text-slate-600";
		const insightClass = (tone) => ({
			blue: "border-blue-100 bg-blue-50 text-blue-800",
			amber: "border-amber-100 bg-amber-50 text-amber-800",
			rose: "border-rose-100 bg-rose-50 text-rose-800",
			emerald: "border-emerald-100 bg-emerald-50 text-emerald-800"
		})[tone] || "border-slate-200 bg-slate-50 text-slate-700";
		const insightIcon = (type) => ({
			active_services: "lucide:wrench",
			low_stock: "lucide:package-open",
			waiting_services: "lucide:clock-3",
			healthy: "lucide:circle-check"
		})[type] || "lucide:info";
		return (_ctx, _push, _parent, _attrs) => {
			const _component_NuxtLink = NuxtLink;
			const _component_Icon = components_default;
			_push(`<div${ssrRenderAttrs(mergeProps({ class: "space-y-8" }, _attrs))}><section class="flex flex-col justify-between gap-5 md:flex-row md:items-end"><div><p class="mb-2 text-sm font-semibold text-blue-600">Selamat datang kembali, Admin</p><h2 class="text-3xl font-extrabold tracking-tight text-slate-900 md:text-4xl">Ringkasan bengkel</h2><p class="mt-2 text-sm text-slate-500">Pantau aktivitas dan kondisi operasional bengkel Anda hari ini.</p></div>`);
			_push(ssrRenderComponent(_component_NuxtLink, {
				to: "/services",
				class: "inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-3 text-sm font-bold text-white shadow-sm hover:bg-blue-700"
			}, {
				default: withCtx((_, _push, _parent, _scopeId) => {
					if (_push) {
						_push(ssrRenderComponent(_component_Icon, {
							name: "lucide:plus",
							class: "h-4 w-4"
						}, null, _parent, _scopeId));
						_push(`Tambah Servis`);
					} else return [createVNode(_component_Icon, {
						name: "lucide:plus",
						class: "h-4 w-4"
					}), createTextVNode("Tambah Servis")];
				}),
				_: 1
			}, _parent));
			_push(`</section><section class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4"><!--[-->`);
			ssrRenderList(unref(statCards), (stat) => {
				_push(`<div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-[0_4px_20px_rgb(15_23_42/0.03)] transition hover:-translate-y-0.5 hover:shadow-md"><div class="flex items-start justify-between"><div class="${ssrRenderClass([stat.iconBg, "flex h-10 w-10 items-center justify-center rounded-xl"])}">`);
				_push(ssrRenderComponent(_component_Icon, {
					name: stat.icon,
					class: ["h-5 w-5", stat.iconColor]
				}, null, _parent));
				_push(`</div><span class="rounded-full bg-emerald-50 px-2 py-1 text-[10px] font-bold text-emerald-700">Aktif</span></div><p class="mt-5 text-sm font-medium text-slate-500">${ssrInterpolate(stat.label)}</p><p class="mt-1 text-3xl font-extrabold tracking-tight text-slate-900">${ssrInterpolate(stat.value)}</p><p class="mt-2 text-xs text-slate-400">${ssrInterpolate(stat.note)}</p></div>`);
			});
			_push(`<!--]--></section><section class="rounded-2xl border border-slate-200 bg-white p-5 shadow-[0_4px_20px_rgb(15_23_42/0.03)] md:p-6"><div class="flex items-center justify-between"><div><h3 class="text-base font-bold text-slate-900">Insight operasional</h3><p class="mt-1 text-xs text-slate-400">Ringkasan otomatis dari kondisi database bengkel</p></div>`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:sparkles",
				class: "h-5 w-5 text-blue-500"
			}, null, _parent));
			_push(`</div><div class="mt-4 grid grid-cols-1 gap-3 md:grid-cols-3"><!--[-->`);
			ssrRenderList(unref(insights), (insight) => {
				_push(`<div class="${ssrRenderClass([insightClass(insight.tone), "rounded-xl border p-4"])}"><div class="flex items-start gap-3">`);
				_push(ssrRenderComponent(_component_Icon, {
					name: insightIcon(insight.type),
					class: "mt-0.5 h-4 w-4 shrink-0"
				}, null, _parent));
				_push(`<div><p class="text-sm font-bold">${ssrInterpolate(insight.title)}</p><p class="mt-1 text-xs leading-5 opacity-80">${ssrInterpolate(insight.description)}</p></div></div></div>`);
			});
			_push(`<!--]--></div></section><section class="grid grid-cols-1 gap-5 xl:grid-cols-[1.35fr_0.65fr]"><div class="rounded-2xl border border-slate-200 bg-white p-5 shadow-[0_4px_20px_rgb(15_23_42/0.03)] md:p-6"><div class="flex items-center justify-between"><div><h3 class="text-base font-bold text-slate-900">Ringkasan servis</h3><p class="mt-1 text-xs text-slate-400">Aktivitas servis dalam 6 periode terakhir</p></div><button class="rounded-lg p-2 text-slate-400 hover:bg-slate-50">`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:more-horizontal",
				class: "h-5 w-5"
			}, null, _parent));
			_push(`</button></div><div class="mt-8 flex h-48 items-end justify-between gap-3 border-b border-l border-slate-200 px-2 pb-0 pt-4"><!--[-->`);
			ssrRenderList(chartBars, (height, index) => {
				_push(`<div class="flex h-full flex-1 flex-col items-center justify-end gap-2"><div class="w-full max-w-10 rounded-t-lg bg-blue-500 transition hover:bg-blue-600" style="${ssrRenderStyle({ height: `${height}%` })}"></div><span class="text-[10px] text-slate-400">${ssrInterpolate(chartLabels[index])}</span></div>`);
			});
			_push(`<!--]--></div></div><div class="rounded-2xl bg-slate-900 p-6 text-white"><div class="flex items-center gap-2 text-blue-300">`);
			_push(ssrRenderComponent(_component_Icon, {
				name: "lucide:activity",
				class: "h-4 w-4"
			}, null, _parent));
			_push(`<span class="text-xs font-bold uppercase tracking-wider">Operasional</span></div><h3 class="mt-6 text-xl font-extrabold">Semua terlihat terkendali.</h3><p class="mt-2 text-sm leading-6 text-slate-400">Jaga stok dan pantau antrean servis agar pelanggan mendapat layanan terbaik.</p><div class="mt-8 grid grid-cols-2 gap-3"><div class="rounded-xl bg-white/10 p-3"><p class="text-2xl font-extrabold">${ssrInterpolate(unref(stats).services)}</p><p class="mt-1 text-[11px] text-slate-400">Servis aktif</p></div><div class="rounded-xl bg-white/10 p-3"><p class="text-2xl font-extrabold">${ssrInterpolate(unref(stats).lowStock)}</p><p class="mt-1 text-[11px] text-slate-400">Perlu restock</p></div></div></div></section><section class="grid grid-cols-1 gap-5 xl:grid-cols-[1.35fr_0.65fr]"><div class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-[0_4px_20px_rgb(15_23_42/0.03)]"><div class="flex items-center justify-between border-b border-slate-100 p-5 md:p-6"><div><h3 class="text-base font-bold text-slate-900">Servis terbaru</h3><p class="mt-1 text-xs text-slate-400">Aktivitas pekerjaan yang baru masuk</p></div>`);
			_push(ssrRenderComponent(_component_NuxtLink, {
				to: "/services",
				class: "text-xs font-bold text-blue-600 hover:text-blue-700"
			}, {
				default: withCtx((_, _push, _parent, _scopeId) => {
					if (_push) _push(`Lihat semua`);
					else return [createTextVNode("Lihat semua")];
				}),
				_: 1
			}, _parent));
			_push(`</div>`);
			if (unref(recentServices).length) {
				_push(`<div class="divide-y divide-slate-100"><!--[-->`);
				ssrRenderList(unref(recentServices), (service) => {
					_push(`<div class="flex items-center justify-between gap-4 p-5 transition hover:bg-slate-50"><div class="flex min-w-0 items-center gap-3"><span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600">`);
					_push(ssrRenderComponent(_component_Icon, {
						name: "lucide:wrench",
						class: "h-4 w-4"
					}, null, _parent));
					_push(`</span><div class="min-w-0"><p class="truncate text-sm font-bold text-slate-800">${ssrInterpolate(getVehicleLabel(service.vehicle_id))}</p><p class="truncate text-xs text-slate-400">${ssrInterpolate(service.complaint || "Tidak ada keluhan")}</p></div></div><span class="${ssrRenderClass([statusBadge(service.status), "shrink-0 rounded-full px-2.5 py-1 text-[10px] font-bold"])}">${ssrInterpolate(statusLabel(service.status))}</span></div>`);
				});
				_push(`<!--]--></div>`);
			} else _push(`<div class="p-8 text-center text-sm text-slate-400">Belum ada data servis.</div>`);
			_push(`</div><div class="rounded-2xl border border-slate-200 bg-white shadow-[0_4px_20px_rgb(15_23_42/0.03)]"><div class="border-b border-slate-100 p-5 md:p-6"><h3 class="text-base font-bold text-slate-900">Perlu restock</h3><p class="mt-1 text-xs text-slate-400">Suku cadang di bawah batas minimum</p></div>`);
			if (unref(lowStockParts).length) {
				_push(`<div class="divide-y divide-slate-100"><!--[-->`);
				ssrRenderList(unref(lowStockParts), (item) => {
					_push(`<div class="p-5"><div class="flex items-center justify-between gap-3"><div class="flex min-w-0 items-center gap-3"><span class="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-50 text-amber-600">`);
					_push(ssrRenderComponent(_component_Icon, {
						name: "lucide:package",
						class: "h-4 w-4"
					}, null, _parent));
					_push(`</span><p class="truncate text-sm font-bold text-slate-800">${ssrInterpolate(item.name)}</p></div><span class="text-xs font-bold text-rose-600">${ssrInterpolate(item.stock)} tersisa</span></div><div class="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full bg-amber-500" style="${ssrRenderStyle({ width: `${Math.min(item.stock / Math.max(item.minimum_stock, 1) * 100, 100)}%` })}"></div></div></div>`);
				});
				_push(`<!--]--></div>`);
			} else _push(`<div class="p-8 text-center text-sm text-slate-400">Stok semua aman.</div>`);
			_push(`</div></section></div>`);
		};
	}
});
//#endregion
//#region pages/index.vue
var _sfc_setup = index_vue_vue_type_script_setup_true_lang_default.setup;
index_vue_vue_type_script_setup_true_lang_default.setup = (props, ctx) => {
	const ssrContext = useSSRContext();
	(ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/index.vue");
	return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
var pages_default = index_vue_vue_type_script_setup_true_lang_default;

export { pages_default as default };
//# sourceMappingURL=pages-DA4o-nlZ.mjs.map
