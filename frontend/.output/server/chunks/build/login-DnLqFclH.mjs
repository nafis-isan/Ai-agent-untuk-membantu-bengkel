import { a as useRoute$1 } from '../virtual/entry.mjs';
import { u as useAuthStore } from './auth-CgeVtR3d.mjs';
import { defineComponent, ref, mergeProps, unref, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderAttr, ssrInterpolate, ssrIncludeBooleanAttr } from 'vue/server-renderer';
import 'nostics';
import 'nostics/formatters/ansi';
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
import '../routes/renderer.mjs';
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
import 'unhead/utils';

//#region pages/login.vue?vue&type=script&setup=true&lang.ts
var login_vue_vue_type_script_setup_true_lang_default = /*@__PURE__*/ defineComponent({
	__name: "login",
	__ssrInlineRender: true,
	setup(__props) {
		useAuthStore();
		useRoute$1();
		const username = ref("");
		const password = ref("");
		const loading = ref(false);
		const error = ref("");
		return (_ctx, _push, _parent, _attrs) => {
			_push(`<main${ssrRenderAttrs(mergeProps({ class: "flex min-h-screen items-center justify-center bg-slate-950 px-4" }, _attrs))}><form class="w-full max-w-sm rounded-2xl bg-white p-8 shadow-2xl"><div class="mb-8"><p class="text-sm font-bold uppercase tracking-[0.18em] text-blue-600">BengkelAI</p><h1 class="mt-2 text-2xl font-extrabold text-slate-900">Admin masuk</h1></div><label class="mb-4 block text-sm font-semibold text-slate-700">Username<input${ssrRenderAttr("value", unref(username))} class="mt-2 w-full rounded-xl border border-slate-200 px-3 py-3" autocomplete="username" required></label><label class="mb-5 block text-sm font-semibold text-slate-700">Password<input${ssrRenderAttr("value", unref(password))} type="password" class="mt-2 w-full rounded-xl border border-slate-200 px-3 py-3" autocomplete="current-password" required></label>`);
			if (unref(error)) _push(`<p class="mb-4 text-sm text-rose-600">${ssrInterpolate(unref(error))}</p>`);
			else _push(`<!---->`);
			_push(`<button class="w-full rounded-xl bg-blue-600 px-4 py-3 font-bold text-white disabled:bg-slate-300"${ssrIncludeBooleanAttr(unref(loading)) ? " disabled" : ""}>Masuk</button></form></main>`);
		};
	}
});
//#endregion
//#region pages/login.vue
var _sfc_setup = login_vue_vue_type_script_setup_true_lang_default.setup;
login_vue_vue_type_script_setup_true_lang_default.setup = (props, ctx) => {
	const ssrContext = useSSRContext();
	(ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/login.vue");
	return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
var login_default = login_vue_vue_type_script_setup_true_lang_default;

export { login_default as default };
//# sourceMappingURL=login-DnLqFclH.mjs.map
